#quicksort


def quicksort(arr):
    '''
    Input: Unsorted list of integers
    Returns sorted list of integers using Quicksort
    Note: This is not an in-place implementation
    '''

    if len(arr) < 2:
        return arr
    else:
        pivot = arr[-1] #choosing pivot
        smaller, equal, larger = [], [] , []
        for num in arr:
            if num < pivot:
                smaller.append(num)
            elif num == pivot:
                equal.append(num)
            else:
                larger.append(num)
    return quicksort(smaller) + equal + quicksort(larger)

l = [6, 8, 1, 4, 10, 7, 8, 9,3, 2, 5]
print(quicksort(l))
