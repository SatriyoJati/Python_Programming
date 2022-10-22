#mergesort

def merge_sorted(arr1,arr2):
    print("Merge function called")
    print(f"lef: {arr1} and right : {arr2}")
    sorted_arr = []
    i, j = 0 , 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            sorted_arr.append(arr1[i])
            i += 1
        else:
            sorted_arr.append(arr2[j])
            j += 1
    while i < len(arr1):
        sorted_arr.append(arr1[i])
        i += 1
    while j < len(arr2):
        sorted_arr.append(arr2[j])
        j += 1
    return sorted_arr

def divide_arr(arr):
    if len(arr) < 2:
        return arr[:]
    else:
        middle = len(arr)//2
        l1 = divide_arr(arr[:middle])
        l2 = divide_arr(arr[middle:])
        print("Left list : {}".format(l1))
        print("Right list : {}".format(l2))
        return merge_sorted(l1,l2)

l1 = [1,4,6,8,10,2,3,5,7,8,9]
l2 = [2,3,5,7,8,9]

print(f"Un-merged list: {divide_arr(l1)}")

#Steps
#ocmpare 1st element in each list and append smaller element
# move marker up by 1 position after smaller number is found
# copy remainnig list once comparisons are complete and ther
# are items still remaining in one of the lists
