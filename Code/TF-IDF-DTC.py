from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn import tree
from sklearn.metrics import precision_recall_fscore_support

# Process the first input file and generate tfidf/feature matrix/list
with open('Train (DClean).txt', 'r') as ins1:
    
    array1 = []
    #train_family = []
    for line in ins1:
        #split_line = line.split(' ') # split each line to get the second work which is the family name
        #train_family.append(split_line[2]) # build the family array for classifer
        array1.append(line)
        #print(line)
        
corpus1 = array1

inf1 = open('Train (FClean).txt')
train_family = []
for line in inf1:
    train_family.append(line)    

#print('\n@@@@@@@@@@ BEGIN @@@@@@@@@@@@\n')
#tfidf = TfidfVectorizer(input : string {'C:\Users\200019451\Downloads\Seema Python\try.txt,  'r'})
tfidf1 = TfidfVectorizer()

tfidf_matrix1 = tfidf1.fit_transform(corpus1)

tfidf1_data = tfidf_matrix1.toarray()
#print(tfidf1_data)

features1 = tfidf1.get_feature_names()
#print(features1)

#print('\n@@@@@@@@@@@ END @@@@@@@@@@@@@\n')

#outputFile1 = open(r'Train-TF-IDF.txt', 'w')
#
## write idf matrix to output file
#outputFile1.write("### Begin Matrix\n")
#for item in tfidf1_data.tolist():
#    outputFile1.write("%s\n" % item)
#outputFile1.write("### End Matrix\n")
#
## write feature list to output file
#outputFile1.write("\n### Begin Extracted Feature List\n")
#str1 = ', '.join(features1)
#outputFile1.write(str1)
#outputFile1.write("\n### End Extracted Feature List\n")
#
#outputFile1.close()

ins1.close()
inf1.close()

# Process the second input file and generate tfidf/feature matrix/list
with open('Test (DClean).txt', 'r') as ins2:
    
    array2 = []
    #test_family = []
    for line in ins2:
        #split_line = line.split(' ') # split each line to get the second work which is the family name
        #test_family.append(split_line[2]) # build the family array for classifer
        array2.append(line)
        #print(line)
        
corpus2 = array2

inf2 = open('Train (FClean).txt')
test_family = []
for line in inf2:
    test_family.append(line)

#print('\n@@@@@@@@@@ BEGIN @@@@@@@@@@@@\n')
#tfidf = TfidfVectorizer(input : string {'C:\Users\200019451\Downloads\Seema Python\try.txt,  'r'})
tfidf2 = TfidfVectorizer()

tfidf_matrix2 = tfidf2.fit_transform(corpus2)

tfidf2_data = tfidf_matrix2.toarray()
#print(tfidf2_data)

features2 = tfidf2.get_feature_names()
#print(features2)

#print('\n@@@@@@@@@@@ END @@@@@@@@@@@@@\n')

#outputFile2 = open(r'Test-TF-IDF.txt', 'w')
#
## write idf matrix to output file
#outputFile2.write("### Begin Matrix\n")
#for item in tfidf2_data.tolist():
#    outputFile2.write("%s\n" % item)
#outputFile2.write("### End Matrix\n")
#
## write feature list to output file
#outputFile2.write("\n### Begin Extracted Feature List\n")
#str2 = ', '.join(features2)
#outputFile2.write(str2)
#outputFile2.write("\n### End Extracted Feature List\n")
#
#outputFile2.close()

ins2.close()
inf2.close()

comm_feature_list = list()

for itm1 in features1:
    for itm2 in features2:
        if itm1 == itm2:
            #print "Match found: ", itm1, itm2
            comm_feature_list.append(itm1) # build a list of common features

# calculate the final train and test idf array sizes need to combine features
common_feature_len = len(comm_feature_list)
train_feature_len = len(features1)
test_feature_len = len(features2)
final_array_col = common_feature_len + (train_feature_len - common_feature_len) + (test_feature_len - common_feature_len)
train_array_row = len(train_family)
test_array_row = len(test_family)

train_idf = np.zeros((train_array_row, final_array_col))
test_idf = np.zeros((test_array_row, final_array_col))

# convert the feature lists to array
train_feature_array = np.asarray(features1)
test_feature_array = np.asarray(features2)
comm_feature_array = np.asarray(comm_feature_list)

# copy the common features to the final idf arrays first
train_col_idx = 0
test_col_idx = 0
for comm_ele in comm_feature_array:
    for trainidx, train_ele in enumerate(train_feature_array):
        if comm_ele == train_ele:
            for (i, row) in enumerate(tfidf1_data):
                train_idf[i][train_col_idx] = tfidf1_data[i][trainidx]
            train_col_idx += 1

    for testidx, test_ele in enumerate(test_feature_array):
        if comm_ele == test_ele:
            for (i, row) in enumerate(tfidf2_data):
                test_idf[i][test_col_idx] = tfidf2_data[i][testidx]
            test_col_idx += 1

# now copy the remaining featurs from train and test to final idf arrays 
# so that both train and test array feature order is same
for trainidx, train_ele in enumerate(train_feature_array):
    notfound = 1    
    for comm_ele in comm_feature_array:
        if comm_ele == train_ele:
            notfound = 0
    
    if notfound == 1:
        for (i, row) in enumerate(tfidf1_data):
            train_idf[i][train_col_idx] = tfidf1_data[i][trainidx]
        train_col_idx += 1

for testidx, test_ele in enumerate(test_feature_array):
    notfound = 1    
    for comm_ele in comm_feature_array:
        if comm_ele == test_ele:
            notfound = 0
            
    if notfound == 1:
        for (i, row) in enumerate(tfidf2_data):
            test_idf[i][train_col_idx] = tfidf2_data[i][testidx]
        train_col_idx += 1

# calssify the data using DecisionTreeClassifier
clf = tree.DecisionTreeClassifier()
clf = clf.fit(train_idf, train_family)

a = clf.score(test_idf, test_family)
print "Score: ", a

#x = clf.predict(test_idf[0])
#print "X = ", x    

y_true = np.asarray(test_family)
y_pred = clf.predict(test_idf)

print precision_recall_fscore_support(y_true, y_pred, average='weighted')

# End of program
