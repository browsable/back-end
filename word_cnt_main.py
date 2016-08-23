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
    # 한국어정리
    name = re.sub(u'[^가-힣A-Za-z]', " ", each[1]['name'])
    name = re.sub(u'(해외|[0-20]*?%즉시할인쿠폰|[가-힣]*?배송|배송[가-힣]*?|[가-힣]*?배송|[09]*?원|구매대행|직구|정품)+', " ", name)
    ko = re.sub(u'(^가-힣)', " ", name)
    ko = " ".join(list(set(x for x in nltk.word_tokenize(ko))))
    # 영어정리
    en = re.sub(u'[^A-Za-z]+', " ", name)
    en = en.lower()
    en = re.sub("intelintel", "intel", en)
    en = re.sub("ibmibm", "ibm", en)
    name = ko + " " + en;
    # final = ""
    # for str in name.split(" "):
    #     if len(str)==1:
    #         final+="";
    #     else :
    #         final += str+" "
    # final = " ".join(x for x in set(final.split(" ")))
    name = re.sub(u' +', " ", name)
    print name
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
