list1 = ([2,4,54,65,9,13,15,78,233,12,4],14)

def bubbleSort(x):
    n=len(x)
    
    for i in range(n):
        for j in range(0, n-i-1): 
            if x[j]> x[j+1]:
                x[j], x[j+1] = x[j+1], x[j]
                
    return x

def onsets(x):
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
        else:
            break
        
    w=bubbleSort(data)
    w.reverse()
    wynik1=[]
        
    for i in range(3):
        wynik1.append(w[i][1])
        
    return wynik1

print(onsets(list1))