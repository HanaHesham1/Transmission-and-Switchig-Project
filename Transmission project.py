import math
import numpy as np
blockingprobability=0.001
totalnoofslots=8
slotsperuser=2
numberofchannelspercluster = 125
citysize = 450  # in Km2
noofsubscribers=1000000#number of subscribers per city
avgcallperuser = 10 #calls per day
avgcallduration = 1  # in minutes
InterfaceRation=6.25
def fact(n):  
    return 1 if (n==1 or n==0) else n * fact(n - 1);  

def erlang(A, m):
    L = (A ** m) / fact(m)
    sum_ = 0
    for n in range(m + 1): sum_ += (A ** n) / fact(n)
    block=(L / sum_)
    return block 
    
    
def getacell(block_prob, trunks):
    left = 0
    right = 1000

    # Perform binary search to find the minimum offered load with the desired blocking probability
    while True:
        mid = (left + right) / 2
        b = erlang(mid, trunks)
        if abs(b - block_prob) < 0.0001:
            return mid
        elif b > block_prob:
            right = mid
        else:
            left=mid
def nocells():
    erlang_per_user=avgcallperuser*avgcallduration/(24*60)
    minimum_reuse_factor=math.ceil(InterfaceRation*6/3)
    trunks=math.ceil(numberofchannelspercluster*totalnoofslots/(slotsperuser*minimum_reuse_factor))
    acell=getacell(blockingprobability,trunks)
    noofsubscribersperuser=math.floor(acell/erlang_per_user)
    cellsNS=math.ceil(noofsubscribers/noofsubscribersperuser)
    #return(math.ceil(noofsubscribers/noofsubscribersperuser))
    N =[3,4,7,9,12,13]
    n60 = [2,1,1,1,1,1]
    n120 =[3,2,2,2,2,2]
    n180=[4,3,3,3,3,3]
    X=3*minimum_reuse_factor/6
    t60=0
    i=0
    while(t60<X):
        t60=3*N[i]/n60[i]
        i=i+1
        if(t60>X):
            N60=N[i]
            n60=n60[i]
        if(i==6):
            break
    t120=0
    i=0
    while(t120<X):
         t120=3*N[i]/n120[i]
         i=i+1
         if(t120>X):
             N120=N[i]
             n120=n120[i]
         if(i==6):
             break 
    t180=0
    i=0
    while(t180<X):
         t180=3*N[i]/n180[i]
         i=i+1
         if(t180>X):
             N180=N[i]
             n180=n180[i]
         if(i==6):
             break    
    #Ntotal=[N60,N120,N180]
    Nsubscribers=[]
    trunks60=math.ceil(numberofchannelspercluster*totalnoofslots/(slotsperuser*N60))
    trunks120=math.ceil(numberofchannelspercluster*totalnoofslots/(slotsperuser*N120))
    trunks180=math.ceil(numberofchannelspercluster*totalnoofslots/(slotsperuser*N180))   
    Acell60=getacell(blockingprobability,math.ceil(trunks60/6))
    Acell120=getacell(blockingprobability,math.ceil(trunks120/3))
    Acell180=getacell(blockingprobability,math.ceil(trunks180/2))
    Nsubscriber60= math.floor(Acell60*6/erlang_per_user)
    Nsubscriber120= math.floor(Acell120*3/erlang_per_user)
    Nsubscriber180= math.floor(Acell180*2/erlang_per_user)
    Nsubscribers.append(Nsubscriber60)
    Nsubscribers.append(Nsubscriber120)
    Nsubscribers.append(Nsubscriber180)
    print(np.max(Nsubscribers))
    Y=np.max(Nsubscribers)
    nocellsmax=math.ceil(noofsubscribers/Y)
    return("Number of cells without sectoring: "+str(cellsNS)+" Number of cells with sectoring with maximum number of subscribers :"+str(nocellsmax))
    