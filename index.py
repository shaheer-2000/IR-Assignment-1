import os
import re
from turtle import pos
from nltk.stem.porter import *

stemmer = PorterStemmer()

class Node:
	def __init__(self):
		self.docFreq = 0
		self.postingList = []
	
	def addPosting(self, docID):
		if int(docID) not in self.postingList:
			self.postingList.append(int(docID))
			self.docFreq += 1

	def getPostingList(self):
		return sorted(self.postingList)

class PositionalNode:
	def __init__(self):
		self.docIndex = {}
	
	def addPosting(self, docID, index):
		docID = int(docID)

		if docID not in self.docIndex:
			self.docIndex[docID] = list()

		if index not in self.docIndex[docID]:
			self.docIndex[docID].append(index)
			self.docIndex[docID] = sorted(self.docIndex[docID])

	def getPostings(self, docID = None):
		if docID is None:
			return dict(sorted(self.docIndex.items()))
		else:
			return sorted(self.docIndex[docID])

# DOCS_PATH = "./Assignment-1/Abstracts"
DOCS_PATH = "./Assignment-1-Updated/CricketReviews/Dataset"
STOPWORDS_PATH = "./Assignment-1-Updated/Stopword-List.txt"
abstracts = os.listdir(DOCS_PATH)
abstractData = {}
termDict = {}
positionalIndex = {}

for abstract in abstracts:
	with open(DOCS_PATH + "/" + abstract, 'r') as f:
		abstractData[abstract.split(sep = '.')[0]] = f.read()

stopWords = []

with open(STOPWORDS_PATH, 'r') as f:
	for s in f:
		s = re.sub(r'[^A-Za-z]', '', s).lower()
		if len(s) > 0:
			stopWords.append(s)

for a in abstractData:
	data = re.sub(r'(-|\n|,)', ' ', abstractData[a])
	data = re.sub(r'\s+', ' ', data).strip()
	cleanedData = re.sub(r'[^A-Za-z\s]', '', data).lower()
	
	tokens = cleanedData.split(' ')
	# if a == "1":
		# print(len(tokens), list(set(tokens)))

	for index, token in enumerate(tokens):
		token = stemmer.stem(token)

		if len(token) <= 0:
			continue

		if token in stopWords:
			if token not in positionalIndex:
				positionalIndex[token] = PositionalNode()
			
			positionalIndex[token].addPosting(a, index)

			continue
		
		if token not in termDict:
			termDict[token] = Node()
		
		if token not in positionalIndex:
			positionalIndex[token] = PositionalNode()

		termDict[token].addPosting(a)
		positionalIndex[token].addPosting(a, index)
	
	# if a == "1":
	# 	print(len(termDict.keys()), list(set(termDict.keys())))

def diffDoc(list1):
	list2 = []
	for i in range(1, 449):
		if i in list1:
			continue

		list2.append(i)
	return list2

def getIntersect(list1, list2):
	intersectedList = []

	i = 0
	j = 0

	while i < len(list1) and j < len(list2):
		if list1[i] < list2[j]:
			i += 1
		elif list1[i] > list2[j]:
			j += 1
		else:
			intersectedList.append(list1[i])
			i += 1
			j += 1

	return intersectedList

def getPostingByPosition(term1, term2, pNum):
	p1 = positionalIndex[term1].getPostings()
	p2 = positionalIndex[term2].getPostings()
	list1 = list(p1.keys())
	list2 = list(p2.keys())

	intersectedList = []

	i = 0
	j = 0
	ii = 0
	jj = 0

	while i < len(list1) and j < len(list2):
		if list1[i] < list2[j]:
			i += 1
		elif list1[i] > list2[j]:
			j += 1
		else:
			while ii < len(p1[list1[i]]) and jj < len(p2[list2[j]]):
				diff = p1[list1[i]][ii] - p2[list2[j]][jj]
				# print(diff, list1[i], p1[list1[i]], p2[list2[j]])
				if diff > 0 and diff <= pNum:
					intersectedList.append(list1[i])
					# print('DD')
					break
				elif diff > 0:
					jj += 1
				else:
					ii += 1
			
			ii = 0
			jj = 0
			i += 1
			j += 1

	return intersectedList

def getUnion(list1, list2):
	return list(set(list1 + list2))

while (True):
	q = input()
	if q == "q":
		break
	qq = q.split(' ')
	p1 = None
	p2 = None
	i = 0
	prevPostingList = None

	queryTokens = []
	while (i < len(qq)):
		t = qq[i]

		if t == "NOT":
			prevPostingList = diffDoc(termDict[stemmer.stem(qq[i + 1])].getPostingList())
			i += 2
		elif t == "AND":
			prevPostingList = getIntersect(prevPostingList, termDict[stemmer.stem(qq[i + 1])].getPostingList())
			i += 2
		elif t == "OR":
			prevPostingList = getUnion(prevPostingList, termDict[stemmer.stem(qq[i + 1])].getPostingList())
			i += 2
		else:
			# p q \2 OR p
			# p AND p q \2 -> evaluate p q \2 first, then p AND result of p q \2
			# if consecutive token, assume proximity
			prevPostingList = termDict[stemmer.stem(t)].getPostingList()
			if (i + 1) < len(qq) and qq[i + 1] != "NOT" and qq[i + 1] != "AND" and qq[i + 1] != "OR":
				wordsForProxQuery = []
				while (i < len(qq) and not qq[i][0] == "/"):
					wordsForProxQuery.append(qq[i])
					i += 1

				# /2 means at max 2 words b/w terms, (0) neural (1) x (2) y (3) information
				proximity = int(qq[i][1:]) + 1 # /2 => 2

				k = 0
				while k < len(wordsForProxQuery):
					cPostingList = getPostingByPosition(stemmer.stem(wordsForProxQuery[k]), stemmer.stem(wordsForProxQuery[k + 1]), proximity)
					k += 2
					if prevPostingList is None:
						prevPostingList = cPostingList
					else:
						prevPostingList = getIntersect(prevPostingList, cPostingList)

			i += 1

	print(prevPostingList)
	
	

# print(termDict['where'].getPostingList(), len(termDict['where'].getPostingList()))
# print(positionalIndex['where'].getPostings(), len(positionalIndex['where'].getPostings()))