import csv
from sklearn import svm
import numpy as np
import warnings
from sklearn.neural_network import MLPClassifier
warnings.filterwarnings("ignore")
tot=0



#add more 0
#normalization
#0.9->1


# with open('data/enrollment_list.csv') as csvfile:
#     reader=csv.DictReader(csvfile)
#     for row in reader:
#         tot+=1
#         print(row['enrollment_id'],row['course_id'])
#         if tot>10:
#             break

train_index=73000

end_index=73000

pre_index=0
time_feature=[0 for i in range(130000)]
act_feature=[0 for i in range(130000)]
course_number=[0 for i in range(130000)]
class_number=[0 for i in range(130000)]
navigate_f=[0 for i in range(130000)]
access_f=[0 for i in range(130000)]
problem_f=[0 for i in range(130000)]
video_f=[0 for i in range(130000)]
wiki_f=[0 for i in range(130000)]
discussion_f=[0 for i in range(130000)]
page_close_f=[0 for i in range(130000)]



dict = { 'abc': 456 };
dictcourse = { 'abc': 456 };
dictcourse2 = { 'abc': 456 };
#relation userid-courses
with open('data/enrollment_list.csv') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
        index = int(row['enrollment_id'])
        userid=row['user_id']
        courseid=row['course_id']

        if courseid not in dictcourse:
            dictcourse[courseid]=1;
        else:
            dictcourse[courseid]+=1;


        if userid not in dict:
            dict[userid]=1;
        else:
            dict[userid]+=1;

with open('data/enrollment_list.csv') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
        index = int(row['enrollment_id'])
        userid=row['user_id']
        courseid = row['course_id']


        class_number[index]=dictcourse[courseid]
        dictcourse2[index]=userid
        course_number[index]=dict[userid]

label_class=[0 for i in range(130000)]

dict = {'abc': 456};
with open('data/activity_log.csv') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:

        index=int(row['enrollment_id'])
        event=row['event']
        if(event=="navigate"):
            navigate_f[index]+=1
        if (event == "access"):
            access_f[index] += 1
        if (event == "problem"):
            problem_f[index] += 1
        if (event == "video"):
            video_f[index] += 1
        if (event == "wiki"):
            wiki_f[index] += 1
        if (event == "discussion"):
            discussion_f[index] += 1
        if (event == "page_close"):
            page_close_f[index] += 1

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
        pre_index=index




tot=0
label=[0 for i in range(130000)]
dictnum=[0 for i in range(130000)]
dictnum2={'123':23}
with open('data/train_label.csv') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
        index=int(row['enrollment_id'])
        label[index]=int(row['dropout_prob'])
        if(label[index]==1):
            if dictcourse2[index] not in dictnum2:
                dictnum2[dictcourse2[index]] = 1
            else:
                dictnum2[dictcourse2[index]] += 1
            dictnum[class_number[index]]+=1
        tot += 1

with open('data/train_label.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        index = int(row['enrollment_id'])
        class_number[index]=dictnum[class_number[index]]/class_number[index]*10
        tot += 1

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
        #train_X.append([time_feature[i],act_feature[i],course_number[i],class_number[i],problem_f[i],wiki_f[i],video_f[i]])
        train_X.append([time_feature[i], act_feature[i], course_number[i]])
        train_Y.append(label[i])
    else:
        test_X.append([time_feature[i],act_feature[i],course_number[i],class_number[i]])
        test_Y.append(label[i])




tot1=0
tot0=0


with open('data/sum_data.csv','w',newline="") as csvfile:
    fieldnames = ['enrollment_id',"time_feature","act_feature","course_number","problem_f","wiki_f","video_f","discussion","page_close","navigate_f","access_f","class_number","label"]  #72326  -- 120542
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(1, 72000):
        writer.writerow({'enrollment_id':i,"time_feature":time_feature[i],"act_feature":act_feature[i],
                         "course_number":course_number[i],"problem_f":problem_f[i],
                         "wiki_f":wiki_f[i],"video_f":video_f[i],"discussion":discussion_f[i],"page_close":page_close_f[i],"navigate_f":navigate_f[i],"access_f":access_f[i],"class_number":class_number[i],"label":train_Y[i]})
        # if(tot1<20000 and train_Y[i]==1):
        #     writer.writerow({'enrollment_id':i,"time_feature":time_feature[i],"act_feature":act_feature[i],
        #                      "course_number":course_number[i],"class_number":class_number[i],"problem_f":problem_f[i],
        #                      "wiki_f":wiki_f[i],"video_f":video_f[i],"label":train_Y[i]})
        #     tot1+=1
        # if(tot0<20000 and train_Y[i]==0):
        #     writer.writerow({'enrollment_id': i, "time_feature": time_feature[i], "act_feature": act_feature[i],
        #                      "course_number": course_number[i], "class_number": class_number[i],
        #                      "problem_f": problem_f[i],
        #                      "wiki_f": wiki_f[i], "video_f": video_f[i], "label": 0})
        #     tot0+=1


with open('data/test.csv','w',newline="") as csvfile:
    fieldnames = ["time_feature","act_feature","course_number","problem_f","wiki_f","video_f","discussion","page_close","navigate_f","access_f","class_number"]  #72326  -- 120542
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(72326, 120543):
            writer.writerow({"time_feature":time_feature[i],"act_feature":act_feature[i],
                             "course_number":course_number[i],"problem_f":problem_f[i],
                             "wiki_f":wiki_f[i],"video_f":video_f[i],"discussion":discussion_f[i],"page_close":page_close_f[i],"navigate_f":navigate_f[i],"access_f":access_f[i],"class_number":class_number[i]})


