#Vlad Vitalaru
#CS 454 Fall 2022
#Assignment 2

from ast import Dict
import csv 

class TF_IDF():
    def __init__(self, dataFile):     
        self.DocumentTerms: dict(str, int) = {}    #Dictionary with # of terms for each document
        self.Index = self.invertedIndex(dataFile)  #Inverted Index obtained from 
              
    def tf_idf(self, Q, k):
        Query = Q.split()
        print(Query)
        pass
    
    def relevance(self, d , Q):
        pass
    
    
    def tf(self, d, t):
        
        pass
    
    '''Function which returns an inverted index "Index" for every term in the datafile.
       Also stores the number of terms for each document in dictionary "DocumentTerms"
    '''
    def invertedIndex(self, datafile):
        Index: dict[str, dict[str, int]] = {}
        
        with open(datafile, 'r') as csvFile:   #Open and parse the CSV file
            csvreader = csv.reader(csvFile)
            next(csvreader)
            for document in csvreader:  #Loop every document
             #   print(document)
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
    Rank.tf_idf("tremendous mac", 3)

    pass

if __name__ == '__main__':
	main()