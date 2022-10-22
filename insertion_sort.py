#Insertion Sort

def insertion_sort(arr):
    indexKey = 1
    while indexKey < len(arr):
        for i in range(indexKey, 0, -1):
            if i-1 < 0:
                break
            while arr[i-1] > arr[i]:
                print("swap happened")
                arr[i-1], arr[i] = arr[i] , arr[i-1]

        indexKey+=1
        print(arr)
l = [6 , 1, 8, 4, 10, 12, 45, 2 , 56 ]
print(l)
insertion_sort(l)
