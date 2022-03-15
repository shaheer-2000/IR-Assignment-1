import os
import re
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
			self.docIndex[docID] = set()

		self.docIndex[docID].add(index)

	def getPostings(self, docID = None):
		if docID is None:
			return dict(sorted(self.docIndex.items()))
		else:
			return sorted(self.docIndex[docID])

abstracts = os.listdir('./Assignment-1/Abstracts')
abstractData = {}
termDict = {}
positionalIndex = {}

for abstract in abstracts:
	with open('./Assignment-1/Abstracts/' + abstract, 'r') as f:
		abstractData[abstract.split(sep = '.')[0]] = f.read()

stopWords = []

with open('./Assignment-1/Stopword-List.txt', 'r') as f:
	for s in f:
		s = re.sub(r'[^A-Za-z]', '', s).lower()
		if len(s) > 0:
			stopWords.append(s)

for a in abstractData:
	data = re.sub(r'(-|\n|,)', ' ', abstractData[a])
	data = re.sub(r'\s+', ' ', data).strip()
	cleanedData = re.sub(r'[^A-Za-z\s]', '', data).lower()
	
	tokens = cleanedData.split(' ')

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

q = input()
qq = q.split(' ')
p1 = None
p2 = None
i = 0

queryTokens = []

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

def getUnion(list1, list2):
	return list(set(list1 + list2))

prevPostingList = None

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
		prevPostingList = termDict[stemmer.stem(t)].getPostingList()
		i += 1

print(prevPostingList)
	
	

# print(termDict['where'].getPostingList(), len(termDict['where'].getPostingList()))
# print(positionalIndex['where'].getPostings(), len(positionalIndex['where'].getPostings()))