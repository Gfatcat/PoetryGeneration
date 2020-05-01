from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf

import os
from tensorflow.contrib import learn
import numpy as np

documents = [
    '欲 出 未 出 光 辣 达 ，千 山 万 山 如 火 发 。须 臾 走 向 天 上 来 ， 逐 却 残 星 赶 却 月 。',
    '片 片 飞 来 静 又 闲 ，楼 头 江 上 复 山 前。飘零尽日不归去，帖破清光万里天。',
    '一气东南王斗牛，祖龙潜为子孙忧。金陵地脉何曾断，不觉真人已姓刘。'
]
# vocab = learn.preprocessing.VocabularyProcessor(32)
# x = np.array(list(vocab.fit_transform(documents)))
lines_dataset = tf.data.TextLineDataset(documents)
for ex in lines_dataset.take(3):
    print(ex)