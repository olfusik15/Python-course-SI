###############FIRST METHOD################################
list1 = [2,4,54,65,13,15,78,233,12,4]
list2 = [3,5,7,9,73,2,463,23,45,12,11,88,111]

def bubbleSort(x):
    n=len(x)
    
    for i in range(n):
        for j in range(0, n-i-1): 
            if x[j]> x[j+1]:
                x[j], x[j+1] = x[j+1], x[j]
                
bubbleSort(list1)

print ("Sorted list 1 is:") 
for i in range(len(list1)): 
    print (list1[i])  
    
###############SECOND METHOD################################    
    
def insertionSort(x):
    for i in range(1, len(x)):
        sample = x[i]
        j = i-1
        while j >= 0 and sample < x[j]:
                x[j + 1] = x[j]
                j-= 1
        x[j + 1] = sample

insertionSort(list2)

print ("Sorted list 2 is:")
for i in range(len(list2)):
    print (list2[i])