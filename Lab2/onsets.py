list1 = ([2,4,54,65,9,13,15,78,233,12,4],14)
list2 = ([3,5,7,9,73,2,463,23,45,12,11,88,111], 3)

def bubbleSort(x):
    n=len(x)
    
    for i in range(n):
        for j in range(0, n-i-1): 
            if x[j]> x[j+1]:
                x[j], x[j+1] = x[j+1], x[j]
                
    return x

def insertionSort(x):
    for i in range(1, len(x)):
        sample = x[i]
        j = i-1
        while j >= 0 and sample < x[j]:
                x[j + 1] = x[j]
                j-= 1
        x[j + 1] = sample
    return x

def onsets_bubble(x):
    values = x[0]
    threshold = x[1]
    count = 0
    data = []
    
    for i in range(len(values)):
        if count < 3:
            if values[i] > threshold:
                cache = []
                cache.append(values[i])
                cache.append(i)
                data.append(cache)
                count += 1
      
    w=bubbleSort(data)
    w.reverse()
    wynik1=[]
        
    for i in range(3):
        wynik1.append(w[i][1])
        
    return wynik1

def onsets_insertion(x):
    values = x[0]
    threshold = x[1]
    count = 0
    data = []
    
    for i in range(len(values)):
        if count < 3:
            if values[i] > threshold:
                cache = []
                cache.append(values[i])
                cache.append(i)
                data.append(cache)
                count += 1
     
    w=insertionSort(data)
    w.reverse()
    wynik1=[]
        
    for i in range(3):
        wynik1.append(w[i][1])
        
    return wynik1

print("onsets bubble list1", onsets_bubble(list1))
print("onsets insertion list1", onsets_insertion(list1))
print("onsets insertion list2", onsets_insertion(list2))