#-*- coding: utf-8 -*-

import pandas as pd
from konlpy.tag import Twitter
from konlpy.tag import Kkma
from konlpy.tag import Hannanum
from konlpy.tag import Komoran
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
train_df = pd.read_pickle("soma_goods_train.df")
train_df.shape
train_df

#komoran = Komoran()
t=Twitter()
vectorizer = CountVectorizer()

d_list = []
cate_list = []

for each in train_df.iterrows():
    name = re.sub(u'[^가-힣A-Za-z0-9.]', " ", each[1]['name']).lower()
    name = re.sub(u'(해외|[가-힣0-20]*?할인[가-힣0-20]*?|구매대행|정품|대리점|폴더접이식)', " ", name)
    bigram = " ".join(x[0] + x[1] for x in nltk.ngrams(name, 2))
    bfinal = ""
    for str in bigram.split(" "):
        if len(str) == 1:
            bfinal += "";
        else:
            bfinal += str + " "
    bfinal = " ".join(x for x in set(bfinal.split(" ")))
    trigram = " ".join(x[0] + x[1] + x[2] for x in nltk.ngrams(name, 3))
    tfinal = ""
    for str in trigram.split(" "):
        if len(str) == 1:
            tfinal += "";
        else:
            tfinal += str + " "
    tfinal = " ".join(x for x in set(tfinal.split(" ")))
    name = " ".join(list(set(x for x in nltk.word_tokenize(name))))
    name += bfinal + " " + tfinal
    names = name.split(" ")
    name = " ".join(list(set(x for x in names)))
    name = re.sub(u' +', " ", name)
    print name
    cate = ";".join([each[1]['cate1'],each[1]['cate2'],each[1]['cate3']])
    d_list.append(name)
    cate_list.append(cate)

print len(set(cate_list))

cate_dict = dict(zip(list(set(cate_list)),range(len(set(cate_list)))))

y_list = []
for each in train_df.iterrows():
    cate = ";".join([each[1]['cate1'],each[1]['cate2'],each[1]['cate3']])
    y_list.append(cate_dict[cate])

x_list = vectorizer.fit_transform(d_list)

svc_param = {'C':np.logspace(-2,0,20)}
gs_svc = GridSearchCV(LinearSVC(loss='l2'),svc_param,cv=5,n_jobs=4)

gs_svc.fit(x_list, y_list)

clf = LinearSVC(C=gs_svc.best_params_['C'])
clf.fit(x_list,y_list)
joblib.dump(clf,'classify.model',compress=3)
joblib.dump(cate_dict,'cate_dict.dat',compress=3)
joblib.dump(vectorizer,'vectorizer.dat',compress=3)
