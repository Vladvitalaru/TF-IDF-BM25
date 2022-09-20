#Vlad Vitalaru
#CS 454 Fall 2022
#Assignment 2


import csv 
import math

class TF_IDF():
    def __init__(self, dataFile):
        self.dataFile = dataFile                         #CSV file passed to class object
        self.DocumentCount = 0                           #Total document count in dataFile
        self.TFscores: dict(str, dict(str, int)) = {}    #Dictionary holding TF_IDF values for each term and document
        self.DocumentTerms: dict(str, int) = {}          #Dictionary with # of terms for each document
        self.Index = self.invertedIndex(dataFile)        #Inverted Index of terms within document        

    '''Returns a list of tuples representing the top k results based on tf_idf score'''
    def tf_idf(self, Q, k):
        self.Results = []                                #Final list of documents and their TF_IDF values
        self.Index = self.invertedIndex(self.dataFile)   #Call invertedIndex to reset values on object
        Query = Q.split()
        for term in Query: #Loop over every single term in Query
            if term in self.Index:          #Check the index for the term
                for doc in self.Index[term]:    
                    self.TFscores[doc][term] = self.tfHelper(doc,term)      #Add TF values to dict
                    if Query.count(term) > 1:      #If term occurs multiple times in query, multiply its tf value by the count
                        self.TFscores[doc][term] = self.TFscores[doc][term] * Query.count(term)
                    
        self.TFsummed = self.TFscores.copy()    
        for doc in self.TFsummed:   #Loop through TF scores for each document
            if self.TFsummed[doc]:                      #Only calculated existing scores
                
                for terms in self.TFsummed[doc].keys():   #Loop through every document's term's TF values and apply the relevance function
                    self.TFsummed[doc][terms] = (self.TFsummed[doc][terms]) / (self.numberOfDocuments(terms))  #Update with relevancy score
       
        for doc in self.TFsummed:   #Go through the TF_IDF scores and sum them up for every document 
            if self.TFsummed[doc]:
                self.Results.append(( str(doc) , sum(self.TFsummed[doc].values())))
                
        self.Results.sort(reverse=True,key=lambda y: y[1]) #Sort the TF_IDF scores 
        count = 0
        self.output = []
        while count < k:
            if count < len(self.Results):
                self.output.append(self.Results[count])
                count+=1
            else:
                break

        print(self.output)  #Print and return ranking results
        return self.output
    
    '''Prints TF score, Log( 1 + the number of term occurrences in a document
       divided by the total number of terms in document)
    '''
    def tf(self, d, t):
        if t not in self.Index:
            print("0")
            return 0
        tfscore = math.log( 1 + (self.Index[t][d]/self.DocumentTerms[d]))
        print(tfscore)
        return tfscore
         
    ''' Returns relevance score for a particular query in a document
    '''
    def relevance(self, d, Q):
        self.TFscores[d] = {}
        total = 0
        for term in Q.split():
            if term in self.Index:          #Check the index for the term   
                self.TFscores[d][term] = self.tfHelper(d,term)      #Add TF values to dict
                if Q.count(term) > 1:
                    self.TFscores[d][term] = self.TFscores[d][term] * Q.count(term) #If term is repeated, multiply its TF value
     
        for term in self.TFscores[d]:
            total += self.TFscores[d][term] / self.numberOfDocuments(term)
            
        print(total)
        return total
        
    
    '''Returns TF score, Log( 1 + the number of term occurrences in a document
       divided by the total number of terms in document)
    '''
    def tfHelper(self, d, t):
        return math.log( 1 + (self.Index[t][d]/self.DocumentTerms[d])) 
    
    '''Function which returns an inverted index "Index" for every term in the datafile.
       Also stores the number of terms for each document in dictionary "DocumentTerms"
    '''
    def invertedIndex(self, datafile):
        Index: dict(str, dict(str, int)) = {}
        self.DocumentCount = 0 
        with open(datafile, 'r') as csvFile:   #Open and parse the CSV file
            csvreader = csv.reader(csvFile)
            next(csvreader)
            for document in csvreader:    #Loop every document
                self.DocumentCount += 1        #Increment document count 
                self.TFscores[document[0]] = {}
                self.DocumentTerms[document[0]] = len(document[1].split()) #save the number of terms for each doc
                for term in document[1].split():  #For every term in doc
                    
                    if term not in Index:    #Check if term was seen before
                        Index[term] = {}
                        Index[term][document[0]] = 1   
                    else:
                        if document[0] in Index[term]:      #Check if the term has been seen before in the current doc
                            Index[term][document[0]] += 1
                        else:
                            Index[term][document[0]] = 1
        return Index
    
    '''Returns the number of times a term appears in documents
       Used to divide the TF scores for every term and document
    '''
    def numberOfDocuments(self, term):            
        return len(self.Index[term])    
    

class BM_25():
    def __init__(self, dataFile):
        self.dataFile = dataFile                          #CSV file passed to class object
        self.k1 = 1.2                                     #k1 constant
        self.k2 = 500                                     #k2 constant
        self.b = 0.75                                     #b constant
        self.DocumentCount = 0                            #Total document count in dataFile
        self.DocumentTerms: dict(str, int) = {}           #Dictionary with # of terms for each document
        self.BM25scores: dict(str, dict(str, int)) = {}   #Dictionary holding BM25 values for each term and document
        self.Index = self.invertedIndex(dataFile)         #Inverted Index of terms within document        
        self.AverageDocumentSize = self.AverageDocumentSize(self.DocumentTerms)
    
    '''Returns a list of tuples representing the top k results based on bm25 score'''
    def bm25(self, query, k):
        self.Results = []
        self.Index = self.invertedIndex(self.dataFile)   #Call invertedIndex to reset values on object
        Query = query.split()
        multiples = set(Query)
        for term in Query: #Loop over every single term in Query
            if term in self.Index:          #Check the index for the term
                for doc in self.Index[term]:    
                    if term not in self.BM25scores[doc]:       #If first time term is seen, create score
                        self.BM25scores[doc][term] = self.BMCalculator(term, doc, query)      #Add BM values to dict
                    else:
                        self.BM25scores[doc][term] += self.BMCalculator(term, doc, query) #If term was seen before, add score
            
        for doc in self.BM25scores: #Go through the BM25 scores and sum them up for every document 
            if self.BM25scores[doc]:
                self.Results.append( (str(doc), sum(self.BM25scores[doc].values())))
        
        
        self.Results.sort(reverse=True,key=lambda y: y[1]) #Sort the BM25 scores 
        count = 0
        self.output = []
        while count < k:
            if count < len(self.Results):
                self.output.append(self.Results[count])
                count+=1
            else:
                break 
        print(self.output)
        return self.output
        
    '''Returns the BM25 score for a term, document and query'''
    def BMCalculator(self, term, doc, Query):
        first = math.log( ((self.DocumentCount - len(self.Index[term]) + 0.5) / (len(self.Index[term]) + 0.5)))

        second = ((self.k1 + 1) * self.Index[term][doc]) / (self.k1 * ( (1 - self.b) + self.b * (self.DocumentTerms[doc]/self.AverageDocumentSize)  ) + (self.Index[term][doc]))
                
        third = ((self.k2 + 1) * (Query.count(term))) / (self.k2 + (Query.count(term)))

        return first * second * third
    
    
    '''Returns the average length of all documents'''
    def AverageDocumentSize(self, dict):
        average = []
        for doc in dict:
            average.append(dict[doc])
        return sum(average)/self.DocumentCount
    
    
    '''Function which returns an inverted index "Index" for every term in the datafile.
       Also stores the number of terms for each document in dictionary "DocumentTerms"
    '''
    def invertedIndex(self, datafile):
        Index: dict(str, dict(str, int)) = {}
        self.DocumentCount = 0
        
        with open(datafile, 'r') as csvFile:   #Open and parse the CSV file
            csvreader = csv.reader(csvFile)
            next(csvreader)
            for document in csvreader:               #Loop every document
                self.DocumentCount += 1              #Increment document count 
                self.BM25scores[document[0]] = {}
                self.DocumentTerms[document[0]] = len(document[1].split()) #save the number of terms for each doc
                for term in document[1].split():  #For every term in doc
                    
                    if term not in Index:    #Check if term was seen before
                        Index[term] = {}
                        Index[term][document[0]] = 1   
                    else:
                        if document[0] in Index[term]:      #Check if the term has been seen before in the current doc
                            Index[term][document[0]] += 1
                        else:
                            Index[term][document[0]] = 1
        return Index
    

def main():
    file = "wine.csv"    
    file2 = "winemag-data_first150k.csv"
    Rank = TF_IDF(file)
    
   # Rank.tf_idf("tremendous wine", 3)
   # print()
  #  Rank.tf_idf("tremendous tremendous watson", 3)
    #print()
  #  Rank.tf_idf("the and", 3)
   # print()
   # Rank.tf_idf("and vlad", 3)
   # print()
  #  Rank.tf_idf("US", 5)
    
    #Rank.tf("0", "tremendous")
   # Rank.tf("0", "the")
   # Rank.tf("20", "vlad")
   # Rank.tf("60", "and")
    #Rank.tf("60", "the")

   # Rank.relevance("0", "tremendous")
   # Rank.relevance("2", "mac watson")
   # Rank.relevance("2", "mac mac watson")
   # Rank.relevance("2", "vlad")
   # Rank.relevance("2", "and vlad")

    BM = BM_25(file)
  #  BM.bm25("tremendous", 3)
   # print()
   # BM.bm25("tremendous tremendous", 3)
   # print()
   # BM.bm25("tremendous tremendous watson", 3)
   # print()
   # BM.bm25("mac watson", 3)
   # print()
   # BM.bm25("vlad", 3)
   # print()

   # Rank.tf_idf("tremendous tremendous watson", 3)
   # print()
   # BM.bm25("tremendous tremendous watson", 3)

   # Rank.tf_idf("and the", 3)
   # print()
   # BM.bm25("and the", 3)
   #BM.bm25("tremendous tremendous tremendous watson", 3)
   # Rank.tf_idf("tremendous tremendous tremendous watson", 5)

if __name__ == '__main__':
	main()