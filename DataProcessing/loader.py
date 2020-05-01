import os
import numpy as np
import collections
import random
import pickle
import logging

logging.basicConfig(level=logging.INFO)

class DataLoader:
    def __init__(self, config):
        self.filename = config.filename
        self.is_evaluate = config.is_evaluate
        self.batch_size = config.batch_size
        self.train_rate = config.train_rate
        self.poems = []
        self.word_vocab = object()

        self.load_data()
        if os.path.isfile('vocab.pkl'):
            with open('vocab.pkl', 'rb') as file:
                self.word_vocab = pickle.load(file)
                logging.info("loaded previous vocabulary")
        else:
            self.create_vocab()

    def load_data(self):
        """读取处理过的数据集"""
        with open('poems.txt', 'r', encoding='utf-8') as file:
            for line in file:
                poem = line.strip()
                poem = poem.replace(' ', '')
                self.poems.append(poem)
        logging.info("loaded data")

    def create_vocab(self):
        # counting words
        wordFreq = collections.Counter()
        for poem in self.poems:
            wordFreq.update(poem)
        print(wordFreq)
        wordFreq[" "] = -1
        wordPairs = sorted(wordFreq.items(), key=lambda x: -x[1])
        words, freq = zip(*wordPairs)
        wordNum = len(words)
        self.word_vocab = dict(zip(words, range(wordNum)))  # word to ID
        with open('vocab.pkl', 'wb') as file:
            pickle.dump(self.word_vocab, file)
        logging.info("created vocabulary")

    def get_dataset(self):
        poemsVector = [([self.word_vocab[word] for word in poem]) for poem in self.poems]  # poem to vector
        if self.is_evaluate:  # evaluating need divide dataset into test set and train set
            self.trainVector = poemsVector[:int(len(poemsVector) * self.train_rate)]
            self.testVector = poemsVector[int(len(poemsVector) * self.train_rate):]
        else:
            self.trainVector = poemsVector
            self.testVector = []
        print("训练样本总数： %d" % len(self.trainVector))
        print("测试样本总数： %d" % len(self.testVector))
        pass

    def generateBatch(self, batchSize=64, isTrain=True):
        # padding length to batchMaxLength
        if isTrain:
            poemsVector = self.trainVector
        else:
            poemsVector = self.testVector

        random.shuffle(poemsVector)
        batchNum = (len(poemsVector) - 1) // batchSize
        X = []
        Y = []
        # create batch
        for i in range(batchNum):
            batch = poemsVector[i * batchSize: (i + 1) * batchSize]
            maxLength = max([len(vector) for vector in batch])
            temp = np.full((batchSize, maxLength), self.wordToID[" "], np.int32)  # padding space
            for j in range(batchSize):
                temp[j, :len(batch[j])] = batch[j]
            X.append(temp)
            temp2 = np.copy(temp)  # copy!!!!!!
            temp2[:, :-1] = temp[:, 1:]
            Y.append(temp2)
        return X, Y
