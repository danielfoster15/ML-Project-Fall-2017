#imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import accuracy_score, confusion_matrix
from nltk import *
from nltk.util import ngrams
import math
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt


#opens sentences and sentiment scores and returns a zipped list of sentence and score

def openfile(comments):
	f= open(comments, "r", encoding='utf-8')
	sentences=[]
	scores=[]
	for line in f:
		sentence = line.split('|')
		sentences.append(sentence[0])
		scores.append(sentence[1])
	f.close()

	sentencescores=list(zip(sentences,scores))
	sentencescores.sort(key=lambda x: len(x[0]))
	return(sentencescores)



#produces tfidf matrix for entire dataset
def Tfidf(sentencescores):
	totalsentiments=[i[1] for i in sentencescores]
	scaler=StandardScaler()

	trainvectorizer = TfidfVectorizer(tokenizer=word_tokenize, stop_words='english', norm="l2")
	totaltfidf=trainvectorizer.fit_transform(i[0] for i in sentencescores)
	feature_names = trainvectorizer.get_feature_names()
	matrix=totaltfidf.todense()
	scaler.fit_transform(matrix)
	df=pd.DataFrame(matrix, columns=feature_names)
	return(df, totalsentiments)

def Tfidfbigram(sentencescores):
	trainbigramvectorizer = TfidfVectorizer(tokenizer=word_tokenize, ngram_range=(2,2), stop_words='english', norm="l2")
	totalsentimentsbigrams=[i[1] for i in sentencescores]
	scaler=StandardScaler()
	totaltfidf=trainbigramvectorizer.fit_transform(i[0] for i in sentencescores)
	feature_names = trainbigramvectorizer.get_feature_names()
	matrix=totaltfidf.todense()
	scaler.fit_transform(matrix)
	dfbigrams=pd.DataFrame(matrix, columns=feature_names)
	return(dfbigrams, totalsentimentsbigrams)

#feature reduction
def featureselection(df, totalsentiments):
	print('Original Feature Amount: ', len(df.transpose()))
	sfm = SelectFromModel(linclf, threshold=.275)
	reduced = sfm.fit(df, totalsentiments)
	matrixdf = reduced.transform(df)
	feature_idx = sfm.get_support()
	feature_name = df.columns[feature_idx]
	matrixdf=pd.DataFrame(matrixdf, columns=list(feature_name))
	print('Reduced Feature Amount: ', len(matrixdf.transpose()))
	tfidfmax=0
	topwords= matrixdf.sum().sort(ascending=False, inplace=False)
	print('Top twenty five tfidf words/bigrams:\n', topwords[:25])
	return(matrixdf, list(feature_name))

#train test split
def traintest(matrixdf, totalsentiments):
	trainsents=matrixdf[:int(.8*len(matrixdf))]
	trainsentiments=totalsentiments[:int(.8*len(totalsentiments))]
	testsents=matrixdf[int(.8*len(matrixdf)):]
	testsentiments=totalsentiments[int(.8*len(totalsentiments)):]
	return(trainsents, trainsentiments, testsents, testsentiments)

#model definitions

linclf=LinearSVC()
linclfbigrams=LinearSVC()

#execute 
file='shuffledsadangrywords.txt'
sentencescores=openfile(file)
df, totalsentiments = Tfidf(sentencescores)

matrixdf, featurenames=featureselection(df, totalsentiments)
trainsents, trainsentiments, testsents, testsentiments = traintest(matrixdf, totalsentiments)

dfbigrams, totalsentimentsbigrams = Tfidfbigram(sentencescores)
matrixdfbigrams, featurenamesbigrams=featureselection(dfbigrams, totalsentimentsbigrams)
trainsentsbigrams, trainsentimentsbigrams, testsentsbigrams, testsentimentsbigrams = traintest(matrixdfbigrams, totalsentimentsbigrams)

model1 = linclf.fit(trainsents, trainsentiments)
model2 = linclfbigrams.fit(trainsentsbigrams, trainsentimentsbigrams)
testpredictions1 = model1.predict(testsents)
testpredictions2 = model2.predict(testsentsbigrams)

print(accuracy_score(testsentiments, testpredictions1))
print(confusion_matrix(testsentiments, testpredictions1))

print(accuracy_score(testsentiments, testpredictions2))
print(confusion_matrix(testsentiments, testpredictions2))