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
    print("START READ AND PREPROCESSING")

    # kitab = np.load('./data/dataset/kitabsave.npy')
    kitab = np.load(resource_path('./data/dataset/kitabsave.npy'))
    kitab = kitab.tolist()
    # sentence_clear = np.load('./data/dataset/sentence_clearsave.npy')
    sentence_clear = np.load(resource_path('./data/dataset/sentence_clearsave.npy'))
    sentence_clear = sentence_clear.tolist()
    # kategori = np.load('./data/dataset/kategori.npy')
    kategori = np.load(resource_path('./data/dataset/kategori.npy'))
    kategori = kategori.tolist()
    # namakitab = np.load('./data/dataset/namakitab.npy')
    namakitab = np.load(resource_path('./data/dataset/namakitab.npy'))
    namakitab = namakitab.tolist()
    # modelFT = ft.load('./data/model/modelFT.model')
    modelFT = ft.load(resource_path('./data/model/modelFT.model'))

    # MOST SIMILAR WE
    hasilQE = modelFT.wv.most_similar(text)
    hasilQE = [(strip_tashkeel(''.join(c for c in hasilQE[i][0] if not ud.category(
        c).startswith('P'))), hasilQE[i][1]) for i in range(len(hasilQE))]
    # print(hasilQE)

    # TF-IDF
    tfidf_vectorizer = TfidfVectorizer()

    isikitab = ''
    ktb = []
    for i in range(len(kitab)):
        for j in kitab[i]:
            isikitab = ''.join(kitab[i])
        ktb.append(isikitab)

    norm_tf = []
    for i in range(len(ktb)):
        norm_tfidf = normalizeArabic(ktb[i])
        norm_tf.append(norm_tfidf)

    tfidf_doc = tfidf_vectorizer.fit_transform(norm_tf)
 
    cosim = []
    nilaicosim = []
    for i in hasilQE:
        tes = i[0]
        # print(tes)
        tfidf_query = tfidf_vectorizer.transform([tes])
        cos = 0.0
        # hitung kedekatan query pada masing masing dokumen
        cos = cosine_similarity(tfidf_doc, tfidf_query)
        # print(type(cos))
        cosim.append(max(cos))
        nilaicosim.append(cos)
 
    print("======= hasil Cosim ===========") 
    finaloutput = []
    angka = 0
    for i in nilaicosim: 
        for j in range(len(i)):
            if i[j] == cosim[angka]:
                print(kategori[0], '-', namakitab[j], '-', i[j])
                finaloutput.append(
                    {'namakitab': namakitab[j], 'kategori': kategori[0], 'nilai': i[j]})
        angka += 1

    # len_finaloutput = len(finaloutput)
    # for i in range(0, finaloutput):
    #     for j in range(0, len_finaloutput-i-1):
    #         if (finaloutput[j] < finaloutput[j+1]):
    #             temp = finaloutput[j]
    #             finaloutput[j] = finaloutput[j+1]
    #             finaloutput[j+1] = temp 

    return finaloutput

if __name__ == "__main__":
    text="الدليل"
    print("test case:", text)
    res = getResult(text)
    print(res)
    print(reversed(sorted(res, key=lambda k: k['nilai'])))