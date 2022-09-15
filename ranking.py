#Vlad Vitalaru
#CS 454 Fall 2022
#Assignment 2

import csv 

class TF_IDF():
    def __init__(self, dataFile):
        self.dataFile = dataFile                   #CSV file passed to class object
        self.DocumentCount = 0                     #Total document count in dataFile
        self.TF: dict(str, dict(str, int)) = {}    #DIctionary holding TF values for each term and document
        self.DocumentTerms: dict(str, int) = {}    #Dictionary with # of terms for each document
        self.Index = self.invertedIndex(dataFile)  #Inverted Index 

        
    def tf_idf(self, Q, k):
        Query = Q.split()
        print(Query)
        for term in Query:
            
            for doc in self.Index[term]:
              #  print(doc)
                self.TF[doc][term] = self.tf(doc,term)
       
       # print(self.TF)
       # print(self.Index)
    
    def relevance(self, d , Q):
        
        pass
    
    '''Returns TF score, the number of term occurrences in a document
       divided by the total number of terms in document
    '''
    def tf(self, d, t):
        return self.Index[t][d]/self.DocumentTerms[d] 
    
    '''Function which returns an inverted index "Index" for every term in the datafile.
       Also stores the number of terms for each document in dictionary "DocumentTerms"
    '''
    def invertedIndex(self, datafile):
        Index: dict(str, dict(str, int)) = {}
        
        with open(datafile, 'r') as csvFile:   #Open and parse the CSV file
            csvreader = csv.reader(csvFile)
            next(csvreader)
            for document in csvreader:    #Loop every document
                self.DocumentCount += 1        #Increment document count 
                self.TF[document[0]] = {}
                self.DocumentTerms[document[0]] = len(document[1].split()) #save the number of terms for each document
                for term in document[1].split():  #For every term in document
                    
                    if term in Index:    #Check if term was seen before
                        Index[term][document[0]] =+ 1
                    else:
                        Index[term] = {}
                        Index[term][document[0]] = 1
        return Index
    
                    
    

class BM_25():
    def __init__(self, dataFile):
        
        pass
    
    
    def bm25(self, query, k):
        pass


def main():
    file = "./wine.csv"    
    file2 = "winemag-data_first150k.csv"
    Rank = TF_IDF(file)
    Rank.tf_idf("tremendous the", 3)

if __name__ == '__main__':
	main()