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
    kitab = np.load(resource_path('./data/dataset/kitabsave.npy'), allow_pickle=True)
    kitab = kitab.tolist()
    # sentence_clear = np.load('dataset/numpy/sentence_clearsave.npy', allow_pickle=True)
    sentence_clear = np.load(resource_path('./data/dataset/sentence_clearsave.npy'), allow_pickle=True)
    sentence_clear = sentence_clear.tolist()
    # kategori = np.load('dataset/numpy/kategori.npy', allow_pickle=True)
    kategori = np.load(resource_path('./data/dataset/kategori.npy'), allow_pickle=True)
    kategori = kategori.tolist()
    # namakitab = np.load('dataset/numpy/namakitab.npy', allow_pickle=True)
    namakitab = np.load(resource_path('./data/dataset/namakitab.npy'), allow_pickle=True)
    namakitab = namakitab.tolist()

    # kitab[0][1]
    # modelFT = ft.load('Model/modelFT.model')
    modelFT = ft.load(resource_path('./data/model/modelFT.model'))

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

    cosimhasil = []
    cosimhasilnilai = []
    hasilqenilaidicosim = []
    namakitabcosim = []
    halamankitabcosim = []
    isikitabcosim = []
    inputandicosim = []

    pifqhasil = []
    pifqhasilnilai = []
    hasilqenilaidipifq = []
    namakitabpifq = []
    halamankitabpifq = []
    isikitabpifq = []
    inputandipifq = []

    gabunganhasil = []
    gabunganhasilnilai = []
    hasilqenilaidigabungan = []
    namakitabgabungan= []
    halamankitabgabungan = []
    isikitabgabungan = []
    inputandigabungan = [] 
    
    # MOST SIMILAR WE
    hasilQE = modelFT.wv.most_similar(text)
    hasilQE = [(strip_tashkeel(''.join(c for c in hasilQE[i][0] if not ud.category(c).startswith('P'))), hasilQE[i][1]) for i in range(len(hasilQE))]
    # print(hasilQE)

    cosim = []
    hasilpifq = []
    hasilgabungan = []
    nilaihasilgabungan = []
    nilaihasilpifq = []
    nilaicosim = []
    QEpakai = hasilQE[0:3]
    for i in QEpakai:
        tes=i[0] 
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

        #PIFQ
        nilaipifq = []
        for k in countTF:
            if sum(countTF) == 0:
                nilaipifq.append(0)
            else:
                nilaipifq.append(1 + np.log10(1 + (k / sum(countTF))) + 0.5)
        nilaihasilpifq.append(nilaipifq)
        hasilpifq.append(max(nilaipifq))
        # print('pifq')

        #gabungan
        nilaigabungan = []
        for k in range(vectoreTF.shape[0]):
            nilaigabungan.append(nilaipifq[k] * cos[k][0])
        nilaihasilgabungan.append(nilaigabungan)
        hasilgabungan.append(max(nilaigabungan)) 

#     print("======= hasil Cosim ===========")
    angka = 0
    for i in nilaicosim:
#         print(hasilQE[angka][0])
        for j in range(len(i)):
            if i[j] == cosim[angka]:
                panjangkitab= 0;
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
                        # inputandicosim.append(kata)
                        break;
        angka += 1

#     print("====== hasil pifq ==========")
    angka = 0
    for i in nilaihasilpifq:
#         print(hasilQE[angka][0])
        for j in range(len(i)):
            if i[j] == hasilpifq[angka]:
                panjangkitab= 0;
                for iterkitab in range(len(kitab)):
                    panjangkitab = panjangkitab + len(kitab[iterkitab])
                    if j <= panjangkitab:
                        tessplit = kitab[iterkitab][0].split(',')
#                         print('Nama Kitab {} halaman ke {}'.format(namakitab[iterkitab],tessplit[4]))
#                         print('isi kitab : ', tessplit[5])
                        pifqhasil.append(hasilQE[angka][0])
                        pifqhasilnilai.append(hasilpifq[angka])
                        hasilqenilaidipifq.append(hasilQE[angka][1])
                        namakitabpifq.append(namakitab[iterkitab])
                        halamankitabpifq.append(tessplit[4])
                        isikitabpifq.append(tessplit[5])
                        # inputandipifq.append(kata)
                        break;
        angka += 1

#     print("============== Hasil Gabungan ===============")
    print("============== selesai ===============")
    angka = 0
    for i in nilaihasilgabungan:
#         print(hasilQE[angka][0])
        for j in range(len(i)):
            if i[j] == hasilgabungan[angka]:
                panjangkitab= 0;
                for iterkitab in range(len(kitab)):
                    panjangkitab = panjangkitab + len(kitab[iterkitab])
                    if j <= panjangkitab:
                        tessplit = kitab[iterkitab][0].split(',')
#                         print('Nama Kitab {} halaman ke {}'.format(namakitab[iterkitab],tessplit[4]))
#                         print('isi kitab : ', tessplit[5])
                        gabunganhasil.append(hasilQE[angka][0])
                        gabunganhasilnilai.append(hasilgabungan[angka])
                        hasilqenilaidigabungan.append(hasilQE[angka][1])
                        namakitabgabungan.append(namakitab[iterkitab])
                        halamankitabgabungan.append(tessplit[4])
                        isikitabgabungan.append(tessplit[5])
                        # inputandigabungan.append(kata)
                        break;
        angka += 1

    nilaihasilcosim = []
    for i in cosimhasilnilai:
        nilaihasilcosim.append(i[0])
 

    # dfcosim = pd.DataFrame(list(zip(inputandicosim, cosimhasil, hasilqenilaidicosim, nilaihasilcosim, namakitabcosim, halamankitabcosim, isikitabcosim)), 
    #             columns =['inputan kata', 'QE', 'Nilai QE', 'Nilai Cosim', 'nama kitab', 'halaman', 'isi']) 

 

    # dfcosim
 
    # dfcosim['isi'][1]


if __name__ == "__main__":
    # text = "الدليل"
    text = "القياس"
    res = getResult(text)
    print("===========================================")
    print(res)