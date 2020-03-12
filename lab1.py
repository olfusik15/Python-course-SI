list1 = [2,4,54,65,13,15,78,233,12,]
def bubbleSort(x):
    n=len(x)
    
    for i in range(n):
        for j in range(0, n-i-1): 
            if x[j]> x[j+1]:
                x[j], x[j+1] = x[j+1], x[j]
                
bubbleSort(list1)

print ("Sorted list is:") 
for i in range(len(list1)): 
    print (list1[i])  