# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re

class Bayes_Classifier:
    goodDict=dict()
    badDict=dict()
    def __init__(self, train=0):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
      if (not os.path.isfile("goodDict.pickle") or not os.path.isfile("badDict.pickle") or train==1):
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
                  otherDict=self.goodDict
              else:
                  currDict=self.goodDict
                  otherDict=self.badDict
              tokens=self.tokenize(self.loadFile("./movies_reviews/"+fileNames))
              for token in tokens:
                  if token in currDict:
                      currDict[token]+=1
                  else:
                      currDict[token]=1
                  if token not in otherDict:
                      otherDict[token]=0
       for key in self.goodDict:
           self.goodDict[key]+=1
       for key in self.badDict:
           self.badDict[key]+=1
       self.save(self.goodDict, "goodDict.pickle")
       self.save(self.badDict, "badDict.pickle")
       
    
    
    def classify(self, sText, verbose=0):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """
        #defines if we use logs or normals
        log=1
        numGood=sum(self.goodDict.itervalues())
        numBad=sum(self.badDict.itervalues())
        tokens=self.tokenize(sText)
        if log:
            goodProb=0
            badProb=0
        else:
            goodProb=1.0
            badProb=1.0
        for token in tokens:
            if log:
                if token in self.goodDict:
                    goodProb+= math.log(self.goodDict[token]/float(numGood))
                if token in self.badDict:
                    badProb+= math.log(self.badDict[token]/float(numBad))
            else:
                if token in self.goodDict:
                    goodProb*= (self.goodDict[token]/float(numGood))
                if token in self.badDict:
                    badProb*= (self.badDict[token]/float(numBad))
        if verbose:
            print goodProb
            print badProb
        
        if log:
            diff=goodProb-badProb           
            avg= (goodProb+badProb)/2
            if verbose:            
                print "diff:",diff             
                print "avg:",avg
            if diff>abs(avg/10) or diff > 5:
                return "positive"
            elif diff<(avg/10) or diff < -5:
                return 'negative'
            else:
                return 'neutral'
        else:
            if 10*goodProb>badProb:
                return "positive"
            elif 10*badProb>goodProb:
                return "negative"
            else:
                return "neutral"
                
      
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

    def tokenize(self, sText, bi=1): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order)."""
      #include two word strings
      if (bi):
          lTokens = []
          last = ""
          sToken = ""
          for c in sText:
             if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
                sToken += c
             else:
                if sToken != "":
                    if last!= "":                    
                        lTokens.append(last+" "+sToken)                    
                    last=sToken
                    lTokens.append(sToken)
                    sToken = ""
                if c.strip() != "":
                   lTokens.append(str(c.strip()))
                   
          if sToken != "":
             lTokens.append(sToken)
      else:
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

    def validate(self, folds=10):
        for stuff in os.walk("./movies_reviews"):
            files=stuff[2]
            numFiles=len(files)
            foldSize=numFiles/folds
            groups=[]
            for i in range(folds):
                groups.append(files[i*foldSize:(i+1)*foldSize])
            trainGroups=[None]*10
            for i in range(folds):
                 trainGroups[i]=[]
                 for exclusion in range(folds):
                     if exclusion!=i:
                         trainGroups[i]+=groups[exclusion]
            for i in range(folds):
                self.trainFileName(trainGroups[i])
                results=self.classifyBatch(groups[i])
                print "Correct:",results[0],". Wrong:",results[1]
                


    def trainFileName(self, files):
        for fileNames in files:                
          if fileNames[7]=='1':
              currDict=self.badDict
              otherDict=self.goodDict
          else:
              currDict=self.goodDict
              otherDict=self.badDict
          tokens=self.tokenize(self.loadFile("./movies_reviews/"+fileNames))
          for token in tokens:
              if token in currDict:
                  currDict[token]+=1
              else:
                  currDict[token]=1
              if token not in otherDict:
                  otherDict[token]=0
        for key in self.goodDict:
           self.goodDict[key]+=1
        for key in self.badDict:
           self.badDict[key]+=1       
            
    def classifyBatch(self, files):
        wrong=0
        correct=0
        for fileName in files:
            result=self.classify(self.loadFile("./movies_reviews/"+fileName))
            if fileName[7]=='1':
                if result=="positive":
                    wrong+=1
                elif result=="negative":
                    correct+=1
            else:
                if result=="positive":
                    correct+=1
                elif result=="negative":
                    wrong+=1
        return [correct, wrong]
                
                
                
                
                