import re
import time
import sys
import os
import numpy as np
import unicodedata as ud
from gensim.models import FastText as ft
from pyarabic.araby import strip_tashkeel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def normalizeArabic(text):
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("\[", "", text)
    text = re.sub("\]", "", text)
    return(text)
    

def getResult(text):
    print("START READ AND PREPROCESSING", text)
    # kitab = np.load('dataset/numpy/kitabsave.npy', allow_pickle=True)
    kitab = np.load(resource_path('./data/numpy/kitabsave.npy'), allow_pickle=True)
    kitab = kitab.tolist()
    # sentence_clear = np.load('dataset/numpy/sentence_clearsave.npy', allow_pickle=True)
    sentence_clear = np.load(resource_path('./data/numpy/sentence_clearsave.npy'), allow_pickle=True)
    sentence_clear = sentence_clear.tolist()
    # kategori = np.load('dataset/numpy/kategori.npy', allow_pickle=True)
    kategori = np.load(resource_path('./data/numpy/kategori.npy'), allow_pickle=True)
    kategori = kategori.tolist()
    # namakitab = np.load('dataset/numpy/namakitab.npy', allow_pickle=True)
    namakitab = np.load(resource_path('./data/numpy/namakitab.npy'), allow_pickle=True)
    namakitab = namakitab.tolist()

    # kitab[0][1]
    # modelFT = ft.load('Model/modelFT.model')
    modelFT = ft.load(resource_path('./data/model/modelFT.model'))

    # MOST SIMILAR WE
    hasilQE = modelFT.wv.most_similar(text)
    hasilQE = [(strip_tashkeel(''.join(c for c in hasilQE[i][0] if not ud.category(c).startswith('P'))), hasilQE[i][1]) for i in range(len(hasilQE))]
    print(hasilQE)

    #TF-IDF
    tfidf_vectorizer = TfidfVectorizer()

    norm_tf=[]
    for isikitab in kitab:
        for ktb in isikitab:
            norm_tfidf = normalizeArabic(ktb)
            norm_tf.append(norm_tfidf)

    tfidf_doc = tfidf_vectorizer.fit_transform(norm_tf) 
    PIFQvectorizer = CountVectorizer()
    vectoreTF = PIFQvectorizer.fit_transform(norm_tf)
    featureTf = PIFQvectorizer.get_feature_names()

    cosim = [] 
    nilaicosim = []
    hasilQEpakai = hasilQE[0:3]
    for i in hasilQEpakai:
        tes=i[0]
        print(tes)

        tfidf_query = tfidf_vectorizer.transform([tes])
        cos=0.0
        #hitung kedekatan query pada masing masing dokumen 
        cos=cosine_similarity(tfidf_doc,tfidf_query)
        # print(type(cos))
        cosim.append(max(cos))
        nilaicosim.append(cos)

        # print('tfidf')
        # ================
        countTF = []
        s = ''.join(c for c in tes if not ud.category(c).startswith('P'))
        s = strip_tashkeel(s)
        for k in range(len(featureTf)):
            if featureTf[k] == s:
            # print(k)
                for j in range(vectoreTF.shape[0]):
                    countTF.append(vectoreTF[j,k]) 

    print("======= hasil Cosim ===========")
    finaloutput = []
    angka = 0
    for i in nilaicosim:
        print(hasilQE[angka][0])
        for j in range(len(i)):
            if i[j] == cosim[angka]:
                panjangkitab= 0
                for iterkitab in range(len(kitab)):
                    panjangkitab = panjangkitab + len(kitab[iterkitab])
                    if j <= panjangkitab:
                        tessplit = kitab[iterkitab][0].split(',')
                        print('Nama Kitab {} halaman ke {}'.format(namakitab[iterkitab],tessplit[4]))
                        print('isi kitab', tessplit[5])
                        finaloutput.append({'namakitab': namakitab[iterkitab], 'halaman': tessplit[4], 'isikitab': tessplit[5]})
                        break
        angka += 1
    return finaloutput

if __name__ == "__main__":
    # text = "الدليل"
    text = "القياس"
    res = getResult(text)
    print("===========================================")
    print(res)