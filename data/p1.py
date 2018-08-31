import csv
from sklearn import svm
import numpy as np
import warnings
warnings.filterwarnings("ignore")
tot=0

# with open('data/enrollment_list.csv') as csvfile:
#     reader=csv.DictReader(csvfile)
#     for row in reader:
#         tot+=1
#         print(row['enrollment_id'],row['course_id'])
#         if tot>10:
#             break

train_index=10000

end_index=10000

pre_index=0
time_feature=[0 for i in range(130000)]
act_feature=[0 for i in range(130000)]
course_number=[0 for i in range(130000)]



dict = { 'abc': 456 };

#relation userid-courses
with open('data/enrollment_list.csv') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
        index = int(row['enrollment_id'])
        userid=row['user_id']
        if userid not in dict:
            dict[userid]=1;
        else:
            dict[userid]+=1;

        if(index>end_index):
            break
with open('data/enrollment_list.csv') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
        index = int(row['enrollment_id'])
        userid=row['user_id']
        course_number[index]=dict[userid]
        if (index > end_index):
            break


dict = {'abc': 456};
with open('data/activity_log.csv') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:

        index=int(row['enrollment_id'])


        #count time
        if(index!=pre_index):
            dict.clear()
        act_time=row['time']
        act_time=act_time[:10]
        if act_time not in dict:
            dict[act_time]=1
            time_feature[index]+=1;


        #count_act
        act_feature[index]+=1;
        if (index > end_index):
            break
        pre_index=index


tot=0
label=[0 for i in range(130000)]
with open('data/train_label.csv') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
        index=int(row['enrollment_id'])
        label[index]=int(row['dropout_prob'])
        tot += 1
        if (index > end_index):
            break
#
# for i in range(50):
#     if(time_feature[i]<3 and label[i]==0):
#         print(i)


train_X=[]
train_Y=[]

test_X=[]
test_Y=[]
for i in range(end_index):
    if (i < train_index):
        train_X.append([time_feature[i],act_feature[i],course_number[i]])
        train_Y.append(label[i])
    else:
        test_X.append([time_feature[i],act_feature[i],course_number[i]])
        test_Y.append(label[i])


for i in range(end_index):
    if(act_feature[i]<3 and train_Y[i]==0):
        print(i)













#
# print("start train")
#
# clf = svm.SVC(probability=True)
# clf.fit(train_X, train_Y)
# #
# # ans=clf.predict_proba([[0,10,1],[1,10,1],[2,10,1],[3,10,1],[4,10,1],[5,10,1],[6,10,1],[99,10,1]])
# # print(ans)
# # tot=0
# # for i in range(end_index-train_index):
# #     pre=clf.predict(test_X[i])
# #     if(pre==test_Y[i]):
# #         tot+=1
# #     else:
# #         print(i)
# #
# # print(tot/(end_index-train_index))
#
#
#
#
#
# text_X=[]
#
# for i in range(72326,120543):
#     test_X.append([time_feature[i],act_feature[i],course_number[i]])
#
#
# tot=0
# print("start predict:")
# # ans=clf.predict_proba([[0],[1],[2],[3],[4],[5],[6],[99]])
# ans=clf.predict_proba(test_X)
# # print(ans[:,1][0])
#
#
# with open('data/sample.csv','w',newline="") as csvfile:
#     fieldnames = ['enrollment_id', 'dropout_prob']  #72326  -- 120542
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#     writer.writeheader()
#
#     for i in range(72326,120543):
#         writer.writerow({'enrollment_id':i, 'dropout_prob':ans[:,1][i-72326]})