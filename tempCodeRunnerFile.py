import streamlit as st
import pickle
import re
import nltk


nltk.download('punkt')
nltk.download('stopwords')

#loading clf

clf = pickle.load(open('clf.pkl' , 'rb'))
tfidfd = pickle.load(open('tfidf.pkl','rb'))

