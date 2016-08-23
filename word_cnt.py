#-*- coding: utf-8 -*-

import re
import nltk
import numpy as np
import operator
word_dic = np.load('word_dic.npy').item()


#name = u'[모리케이블] [M07321] 넷메이트(Netmate) CAT5 KVM 스위치 USB Dongle [DGU-01]'
namelist = [u'[모리케이블] [M07321] 넷메이트(Netmate) CAT5 KVM 스위치 USB Dongle [DGU-01]',u'[5%즉시할인쿠폰](P1j)폰줄/사각무늬곰돌이(10개1Set)',u'[해외][구매대행][B00MMVIFZM] Voltage References 3.3V Prec Micropwr LDO Low VRef (5 pieces)']
for name in namelist:
    cate_dic = {}
    name = re.sub(u'[^가-힣A-Za-z]', " ", name)
    name = re.sub(u'(해외|[0-20]*?%즉시할인쿠폰|[가-힣]*?배송|배송[가-힣]*?|[가-힣]*?배송|[09]*?원|구매대행|직구|정품)+', " ", name)
    ko = re.sub(u'(^가-힣)', " ", name)
    ko = " ".join(list(set(x for x in nltk.word_tokenize(ko))))
    # 영어정리
    en = re.sub(u'[^A-Za-z]+', " ", name)
    en = en.lower()
    en = re.sub("intelintel", "intel", en)
    en = re.sub("ibmibm", "ibm", en)
    if (ko == ""):
        name = en
    else:
        name = ko + " " + en;
    # final = ""
    # for str in name.split(" "):
    #     if len(str)==1:
    #         final+="";
    #     else :
    #         final += str+" "
    # final = " ".join(x for x in set(final.split(" ")))
    name = re.sub(u' +', " ", name)

    word_list = name.split(" ")
    for word in word_list:
        try:
            for cate in word_dic[word]:
                if cate in cate_dic:
                    cate_dic[cate] += word_dic[word][cate]
                else:
                    cate_dic[cate] = word_dic[word][cate]
        except KeyError:
                print "error word:"+word

    max_key = max(cate_dic, key=lambda k: cate_dic[k])
    print max_key