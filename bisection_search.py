def bisection_search(n, arr):
    start = 0
    stop = len(arr)-1
    while True:
        mid = (start + stop)//2
        print(mid)
        if n == arr[mid]:
            print("Found {} in index {}".format(n,mid))
            break
        elif n > arr[mid]:
            start = mid + 1
        else :
            stop = mid - 1

l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

bisection_search(7, l)
