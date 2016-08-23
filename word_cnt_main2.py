#-*- coding: utf-8 -*-

import pandas as pd
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.grid_search import GridSearchCV
import numpy as np
from sklearn.externals import joblib
import re
import nltk
import numpy as np
train_df = pd.read_pickle("soma_goods_train.df")
train_df.shape
train_df

t=Twitter()
vectorizer = CountVectorizer()

#name_server = joblib.load('name_server.dat');
d_list = []
cate_list = []

word_dic = {} # 단어에 대한 카테고리 모음 { 인텔 :(A;B;C;,...)}
word_list = []

for each in train_df.iterrows():
    name = re.sub(u'[^가-힣A-Za-z0-9.]', " ", each[1]['name'])
    name = re.sub(u'(해외|[0-20]*?%즉시할인쿠폰|[가-힣]*?%배송)', " ", name)
    name += " ".join(x[0] + x[1] for x in nltk.ngrams(name, 2))
    name += " ".join(x[0] + x[1] + x[2] for x in nltk.ngrams(name, 3))
    name = " ".join(list(set(x[0] for x in nltk.word_tokenize(name)).union(x[0] for x in t.pos(name))))
    cate = ";".join([each[1]['cate1'], each[1]['cate2'], each[1]['cate3']])

    word_list = name.split(" ")
    for word in word_list:
        if word in word_dic:
            if cate in word_dic[word]:
                #try:
                word_dic[word][cate] += 1
                #except KeyError:
            else:
                word_dic[word][cate] = 1
        else:
            word_dic[word] = {cate : 1}

np.save('word_dic.npy', word_dic)
