import os
import json
import pandas as pd


def char_cut(text):
    char_list = [i for i in text]
    if len(char_list) % 6 == 0:
        char_num = 5
    elif len(char_list) % 8 == 0:
        char_num = 7
    else:
        char_num = 0
    char_list.append('<end>')
    return char_num, char_list


def rhy_cut(text):
    rhy_list = [i for i in text]
    rhy_list.append('<end>')
    return rhy_list


def deal_file(file_name):
    with open(os.path.join(file_name), 'r', encoding='UTF-8') as file:
        json_dict = json.load(file)
        for item in json_dict:
            num_sents = len(item['paragraphs'])
            if num_sents not in [2, 4]:
                continue
            texts = ''
            thythms = ''
            for i in range(num_sents):
                texts += item['paragraphs'][i]
                thythms += item['strains'][i]
            char_num, char_list = char_cut(texts)
            if char_num ==0:
                continue
            rhy_list = rhy_cut(thythms)
            # 五绝
            if char_num == 5 and num_sents ==2:
                pass
            # 五律
            elif char_num == 5 and num_sents ==4:
                pass
            # 七绝
            elif char_num == 7 and num_sents ==2:
                pass
            # 七律
            elif char_num == 7 and num_sents ==4:
                pass



path = os.getcwd()[:-15]
for file_name in os.listdir(os.path.join(path, 'poetry')):
    deal_file(os.path.join(path, 'poetry', file_name))
