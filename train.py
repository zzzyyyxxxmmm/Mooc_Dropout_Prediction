import csv
from sklearn import svm
import numpy as np
import warnings
from sklearn.neural_network import MLPClassifier
import math
warnings.filterwarnings("ignore")

tot_num=34856
feature_num=11
train_X=[]
train_Y=[]

test_X=[]
test_Y=[]

tot=0

train_num=70000
test=[]
fieldnames = ["time_feature", "act_feature", "course_number", "problem_f",
                  "wiki_f", "video_f", "discussion","page_close","navigate_f","access_f","class_number","label"]
with open('data/data_norm.csv') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
        if(tot<train_num):
            train_X.append([float(row[fieldnames[i]]) for i in range(feature_num)])
            train_Y.append(int(row[fieldnames[feature_num]]))
        else:
            test_X.append([float(row[fieldnames[i]]) for i in range(feature_num)])
            test_Y.append(int(row[fieldnames[feature_num]]))
        tot+=1

# train_X=np.array(train_X).dot(100)
# train_X=np.ndarray.tolist(train_X)
#
# test_X=np.array(test_X).dot(100)
# test_X=np.ndarray.tolist(test_X)


print("start_train")
clf = MLPClassifier(solver='adam',learning_rate='adaptive', learning_rate_init =0.0001,hidden_layer_sizes=(1500,),early_stopping=True)
clf.fit(train_X,train_Y)

print("train end")




#
# ans=clf.predict_proba(test_X)
#
# loss=0
# for i in range(tot_num-train_num):
#     for j in range(2):
#         loss += math.log(ans[:, j][i]) * (test_Y[i] == j)
# print(-1*loss/(tot_num-train_num))
#






tot=0
test=[]
with open('data/test_norm.csv') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
        test.append([float(row[fieldnames[i]]) for i in range(feature_num)])

# test=np.array(test).dot(100)
# test=np.ndarray.tolist(test)


print("start predict:")
ans=clf.predict_proba(test)


with open('data/sample.csv','w',newline="") as csvfile:
    fieldnames = ['enrollment_id', 'dropout_prob']  #72326  -- 120542
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for i in range(72326,120543):
        writer.writerow({'enrollment_id': i, 'dropout_prob': ans[:, 1][i - 72326]})

#
# with open('data/check.csv','w',newline="") as csvfile:
#     fieldnames2 = ['enrollment_id',"time_feature", "act_feature", "course_number", "class_number", "problem_f",
#                   "wiki_f", "video_f", "dropout_prob"]
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames2)
#
#     writer.writeheader()
#
#     for i in range(72326,120543):
#         writer.writerow({'enrollment_id':i,"time_feature": test[i-72326][0], "act_feature": test[i-72326][1],
#                          "course_number": test[i-72326][2],"dropout_prob":ans[:, 1][i - 72326]})