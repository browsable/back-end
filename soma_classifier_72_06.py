#-*- coding: utf-8 -*-

import pandas as pd
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
import re
import time
import nltk
from selenium import webdriver

train_df = pd.read_pickle("soma_goods_train.df")
train_df.shape
train_df

t=Twitter()
vectorizer = CountVectorizer()


d_list = []
cate_list = []
googlecate_dic = {}
i = 0
def searchfile(filePath):
        browser = webdriver.Firefox()
        browser.get('http://www.google.com.au/imghp')

        # Click "Search by image" icon
        elem = browser.find_element_by_class_name('gsst_a')
        elem.click()
        # Switch from "Paste image URL" to "Upload an image"
        browser.execute_script("google.qb.ti(true);return false")
        # Set the path of the local file and submit
        ele0 = browser.find_element_by_id("qbfile")
        ele0.send_keys(filePath)
        catename = browser.find_element_by_class_name("_gUb").text
        browser.close()
        browser.quit()
        print catename
        return catename


for each in train_df.iterrows():
    time.sleep(3)
    # 트위터와 nltk를 혼합하여 형태소 추출
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
    name = re.sub(u'[0-99] ', " ", name)
    # n그램 사용
    # bigram = " ".join(x[0] + x[1] for x in nltk.ngrams(name, 2))
    # bfinal = ""
    # for str in bigram.split(" "):
    #     if len(str) == 1:
    #         bfinal += "";
    #     else:
    #         bfinal += str + " "
    # bfinal = " ".join(x for x in set(bfinal.split(" ")))
    # trigram = " ".join(x[0] + x[1] + x[2] for x in nltk.ngrams(name, 3))
    # tfinal = ""
    # for str in trigram.split(" "):
    #     if len(str) == 1:
    #         tfinal += "";
    #     else:
    #         tfinal += str + " "
    # tfinal = " ".join(x for x in set(tfinal.split(" ")))

    # 구글 이미지 서치 이용하여 이미지의 카테고리 추출, 네임에 태깅
    # selenium을 사용하기 위해서는 파이어폭스가 설치되어 있어야함
    filename = each[0]
    filePath = "/Users/browsable/PycharmProjects/venv/soma_train/"+str(filename)+".jpg"
    catename = searchfile(filePath)
    googlecate_dic[filename] = catename
    name += " "+catename
    i+=1
    print i
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


