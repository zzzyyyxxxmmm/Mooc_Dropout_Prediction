import csv
from sklearn import svm
import numpy as np
import warnings
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
import numpy as np
warnings.filterwarnings("ignore")
tot=0
tot_num=70000
features_num=11

features=[]
test_features=[]
label=[]
fieldnames = ["time_feature", "act_feature", "course_number", "problem_f",
                  "wiki_f", "video_f", "discussion","page_close","navigate_f","access_f","class_number","label"]
with open('data/sum_data.csv') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
        sub=[]
        for i in range(features_num):
            sub.append(float(row[fieldnames[i]]))
        label.append(int(row[fieldnames[features_num]]))
        features.append(sub)
X = np.array(features)
X_normalized = preprocessing.normalize(X, axis=0,norm='l2')
X_normalized*=100
X_normalized=np.array(X_normalized)


with open('data/data_norm.csv','w',newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    tot=0
    for row in X_normalized:
        writer.writerow({"time_feature": row[0], "act_feature": row[1],
                         "course_number": row[2],
                         "problem_f": row[3],
                         "wiki_f": row[4], "video_f": row[5],"discussion":row[6],"page_close":row[7],"navigate_f":row[8] ,"access_f":row[9],"class_number":row[10],"label": label[tot]})
        tot+=1




with open('data/test.csv') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
        sub=[]
        for i in range(features_num):
            sub.append(int(row[fieldnames[i]]))
            test_features.append(sub)
X = np.array(test_features)
X_normalized = preprocessing.normalize(X, axis=0,norm='l2')
X_normalized*=100
X_normalized=np.array(X_normalized)



with open('data/test_norm.csv','w',newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    tot=0
    for row in X_normalized:
        writer.writerow({"time_feature": row[0], "act_feature": row[1],
                         "course_number": row[2],
                         "problem_f": row[3],
                         "wiki_f": row[4],"video_f": row[5],"discussion":row[6],"page_close":row[7],"navigate_f":row[8],"access_f":row[9],"class_number":row[10]})
        tot+=1



