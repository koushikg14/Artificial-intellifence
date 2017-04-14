import csv
import math
import operator
def euclideandist(instance1,instance2,length):
    distance=0
    for i in range(length):
        distance += pow((instance1[i] - instance2[i]), 2)
    return math.sqrt(distance)

def neighbours(i_d,temperature,humidity,light,co2,occ,test,k):
    distances=[]
    length=len(test)-1
    for i in range(len(temperature)):
        instance1=[]
        instance1.append(temperature[i])
        instance1.append(humidity[i])
        instance1.append(light[i])
        instance1.append(co2[i])
        dist=euclideandist(instance1,test,length)
        instance1.append(i_d[i])
        instance1.append(occ[i])
        instance1.append(dist)
        distances.append((instance1,dist))
    distances.sort(key=operator.itemgetter(1))
    neighbours=[]
    for x in range(k):
        neighbours.append(distances[x][0])
    neighbours.append(distances[len(distances)-1][0])
    return neighbours

def neighbours1(i_d,temperature,humidity,light,co2,occ,test,k,a,b):
    distances=[]
    length=len(test)-1
    for i in range(len(temperature)):
        if (a-i>0 and b-i>0) or (a-i<0 and b-i<0):
            instance1=[]
            instance1.append(temperature[i])
            instance1.append(humidity[i])
            instance1.append(light[i])
            instance1.append(co2[i])
            dist=euclideandist(instance1,test,length)
            instance1.append(i_d[i])
            instance1.append(occ[i])
            instance1.append(dist)
            distances.append((instance1,dist))
    distances.sort(key=operator.itemgetter(1))
    neighbours=[]
    for x in range(k):
        neighbours.append(distances[x][0])
    neighbours.append(distances[len(distances)-1][0])
    return neighbours
def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)-1):
        response = neighbors[x][5]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]
def getResponseWeights(neighbors):
    x=len(neighbors)
    classVotes={}
    max_dist=neighbors[x-1][6]
    min_dist=neighbors[0][6]
    diff=max_dist-min_dist
    for i in range(x-1):
        response=neighbors[i][5]
        weight=float(max_dist-neighbors[i][6])/float(diff)
        if response in classVotes:
            classVotes[response]+=weight
        else:
            classVotes[response]=weight
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

def standard_deviation(errors,mean,n):
	sum1=0
	for i in errors:
		sum1+=(i-mean)^2
	sd=float(sum1)/float(n)
	return sd
train_id=[]
train_temperature=[]
train_humidity=[]
train_light=[]
train_co2=[]
train_occupancy=[]
m=1
with open('train.csv', 'rb') as csvfile:
    lines = csv.reader(csvfile)
    for row in lines:
        if m==1:
            m+=1
            continue
        train_id.append(int(row[0]))
        train_temperature.append(float(row[2]))
        train_humidity.append(float(row[3]))
        train_light.append(float(row[4]))
        train_co2.append(float(row[5]))
        train_occupancy.append(int(row[7]))
m=1
test_id=[]
test_temperature=[]
test_humidity=[]
test_light=[]
test_co2=[]
test_occupancy=[]
with open('test.csv', 'rb') as csvfile:
    lines = csv.reader(csvfile)
    for row in lines:
        if m==1:
            m+=1
            continue
        test_id.append(int(row[0]))
        test_temperature.append(float(row[2]))
        test_humidity.append(float(row[3]))
        test_light.append(float(row[4]))
        test_co2.append(float(row[5]))
        test_occupancy.append(int(row[7]))


print "Starting 3-fold cross validation"
#3-fold cross validation
new_len=len(train_id)/3
error_list={}
smallest_k={}
sd={}
for i in range(3):
    for j in range(1,10):
        k=j
        a=i*new_len
        b=a+new_len
        errors=[]
        for sets in range(a,b):
            testInstance=[]
            testInstance.append(train_temperature[sets])
            testInstance.append(train_humidity[sets])
            testInstance.append(train_light[sets])
            testInstance.append(train_co2[sets])
            testInstance.append(train_occupancy[sets])
            neighbors = neighbours1(train_id,train_temperature,train_humidity,train_light,train_co2,train_occupancy, testInstance,k,a,b)
            response = getResponse(neighbors)
            err=abs(response-train_occupancy[sets])
            if err>0:
            	errors.append(err)
        mean=float(reduce(lambda x, y: x + y, errors))
        error_list[j]+=mean
    key=min(error_list,key=error_list.get)
    value=error_list[key]
    smallest_k[key]=value
    #sum1=reduce(lambda x, y: x + y, error_list)
    #sum1/=float(3)
    #result.append(sum1)
k=min(smallest_k, key=smallest_k.get)
print "k value=%d"%(k)
print "For test set1:"
count=0
for sets in range(len(test_occupancy)):
    testInstance=[]
    testInstance.append(test_temperature[sets])
    testInstance.append(test_humidity[sets])
    testInstance.append(test_light[sets])
    testInstance.append(test_co2[sets])
    testInstance.append(test_occupancy[sets])
    neighbors = neighbours(train_id,train_temperature,train_humidity,train_light,train_co2,train_occupancy, testInstance,k)
    response = getResponseWeights(neighbors)
    if response!=test_occupancy[sets]:
        count+=1
print "For weighted k-nn:"
print count
print "Accuracy= %fpercent"%(100.0-(float(count)/float(len(test_occupancy)))*100.0)
count=0
for sets in range(len(test_occupancy)):
    testInstance=[]
    testInstance.append(test_temperature[sets])
    testInstance.append(test_humidity[sets])
    testInstance.append(test_light[sets])
    testInstance.append(test_co2[sets])
    testInstance.append(test_occupancy[sets])
    neighbors = neighbours(train_id,train_temperature,train_humidity,train_light,train_co2,train_occupancy, testInstance,k)
    response = getResponse(neighbors)
    if response!=test_occupancy[sets]:
        count+=1
print "For normal k-nn:"
print count
print "Accuracy= %fpercent"%(100.0-(float(count)/float(len(test_occupancy)))*100.0)
print "For test set2:"
m=1
with open('test1.csv', 'rb') as csvfile:
    lines = csv.reader(csvfile)
    for row in lines:
        if m==1:
            m+=1
            continue
        test_id.append(int(row[0]))
        test_temperature.append(float(row[2]))
        test_humidity.append(float(row[3]))
        test_light.append(float(row[4]))
        test_co2.append(float(row[5]))
        test_occupancy.append(int(row[7]))
count=0
for sets in range(len(test_occupancy)):
    testInstance=[]
    testInstance.append(test_temperature[sets])
    testInstance.append(test_humidity[sets])
    testInstance.append(test_light[sets])
    testInstance.append(test_co2[sets])
    testInstance.append(test_occupancy[sets])
    neighbors = neighbours(train_id,train_temperature,train_humidity,train_light,train_co2,train_occupancy, testInstance,k)
    response = getResponseWeights(neighbors)
    if response!=test_occupancy[sets]:
        count+=1
print "For weighted k-nn:"
print count
print "Accuracy= %fpercent"%(100.0-(float(count)/float(len(test_occupancy)))*100.0)
count=0
for sets in range(len(test_occupancy)):
    testInstance=[]
    testInstance.append(test_temperature[sets])
    testInstance.append(test_humidity[sets])
    testInstance.append(test_light[sets])
    testInstance.append(test_co2[sets])
    testInstance.append(test_occupancy[sets])
    neighbors = neighbours(train_id,train_temperature,train_humidity,train_light,train_co2,train_occupancy, testInstance,k)
    response = getResponse(neighbors)
    if response!=test_occupancy[sets]:
        count+=1
print "For normal k-nn:"
print count
print "Accuracy= %fpercent"%(100.0-(float(count)/float(len(test_occupancy)))*100.0)
        
