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
from nltk import collocations
import random
train_df = pd.read_pickle("soma_goods_train.df")
train_df.shape
train_df

k = Kkma()
t=Twitter()
vectorizer = CountVectorizer()
bigram_measures=collocations.BigramAssocMeasures()


d_list = []
cate_list = []

for each in train_df.iterrows():

    name = re.sub(u'[^가-힣A-Za-z0-9.]+', " ", each[1]['name'])
    name = re.sub(u'(해외|[가-힣0-20]*?할인[가-힣0-20]*?)', " ", name)
    name = re.sub(u' +', " ", name)
    name = re.sub(u' \. ', " ", name)
    name = re.sub(u' [0-99] ', " ", name)
    name = " ".join(list(set(x[0] for x in t.pos(name))
                .union(x for x in nltk.word_tokenize(name))))
    names = name.split(" ")
    name = " ".join(list(set(x for x in names)))
    name = re.sub(u' +', " ", name)
    name = re.sub(u' \. ', " ", name)
    name = re.sub(u' [0-99] ', " ", name)
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

# svc_param = {'C': np.logspace(-2, 0, 20)}
# gs_svc = GridSearchCV(LinearSVC(loss='l2'), svc_param, cv=5, n_jobs=4)
#
# gs_svc.fit(x_list, y_list)
# print gs_svc.best_params_['C']
# 0.143844988829
clf = LinearSVC(C=0.145422494412)
clf.fit(x_list, y_list)
joblib.dump(clf, 'classify.model', compress=3)
joblib.dump(cate_dict, 'cate_dict.dat', compress=3)
joblib.dump(vectorizer, 'vectorizer.dat', compress=3)


