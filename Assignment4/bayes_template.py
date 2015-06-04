# Bayes_Classifier
# Author(s) names AND netid's: 
#   Hannah Arntson  hra069
#   Katie George    kmg381
#   Peter Haddad    pbh423
# Date: 2nd May, 2015

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
        # different types of classification. For evaluation we are not including negatives
        if goodProb>badProb:
            return "positive"
        elif badProb>=goodProb:
            return "negative"
#        if log:
#            diff=goodProb-badProb           
#            avg= (goodProb+badProb)/2
#            if verbose:            
#                print "diff:",diff             
#                print "avg:",avg
#            if diff>abs(avg/10) or diff > 2:
#                return "positive"
#            elif diff<(avg/10) or diff < -2:
#                return 'negative'
#            else:
#                return 'neutral'
#        else:
#            if 10*goodProb>badProb:
#                return "positive"
#            elif 10*badProb>goodProb:
#                return "negative"
#            else:
#                return "neutral"
                
      
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

    def tokenize(self, sText, bi=0): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order).
      Has been edited so it can include bigrams, which are inabled by the input."""
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
        """uses N fold clasification to validate the results.
        Splits the data into N groups. The trains on all but one group
        Then tests on the excludeed group"""
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
            precision=[None]*folds
            recall=[None]*folds
            accuracy=[None]*folds
            fmeasure=[None]*folds
            
            for i in range(folds):
                self.goodDict.clear()
                self.badDict.clear()
                self.trainFileName(trainGroups[i])
                results = self.classifyBatch(groups[i])
                for x in results:
                    print x
                trueNeg = float(results[0])
                wrongNeg = float(results[1])
                truePos = float(results[2])
                falsePos = float(results[3])
                positive = float(results[4])
                total = float(results[6])
                precision[i] = truePos/(truePos+falsePos)
                print "precision:",precision[i]
                recall[i] = float(truePos/(truePos+wrongNeg))
                print "recall:",recall[i]                
                accuracy[i] = float((truePos+trueNeg)/(total))
                print "accuracy",accuracy[i]
                fmeasure[i] = float(2*truePos/(2*truePos+falsePos+wrongNeg))
                print "fmeasure",fmeasure[i]
                
            print "Final accuracies"
            print "Precision:",avg(precision)
            print "Recall:", avg(recall)
            print "Accuracy:",avg(accuracy)
            print "Fmeasure",avg(fmeasure)
                
                
                
    def trainFileName(self, files):
        """Alternative training method that takes a list of filenames and then trains on them. Made so we can exclude a test set easily"""
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
        """Calls classify on on files in the list files. Tallys up the results"""
        positive = 0
        negative = 0        
        wrongPos=0
        correctPos=0
        wrongNeg=0
        correctNeg=0
        total = 0
        for fileName in files:
            result=self.classify(self.loadFile("./movies_reviews/"+fileName))
            total+=1            
            if fileName[7]=='1':
                negative+=1
                if result=="positive":
                    wrongNeg+=1
                elif result=="negative":
                    correctNeg+=1
            else:
                positive+=1
                if result=="positive":
                    correctPos+=1
                elif result=="negative":
                    wrongPos+=1
        return [correctNeg, wrongNeg, correctPos, wrongPos,positive,negative,total]
                
                
                
def avg(l):
    """Average of a list"""
    return sum(l)/float(len(l))
                