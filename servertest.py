#-*- coding: utf-8 -*-
from sklearn.externals import joblib

from threading import  Condition
import re
from konlpy.tag import Twitter
import nltk
from nltk.util import ngrams
import numpy as np
import pandas as pd
import operator

clf = joblib.load('classify.model')
cate_dict = joblib.load('cate_dict.dat')
vectorizer = joblib.load('vectorizer.dat')
joblib.dump(clf,'n_classify.model')
joblib.dump(cate_dict,'n_cate_dict.dat')
joblib.dump(vectorizer,'n_vectorizer.dat')
cate_id_name_dict = dict(map(lambda (k,v):(v,k),cate_dict.items()))

t=Twitter()
_CONDITION = Condition()
word_dic = np.load('word_dic.npy').item()

train_df = pd.read_pickle("soma_goods_train.df")
train_df.shape
train_df
# f = open("data.txt", 'r')
# lines = f.readlines()
n_split = {}
blacklist = [20, 0, 57,81,0,26,17,57,1,31,101,17,18,85,98,23,63,22,100,96,80,59,16]
wrongcnt = 0;
for each in train_df.iterrows():
    cate = ";".join([each[1]['cate1'], each[1]['cate2'], each[1]['cate3']])
    name_split = name.split(" ")
    for word in name_split:
        if word in n_split:
            n_split[word] += 1
        else:
            n_split[word]=1

    name = re.sub(u'[^가-힣A-Za-z0-9.]+', " ", each[1]['name'])
    # name = name.lower()
    name = re.sub(u'(해외|[가-힣0-20]*?할인[가-힣0-20]*?|정품)', " ", name)
    name = " ".join(list(set(x[0] for x in t.pos(name))
                         .union(x for x in nltk.word_tokenize(name))))
    # name += " ".join(x[0] + x[1] for x in nltk.ngrams(name,2))
    # name += " ".join(x[0] + x[1] + x[2] for x in nltk.ngrams(name, 3))
    names = name.split(" ")
    name = " ".join(list(set(x for x in names)))
    name = re.sub(u' +', " ", name)
    name = re.sub(u' . ', " ", name)

    pred = clf.predict(vectorizer.transform([name]))[0]

    # if pred in blacklist:
    #     if pred==0:
    #         if u'Coms KVM'in each[1]['name']:
    #             pred = 84
    #     elif pred==107:
    #         if u'(GL|케이블가이|EZ|산화)'in name:
    #             pred = 31
    if (cate_id_name_dict[pred] != cate):
        wrongcnt +=1;

    # if(cate_id_name_dict[pred]!=cate):
    #     print u"------------------------------"
    #     print u"제품 :" + each[1]['name']
    #     print u"수정 :" + name
    #     code = 0;
    #     for item in cate_id_name_dict.items():
    #         if(item[1]==cate):
    #             code = item[0]
    #     print u"예측 :" '%s' u" 코드 : " '%d' % (cate_id_name_dict[pred], pred)
    #     print u"원본 :" '%s' u" 코드 : " '%d' % (cate, code)
    #     print u"------------------------------"

#f.close()

sorted_x = sorted(n_split.items(), key=operator.itemgetter(1))

for dic in sorted_x:
    print dic[0]
    print dic[1]
print wrongcnt