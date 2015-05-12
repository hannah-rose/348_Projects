# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re

class Bayes_Classifier:
    goodDict=dict()
    badDict=dict()
    def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
      if (not os.path.isfile("goodDict.pickle") or not os.path.isfile("badDict.pickle")):
          self.train()
      else:
          self.goodDict=self.load("goodDict.pickle")
          self.badDict=self.load("badDict.pickle")

    def train(self):   
       """Trains the Naive Bayes Sentiment Classifier."""
       for files in os.walk("./movies_reviews"):
          for fileNames in files[2]:                
              if fileNames[7]=='1':
                  currDict=self.badDict
              else:
                  currDict=self.goodDict
              tokens=self.tokenize(self.loadFile("./movies_reviews/"+fileNames))
              for token in tokens:
                  if token in currDict:
                      currDict[token]+=1
                  else:
                      currDict[token]=1
       self.save(self.goodDict, "goodDict.pickle")
       self.save(self.badDict, "badDict.pickle")
    
    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """
        numGood=sum(self.goodDict.itervalues())
        numBad=sum(self.badDict.itervalues())
        tokens=self.tokenize(sText)
        goodProb=1.0
        badProb=1.0
        for token in tokens:
            #good prob
            if token in self.goodDict:
                goodProb*= (self.goodDict[token]/float(numGood))
            if token in self.badDict:
                badProb*= (self.badDict[token]/float(numBad))
        print goodProb
        print badProb
                
      
    def loadFile(self, sFilename):
      """Given a file name, return the contents of the file as a string."""

      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
    def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
    def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

    def tokenize(self, sText): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order)."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))
               
      if sToken != "":
         lTokens.append(sToken)

      return lTokens

        