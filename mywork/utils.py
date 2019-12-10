from collections import Counter
import numpy as np
def checkshape(a):
    print("checking shape:",np.array(a).shape)
def show_repeated(a):
    b = dict(Counter(a))
    print ([key for key,value in b.items()if value > 1])

def fillNoneWithSwappedValue(arr1 ,arr2 ,final1 ,final2 ):
    for a in range(0,arr1.__len__()):
        if final1[a] == None:
            final1[a] = arr2[a]
        if final2[a] == None:
            final2[a] = arr1[a]
    return final1,final2

def indexOf(arr,x):
    for a in range(0,arr.__len__()):
        if arr[a] == x:
            return a
    return -1

def findUnusedIndexValues(parent,offspring):
    res = []
    for a in parent:
        if indexOf(offspring,a) == -1:
            res.append(a)
    return res

import pysnooper
#@pysnooper.snoop()
def crossoverOperator2( parent1, parent2 ):
    if len(parent1) != len(set(parent1)) or len(parent2) != len(set(parent2)):
        print("--------wrong input-------------")
        print("from crossover,error parent!\n",parent1,parent2)
        show_repeated(parent1)
        show_repeated(parent2)
        return
    offspring1 = [None] * parent1.__len__()
    offspring2 = [None] * parent2.__len__()
    i1 = 0
    i2 = 0
    # latestUpdated2 = parent2[0]
    check = 1
    index1 = 0
    BUG = False
    #更新O1
    initalSelected = parent1[0]
    offspring1[i1] = parent2[0]
    i1 += 1
    while i1 < parent1.__len__() and i2 < parent2.__len__():
        #求O2应得哪个元素
        index1 = indexOf(parent1,offspring1[i1-1])
        index1 = indexOf(parent1,parent2[index1])
        latestUpdated2 = parent2[index1]
        offspring2[i2] = latestUpdated2
        i2 += 1

        #如果进入BUG状态
        if offspring1[0]==parent2[0] and offspring2[0] ==parent1[0] and parent1[0]!=parent2[0]:
            #print("Algo Bug!")
            BUG = True
            #修复更新O1
            offspring1[i1] = offspring2[0]
            i1+=1
            #修复更新O2
            offspring2[i2] = offspring1[0]
            i2 += 1
            #构造环
            latestUpdated2 = initalSelected

        #检查是否有环
        if latestUpdated2 == initalSelected:
            check = 0
            res1 = findUnusedIndexValues(parent1,offspring1)
            res2 = findUnusedIndexValues(parent2,offspring2)
            #print("cycle detected,remained parts:",res1,res2)
            if(res1 == [] and res2 == []):
                break
            ans1,ans2 = crossoverOperator2(res1, res2)
            offspring1[i1:] = ans1
            offspring2[i2:] = ans2
            check = 0
            break
        else:#没有进入BUG状态，也没有环
            #更新O1
            index1 = indexOf(parent1,offspring2[i2-1])
            offspring1[i1] = parent2[index1]
            i1 += 1
    if check:
        index1 = indexOf(parent1, offspring1[i1 - 1])
        index1 = indexOf(parent1, parent2[index1])
        latestUpdated2 = parent2[index1]
        offspring2[i2] = latestUpdated2
        i2 += 1
    return offspring1,offspring2






if __name__ == '__main__':
    print("origin paper CX2 case1:")
    p1,p2 = [3,4,8,2,7,1,6,5],[4,2,5,1,6,8,3,7]
    print("p1 = {},p2 = {}".format(p1,p2))
    ans1,ans2 = crossoverOperator2(p1,p2)
    print("o1 = {},o2 = {}".format(ans1,ans2))

    print("origin paper CX2 case2:")
    p1,p2 = [1,2,3,4,5,6,7,8],[2,7,5,8,4,1,6,3]
    print("p1 = {},p2 = {}".format(p1,p2))
    ans1,ans2 = crossoverOperator2(p1,p2)
    print("o1 = {},o2 = {}".format(ans1,ans2))


    p1,p2 = [4,1,2,3,0],[3,4,0,1,2]
    print("my testcase:p1 = {},p2 = {}".format(p1,p2))
    ans1,ans2 = crossoverOperator2(p1,p2)
    print("o1 = {},o2 = {}".format(ans1,ans2))

    from TSP import City,createRoute
    p1 = []
    p2 = []
    for i in range(25):
        p1.append(City(i,i))
    for i in range(1000000000):
        p1 = createRoute(p1)
        p2 = createRoute(p1)
        r  = crossoverOperator2(p1,p2)
        if r == None:
            print("error",p1,p2)
            break
