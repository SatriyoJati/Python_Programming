#Selection Sort
#Marker

'''
So lets take a look board marker the board in the algorithm

first element is smaller
'''

l = [6,8,1,4,10,7,8,9,3,2,5]

def selection_sort(arr):
    print("-- selection sort ready to go ---")
    spot_marker = 0;
    print(arr[spot_marker]);
    while(spot_marker < len(arr)):
        for num in range(spot_marker,len(arr)):
            if arr[num] < arr[spot_marker]:
                print('swap candidate found')
                arr[spot_marker], arr[num] = arr[num], arr[spot_marker]
                # print('item swapped')
        spot_marker +=1
        print(arr)



selection_sort(l)
