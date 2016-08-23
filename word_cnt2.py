#-*- coding: utf-8 -*-

import re
import nltk
import numpy as np
from konlpy.tag import Twitter
word_dic = np.load('word_dic.npy').item()
t=Twitter()

namelist = [u'[모리케이블] [M07321] 넷메이트(Netmate) CAT5 KVM 스위치 USB Dongle [DGU-01]',u'[5%즉시할인쿠폰](P1j)폰줄/사각무늬곰돌이(10개1Set)',u'[해외][구매대행][B00MMVIFZM] Voltage References 3.3V Prec Micropwr LDO Low VRef (5 pieces)']
for name in namelist:
    cate_dic = {}
    name = re.sub(u'[^가-힣A-Za-z]', " ", name)
    name = re.sub(u'(해외|[0-20]*?%즉시할인쿠폰|[0-9]*?원)+', " ", name)
    name = " ".join(list(set(x[0] for x in t.pos(name))
                         .union(x for x in nltk.word_tokenize(name))))
    name = re.sub(u' +', " ", name)
    print name

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

    #print max(cate_dic.iteritems(), key=operator.itemgetter(1))[0]

    ddd = {'a': 3, 'b': 1}
    max_key = max(cate_dic, key=lambda k: cate_dic[k])
    print max_key