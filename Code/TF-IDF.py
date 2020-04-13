from sklearn.feature_extraction.text import TfidfVectorizer

import pickle

#with open(r'C:\Users\200019451\Downloads\Seema Python\try.txt','r') as f:
#   head,sub,auth =filter(None,(f.readline().strip() for i in range(6)))
#   data=f.read()
#    print head,sub,auth,data
  
#with open('CSV_394-510-New.csv', 'r') as ins:
#    
#    array = []
#    for line in ins:
#        array.append(line)
#        print(line)
#        
#corpus = array
  
mfile = open('CSV_394-510-New.csv', 'r') 
  
corpus = mfile.readlines()

#vectorizer = TfidfVectorizer(min_df=1)
#X = vectorizer.fit_transform(corpus)
#print(X.toarray())
#idf = vectorizer._tfidf.idf_
#print dict(zip(vectorizer.get_feature_names(), idf))

#print(vectorizer.get_feature_names() )
#print(X.toarray())

print('\n@@@@@@@@@@ BEGIN @@@@@@@@@@@@\n')
#tfidf = TfidfVectorizer(input : string {'C:\Users\200019451\Downloads\Seema Python\try.txt,  'r'})
tfidf = TfidfVectorizer()

tfidf_matrix = tfidf.fit_transform(corpus)

tfidf_data = tfidf_matrix.toarray()
print(tfidf_data)
#tfidf_matrix._check_vocabulary()

features = tfidf.get_feature_names()
print(features)

print('\n@@@@@@@@@@@ END @@@@@@@@@@@@@\n')

outputFile = open(r'TFIDF_11-15.txt', 'w')

# write idf matrix to output file
outputFile.write("### Begin Matrix\n")
for item in tfidf_data.tolist():
    outputFile.write("%s\n" % item)
outputFile.write("### End Matrix\n")

# write feature list to output file
outputFile.write("\n### Begin Extracted Feature List\n")
str = ', '.join(features)
outputFile.write(str)
outputFile.write("\n### End Extracted Feature List\n")

outputFile.close()

ins.close()

# End of program
