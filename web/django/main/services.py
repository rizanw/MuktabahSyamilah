import re
import time
import numpy as np
import unicodedata as ud
from gensim.models import FastText as ft
from pyarabic.araby import strip_tashkeel
from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer


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

  kitab = np.load('./main/data/dataset/kitabsave.npy')
  kitab = kitab.tolist()
  sentence_clear = np.load('./main/data/dataset/sentence_clearsave.npy')
  sentence_clear = sentence_clear.tolist()
  kategori = np.load('./main/data/dataset/kategori.npy')
  kategori = kategori.tolist()
  namakitab = np.load('./main/data/dataset/namakitab.npy')
  namakitab = namakitab.tolist()
  modelFT = ft.load('./main/data/model/modelFT.model')

  # MOST SIMILAR WE
  hasilQE = modelFT.wv.most_similar(text)
  hasilQE = [(strip_tashkeel(''.join(c for c in hasilQE[i][0] if not ud.category(c).startswith('P'))), hasilQE[i][1]) for i in range(len(hasilQE))]
  print(hasilQE)

  #TF-IDF
  tfidf_vectorizer = TfidfVectorizer() 
  
  isikitab=''
  ktb=[]
  for i in range(len(kitab)):
      for j in kitab[i] :
          isikitab = ''.join(kitab[i])
      ktb.append(isikitab)
      
  norm_tf=[]
  for i in range(len(ktb)):
      norm_tfidf = normalizeArabic(ktb[i])
      norm_tf.append(norm_tfidf)

  tfidf_doc = tfidf_vectorizer.fit_transform(norm_tf)
  
  # PIFQvectorizer = CountVectorizer()
  # vectoreTF = PIFQvectorizer.fit_transform(norm_tf)
  # featureTf = PIFQvectorizer.get_feature_names()

  cosim = [] 
  nilaicosim = []
  for i in hasilQE: 
    tes=i[0]
    print(tes)
    tfidf_query = tfidf_vectorizer.transform([tes])
    cos=0.0
    #hitung kedekatan query pada masing masing dokumen 
    cos=cosine_similarity(tfidf_doc,tfidf_query)
    # print(type(cos))
    cosim.append(max(cos))
    nilaicosim.append(cos)

    # countTF = []
    # s = ''.join(c for c in tes if not ud.category(c).startswith('P'))
    # s = strip_tashkeel(s)
    # for k in range(len(featureTf)):
    #   if featureTf[k] == s:
    #     # print(k)
    #     for j in range(vectoreTF.shape[0]):
    #       countTF.append(vectoreTF[j,k])
    # if len(countTF) < 1 :
    #   for j in range(vectoreTF.shape[0]):
    #     countTF.append(0.0)
 
  finaloutput = []
  print("======= hasil Cosim ===========")
  angka = 0
  for i in nilaicosim: 
    for j in range(len(i)):
      if i[j] == cosim[angka]:
        print(kategori[0], '-', namakitab[j], '-', i[j])
        finaloutput.append({'namakitab': namakitab[j], 'kategori': kategori[0]}) 
    angka += 1
  
  return finaloutput 
      