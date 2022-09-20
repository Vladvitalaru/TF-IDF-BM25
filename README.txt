Vlad Vitalaru
CS 454 HW2 - TF_IDF and BM25

The code will be imported and 4 given functions are tested:

tf_idf(self, Q, k):

relevance(self, d, Q):

tf(self, d, t):

bm25(self, query, k):


Besides these functions, I have added a few additional helper methods:

tfHelper(self, d, t):
-method which assists with tf values inside tf_idf() method. This method only returns the tf score and does not print it like the tf() method.

invertedIndex(self, datafile):
-method which builds out the directories holding information such as an inverted index, and tf & bm25 scores.

numberOfDocuments(self, term):
-method simply returning the number of documents a term appears in.

BMCalculator(self, term, doc, Query):
-returning the BM25 score for a specific document, term and query.

AverageDocumentSize(self, dict):
-returns the average size of all documents in the dictionary 

