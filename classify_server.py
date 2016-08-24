#-*- coding: utf-8 -*-

from sklearn.externals import joblib
from bottle import route, run, template, request, get, post
from threading import Condition
from konlpy.tag import Twitter
import nltk
from urllib import quote_plus as q, unquote_plus as unq, urlencode
from urllib2 import build_opener, urlopen, HTTPCookieProcessor
from cookielib import CookieJar
import re
t = Twitter()
_CONDITION = Condition()

__author__ = 'bluele'

BASE_URL = 'https://www.google.co.jp'
BASE_SEARCH_URL = BASE_URL + '/searchbyimage?%s'

REFERER_KEY = 'Referer'

Opener = build_opener(HTTPCookieProcessor(CookieJar()))
Opener.addheaders = [
    ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'),
    ('Accept-Language', 'ja,en-us;q=0.7,en;q=0.3')
]

image_url_pattern = re.compile(ur'^http://www.google.co.jp/imgres\?imgurl=(?P<url>[^&]+)')


clf = joblib.load('classify.model')
cate_dict = joblib.load('cate_dict.dat')
vectorizer = joblib.load('vectorizer.dat')

joblib.dump(clf,'n_classify.model')
joblib.dump(cate_dict,'n_cate_dict.dat')
joblib.dump(vectorizer,'n_vectorizer.dat')
cate_id_name_dict = dict(map(lambda (k,v):(v,k),cate_dict.items()))



def set_referer(url):
    cur = get_referer_index()
    if cur is not None:
        del Opener.addheaders[cur]
    Opener.addheaders.append(
        (REFERER_KEY, url)
    )


def search_image(url):
    params = {
        'image_url': url,
        'hl': 'ja',
    }
    query = BASE_SEARCH_URL % urlencode(params)
    f = Opener.open(query)
    url = f.url
    # domain
    # url += '&as_sitesearch=zozo.jp'
    f = Opener.open(url)
    html = f.read()
    set_referer(f.url)
    return html


def get_referer_index():
    i = 0
    for k, v in Opener.addheaders:
        if k == REFERER_KEY:
            return i
        i += 1
    else:
        return None


def get_referer():
    cur = get_referer_index()
    if cur is not None:
        return Opener.addheaders[cur]
    else:
        return None


@route('/classify')
def classify():
    print "classify called"
    img = request.GET.get('img', '')
    # 이미지 사용하지 못함..
    #     html = search_image(img)
    #     soup = BeautifulSoup.BeautifulSoup(html)
    #     cateFromImg = soup.findAll('a', attrs={'class':'_gUb'})
    #     print cateFromImg
    name = request.GET.get('name', '').decode('utf-8')

    name = re.sub(u'[^가-힣A-Za-z0-9.]+', " ", name)
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

    pred = clf.predict(vectorizer.transform([name]))[0]
    return {'cate': cate_id_name_dict[pred]}


run(host='0.0.0.0', port=8887)
