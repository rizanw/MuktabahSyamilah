import re
import time
import sys
import os
import numpy as np
import pandas as pd
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

    kitab = np.load('data/numpy/kitabsave.npy', allow_pickle=True)
    kitab = kitab.tolist()
    sentence_clear = np.load('data/numpy/sentence_clearsave.npy', allow_pickle=True)
    sentence_clear = sentence_clear.tolist()
    kategori = np.load('data/numpy/kategori.npy', allow_pickle=True)
    kategori = kategori.tolist()
    namakitab = np.load('data/numpy/namakitab.npy', allow_pickle=True)
    namakitab = namakitab.tolist()
    modelFT = ft.load('data/model/modelFT.model')

    #TF-IDF
    tfidf_vectorizer = TfidfVectorizer()

    norm_tf=[]
    for isikitab in kitab:
        for ktb in isikitab:
            norm_tfidf = normalizeArabic(ktb)
            norm_tf.append(norm_tfidf)

    tfidf_doc = tfidf_vectorizer.fit_transform(norm_tf)
    tfidf_word=tfidf_vectorizer.get_feature_names()

    PIFQvectorizer = CountVectorizer()
    vectoreTF = PIFQvectorizer.fit_transform(norm_tf)
    featureTf = PIFQvectorizer.get_feature_names()

    # baca = pd.read_csv('katakunci.csv')
    # baca.values[5:10]

    cosimhasil = []
    cosimhasilnilai = []
    hasilqenilaidicosim = []
    namakitabcosim = []
    halamankitabcosim = []
    isikitabcosim = []
    inputandicosim = []

    # kata = "القياس"
    # kata = "الظن"
    kata = text
    # no = 1
    # for key in baca.values[0:50]:
    # kata = key[0]
    # print(no, 'key', kata)
    # no = no +1
    # MOST SIMILAR WE
    hasilQE = modelFT.wv.most_similar(kata)

    hasilQE = [(strip_tashkeel(''.join(c for c in hasilQE[i][0] if not ud.category(c).startswith('P'))), hasilQE[i][1]) for i in range(len(hasilQE))]
    # print(hasilQE)

    cosim = [] 
    nilaicosim = []
    QEpakai = hasilQE[0:3]
    for i in QEpakai:
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
    #         if len(countTF) < 1 :
    #             for j in range(vectoreTF.shape[0]):
    #                 countTF.append(0.0)

    #     print("======= hasil Cosim ===========")
    angka = 0
    finaloutput = []
    for i in nilaicosim:
    #         print(hasilQE[angka][0])
        for j in range(len(i)):
            if i[j] == cosim[angka]:
                panjangkitab= 0
                for iterkitab in range(len(kitab)):
                    panjangkitab = panjangkitab + len(kitab[iterkitab])
                    if j <= panjangkitab:
                        tessplit = kitab[iterkitab][0].split(',')
    #                         print('Nama Kitab {} halaman ke {}'.format(namakitab[iterkitab],tessplit[4]))
    #                         print('isi kitab : ', tessplit[5])
                        cosimhasil.append(hasilQE[angka][0])
                        hasilqenilaidicosim.append(hasilQE[angka][1])
                        cosimhasilnilai.append(cosim[angka])
                        namakitabcosim.append(namakitab[iterkitab])
                        halamankitabcosim.append(tessplit[4])
                        isikitabcosim.append(tessplit[5])
                        inputandicosim.append(kata)
                        finaloutput.append({"namakitab":namakitab[iterkitab], "halaman":tessplit[4],"isikitab":tessplit[5]})
                        break
                break
        angka += 1
            
    print("============== selesai ===============")

    nilaihasilcosim = []
    for i in cosimhasilnilai:
        nilaihasilcosim.append(i[0])
    
    dfcosim = pd.DataFrame(list(zip(inputandicosim, cosimhasil, hasilqenilaidicosim, nilaihasilcosim, namakitabcosim, halamankitabcosim, isikitabcosim)), 
                columns =['inputan kata','QE', 'Nilai QE', 'Nilai Cosim', 'nama kitab', 'halaman', 'isi']) 

    print(dfcosim)

    return finaloutput
    # dfcosim.to_csv('hasil/dfFullcosim.csv', encoding='cp1256')

if __name__ == "__main__":
    # text = "الدليل"
    text = "الظن"
    res = getResult(text)
    print("===========================================")
    print(res)
