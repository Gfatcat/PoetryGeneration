import os
import json
import numpy as np
from tqdm import tqdm
import pandas as pd
import jieba
import jieba.analyse


def char_cut(text):
    char_list = [i for i in text if i not in ["，", "。", "？", "！"]]
    if len(char_list) / 5 == 4:
        char_form = "五绝"
    elif len(char_list) / 5 == 8:
        char_form = "五律"
    elif len(char_list) / 7 == 4:
        char_form = "七绝"
    elif len(char_list) / 7 == 8:
        char_form = "七律"
    else:
        char_form = 0
    return char_form, string_add_space(text)


def list2str(strlist):
    string = ''
    for item in strlist:
        item = string_add_space(item)
        string += item
        string += ' '
    return string[:-1]


def string_add_space(string):
    output_string = ""
    for item in string:
        output_string += item
        output_string += ' '
    return output_string[:-1]


def deal_file(file_name):
    with open(os.path.join(file_name), 'r', encoding='UTF-8') as file:
        json_dict = json.load(file)
        for item in tqdm(json_dict):
            num_sentences = len(item['paragraphs'])
            if num_sentences not in [2, 4]:
                continue

            # 提取诗句、格律、作者和标题
            paragraphs = ''
            strains = ''
            for i in range(num_sentences):
                paragraphs += item['paragraphs'][i]
                strains += item['strains'][i]
            author = item['author']
            title = string_add_space(item["title"])

            form, paragraphs_add_space = char_cut(paragraphs)
            if form == 0:
                continue
            strains_add_space = string_add_space(strains)

            # 格式: 五律、五绝、七律、七绝
            global data, counter, current_line_num
            counter[form] += 1
            keywords = jieba.analyse.textrank(paragraphs, topK=5, withWeight=False,
                                              allowPOS=('ns', 'n', 'vn', 'v', 'a'))
            if len(keywords) == 0:
                keywords = jieba.analyse.tfidf(paragraphs, topK=5, withWeight=False,
                                               allowPOS=('ns', 'n', 'vn', 'v', 'a'))
            keywords = list2str(keywords)
            current_line = [strains_add_space, author, paragraphs_add_space, title, form, keywords, 0]
            poem_with_space = title + ':' + string_add_space(keywords) + ':' + str(
                form) + '::' + strains_add_space + '::' + paragraphs_add_space
            keywords =keywords.replace(" ", "")
            poem_without_space = title + ':' + keywords + ':' + str(form) + '::' + strains + '::' + paragraphs
            data.append(current_line)
            poems_with_space.append(poem_with_space)
            poems_without_space.append(poem_without_space)


# 诗歌数量统计器 五律、五绝、七律、七绝
counter = {
    "五律": 0,
    "五绝": 0,
    "七律": 0,
    "七绝": 0,
}
current_line_num = 0
"""
Data form:
[ n * (strains, author, paragraphs, title, form, keywords, sentiment)]
[ n * 7]
"""
data = []
poems_with_space = []
poems_without_space = []
path = os.getcwd()[:-15]
file_list = os.listdir(os.path.join(path, 'poetry'))
file_list_length = len(file_list)
count = 0
for file_name in file_list:
    count += 1
    print("Processing {},  {}/{}".format(file_name, count, file_list_length))
    deal_file(os.path.join(path, 'poetry', file_name))
    print(counter)

data_frame = pd.DataFrame(data)
data_frame.columns = ['strains', 'author', 'paragraphs', 'title', 'form', 'keywords', 'sentiment']
data_frame.to_csv('poetry.csv', encoding='utf-8')

with open('poems_with_space.txt', 'wb', encoding='utf-8') as file:
    file.writelines(["%s\n" % poem for poem in poems_with_space])

with open('poems_without_space.txt', 'wb', encoding='utf-8') as file:
    file.writelines(["%s\n" % poem for poem in poems_without_space])
