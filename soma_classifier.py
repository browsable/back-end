import pandas as pd

train_df = pd.read_pickle("soma_goods_train.df")

train_df.shape

train_df

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()

d_list = []
cate_list = []
for each in train_df.iterrows():
    cate = ";".join([each[1]['cate1'],each[1]['cate2'],each[1]['cate3']])
    d_list.append(each[1]['name'])
    cate_list.append(cate)

print len(set(cate_list))

cate_dict = dict(zip(list(set(cate_list)),range(len(set(cate_list)))))

print cate_dict[u'디지털/가전;네트워크장비;KVM스위치']
print cate_dict[u'패션의류;남성의류;정장']

y_list = []
for each in train_df.iterrows():
    cate = ";".join([each[1]['cate1'],each[1]['cate2'],each[1]['cate3']])
    y_list.append(cate_dict[cate])

x_list = vectorizer.fit_transform(d_list)

from sklearn.svm import LinearSVC
from sklearn.grid_search import GridSearchCV
import numpy as np

svc_param = {'C':np.logspace(-2,0,20)}
gs_svc = GridSearchCV(LinearSVC(loss='l2'),svc_param,cv=5,n_jobs=4)

gs_svc.fit(x_list, y_list)

print gs_svc.best_params_, gs_svc.best_score_
clf = LinearSVC(C=gs_svc.best_params_['C'])
clf.fit(x_list,y_list)

from sklearn.externals import joblib

joblib.dump(clf,'classify.model',compress=3)
joblib.dump(cate_dict,'cate_dict.dat',compress=3)
joblib.dump(vectorizer,'vectorizer.dat',compress=3)

import requests

name='[신한카드5%할인][예화-좋은아이들] 아동한복 여아 1076 빛이나노랑'
img=''

u='http://localhost:8887/classify?name=%s&img=%s'

r = requests.get(u%(name,img)).json()

print r