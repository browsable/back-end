#-*- coding: utf-8 -*-

import pandas as pd
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.grid_search import GridSearchCV
import numpy as np
from sklearn.externals import joblib
import re
import requests
import simplejson
import json
from pprint import pprint
from nltk.util import ngrams
import nltk
from functools import reduce
from konlpy.tag import Kkma
train_df = pd.read_pickle("soma_goods_train.df")
train_df.shape
train_df

k = Kkma()
t=Twitter()
vectorizer = CountVectorizer()

d_list = []
cate_list = []

for each in train_df.iterrows():
    #한국어정리
    ko = re.sub(u'[^가-힣]+', " ", each[1]['name'])
    ko = re.sub(u'(해외|[0-20]*?%즉시할인쿠폰)', " ", ko)
    ko = " ".join(list(set(x[0] for x in t.pos(ko))
                .union(x for x in nltk.word_tokenize(ko))))
    ko += " ".join(x[0] + x[1] for x in nltk.ngrams(ko,2))
    ko += " ".join(x[0] + x[1] + x[2] for x in nltk.ngrams(ko, 3))
    #영어정리
    en = re.sub(u'[^A-Za-z]+', " ", each[1]['name']).lower()
    en = re.sub("intelintel", "intel", en)
    en = re.sub("ibmibm", "ibm", en)
    en = " ".join(list(set(x[0] for x in t.pos(en))
                .union(x for x in nltk.word_tokenize(en))))
    en += " ".join(x[0] + x[1] for x in nltk.ngrams(en, 2))
    en += " ".join(x[0] + x[1] + x[2] for x in nltk.ngrams(en, 3))
    if(ko==""): name = en
    else : name = ko+" "+en;
    name = re.sub(u'[  |   |    |     |      ]+', " ", name)
    print name

    cate = ";".join([each[1]['cate1'], each[1]['cate2'], each[1]['cate3']])
    d_list.append(name)
    cate_list.append(cate)

print len(set(cate_list))

cate_dict = dict(zip(list(set(cate_list)), range(len(set(cate_list)))))

y_list = []
for each in train_df.iterrows():
    cate = ";".join([each[1]['cate1'], each[1]['cate2'], each[1]['cate3']])
    y_list.append(cate_dict[cate])

x_list = vectorizer.fit_transform(d_list)

svc_param = {'C': np.logspace(-2, 0, 20)}
gs_svc = GridSearchCV(LinearSVC(loss='l2'), svc_param, cv=5, n_jobs=4)

gs_svc.fit(x_list, y_list)

clf = LinearSVC(C=gs_svc.best_params_['C'])
clf.fit(x_list, y_list)
joblib.dump(clf, 'classify.model', compress=3)
joblib.dump(cate_dict, 'cate_dict.dat', compress=3)
joblib.dump(vectorizer, 'vectorizer.dat', compress=3)
    # ngram_name = name;
    # ngram_name = " ".join(((x for x in range(len(ngram))) for ngram in ngrams(ngram_name,i)) for i in range(5))
    # print ngram_name
#     for x in ngrams(ngram_name,2):
#         name += x[0]+x[1]+" "
#     for x in ngrams(ngram_name,3):
#         name += x[0]+x[1]+x[2]+" "
#     for x in ngrams(ngram_name,4):
#         name += x[0]+x[1]+x[2]+x[3]+" "
#     for x in ngrams(ngram_name,5):
#         name += x[0]+x[1]+x[2]+x[3]+x[4]+" "
#     final=""
#     for str in name.split(" "):
#         if len(str)==1:
#             final+="";
#         else :
#             final += str+" "
#     final = " ".join(x for x in set(final.split(" ")))
#     final = re.sub(u'[ |  |   |    |     |      |       |         |          |]+', " ", name)
#
#     print final

