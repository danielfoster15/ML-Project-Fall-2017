import csv
import nltk
import string
import re
import random

statuses=[]
comments=[]

#opens status csv 
with open('newshour_facebook_statuses.csv', encoding='utf-8') as f:
	reader = csv.reader(f)
	for row in reader:
		if row != []:
				statuses.append(row)
datapoints = statuses[0]

#opens comments csv
with open('newshour_facebook_comments.csv', encoding='utf-8') as f1:
	reader = csv.reader(f1)
	for row in reader:
		if row != []:
				comments.append(row)

labeledcomments=[]
#labels comments to their corresponding status
for row in comments:
	if row[3] != '[[PHOTO]]':
		labeledcomments.append([row[1], row[3]])
labeledcomments=labeledcomments[1:]

labeledstatuses=[]
#labels each datapoint in the status csv
for row in statuses:
	labeledstatuses.append(list(zip(datapoints, row)))
labeledstatuses=labeledstatuses[1:]
#collects statuses with at least 75% one reaction and classifies them in groups
loveposts=[]
wowposts=[]
hahaposts=[]
sadposts=[]
angryposts=[]

for status in labeledstatuses:
	reacts=int(status[6][1])-int(status[9][1])
	if reacts==0:
		pass
	elif int(status[10][1])/reacts >.744:
		loveposts.append(status)
	elif int(status[11][1])/reacts >.744:
		wowposts.append(status)     
	elif int(status[12][1])/reacts >.744:
		hahaposts.append(status)
	elif int(status[13][1])/reacts >.744:
		sadposts.append(status)
	elif int(status[14][1])/reacts >.744:
		angryposts.append(status)
print(len(loveposts), len(wowposts), len(hahaposts), len(sadposts), len(angryposts))

lovetext=[]
wowtext=[]
hahatext=[]
sadtext=[]
angrytext=[]

for status in loveposts:
	for comment in labeledcomments:
			if status[0][1] == comment[0]:
				lovetext.append(nltk.word_tokenize(comment[1].lower()))

for status in wowposts:
	for comment in labeledcomments:
			if status[0][1] == comment[0]:
				wowtext.append(nltk.word_tokenize(comment[1].lower()))

for status in hahaposts:
	for comment in labeledcomments:
			if status[0][1] == comment[0]:
				hahatext.append(nltk.word_tokenize(comment[1].lower()))


for status in sadposts:
	for comment in labeledcomments:
			if status[0][1] == comment[0]:
				sadtext.append(nltk.word_tokenize(comment[1].lower()))


for status in angryposts:
	for comment in labeledcomments:
			if status[0][1] == comment[0]:
				angrytext.append(nltk.word_tokenize(comment[1].lower()))

commentdata= (lovetext, wowtext, hahatext, sadtext, angrytext)

lovewords=[]
wowwords=[]
hahawords=[]
sadwords=[]
angrywords=[]

puncts = (list(set(string.punctuation)))
puncts.append('photo')
for sentence in lovetext:
	for word in sentence:
		for punct in puncts:
			word=word.replace(punct,"")
		if 'www' not in word and 'http' not in word and word is not None:
				lovewords.append(word)
	lovewords.append('$')
with open('lovewords.txt', 'w', encoding='utf-8') as lovewordfile:
	for word in lovewords:
		if word =='$':
			lovewordfile.write('|  LOV\n')
		else: 
			lovewordfile.write(word+' ')
lovewordfile.close()

for sentence in hahatext:
	for word in sentence:
		for punct in puncts:
			word=word.replace(punct,"")
		if 'www' not in word and 'http' not in word and word is not None:
				hahawords.append(word)
	hahawords.append('$')
with open('hahawords.txt', 'w', encoding='utf-8') as hahawordfile:
	for word in hahawords:
		if word =='$':
			hahawordfile.write('|  HAH\n')
		else: 
			hahawordfile.write(word+' ')
hahawordfile.close()

for sentence in wowtext:
	for word in sentence:
		for punct in puncts:
			word=word.replace(punct,"")
		if 'www' not in word and 'http' not in word and word is not None:
				wowwords.append(word)
	wowwords.append('$')
with open('wowwords.txt', 'w', encoding='utf-8') as wowwordfile:
	for word in wowwords:
		if word =='$':
			wowwordfile.write('|  WOW\n')
		else: 
			wowwordfile.write(word+' ')
wowwordfile.close()

for sentence in sadtext:
	for word in sentence:
		for punct in puncts:
			word=word.replace(punct,"")
		if 'www' not in word and 'http' not in word and word is not None:
				sadwords.append(word)
	sadwords.append('$')
with open('sadwords.txt', 'w', encoding='utf-8') as sadwordfile:
	for word in sadwords:
		if word =='$':
			sadwordfile.write('|  SAD\n')
		else: 
			sadwordfile.write(word+' ')
sadwordfile.close()

for sentence in angrytext:
	for word in sentence:
		for punct in puncts:
			word=word.replace(punct,"")
 		if 'www' not in word and 'http' not in word and word is not None:
 				angrywords.append(word)
 	angrywords.append('$')
 with open('angrywords.txt', 'w', encoding='utf-8') as angrywordfile:
 	for word in angrywords:
 		if word =='$':
 			angrywordfile.write('|  ANG\n')
 		else: 
 			angrywordfile.write(word+' ')
 angrywordfile.close()

 filenames=['lovewords.txt', 'hahawords.txt', 'wowwords.txt', 'sadwords.txt', 'angrywords.txt']
 with open('reactionwords.txt', 'w', encoding='utf-8') as outfile:
     for fname in filenames:
         with open(fname, encoding='utf-8') as infile:
             outfile.write(infile.read())


lines = open('reactionwords.txt', encoding='utf-8').readlines()
random.shuffle(lines)
open('shuffledreactionwords.txt', 'w', encoding='utf-8').writelines(lines)

lovelines=open('lovewords.txt', encoding='utf-8').readlines()
angrylines=open('angrywords.txt', encoding='utf-8').readlines()
sadlines=open('sadwords.txt', encoding='utf-8').readlines()

angrylineslove=angrylines[:len(lovelines)]
angrylinessad=angrylines[:len(sadlines)]



angrylovelines = lovelines+angrylineslove
angrysadlines = sadlines+angrylinessad

# random.shuffle(angrylovelines)
random.shuffle(angrysadlines)
open('shuffledsadangrywords.txt', 'w', encoding='utf-8').writelines(angrysadlines)
# open('shuffledloveangrywords.txt', 'w', encoding='utf-8').writelines(angrylovelines)
