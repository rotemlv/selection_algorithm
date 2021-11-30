from random import randint

MINIMUM_SIZE = 30  # arrays under this size will simply get sorted during the selection algorithm
ARRAY_SIZE = 100
MIN_ARRAY_VAL = 0
MAX_ARRAY_VAL = 100

_TEST_QUICKSORT = True
_TEST_SELECT = False


def random_array(size=ARRAY_SIZE, start=MIN_ARRAY_VAL,end=MAX_ARRAY_VAL):
    return [randint(start, end) for _ in range(size)]


def partial_sort(array, start, end):
    # sort the part array[start:end+1] (as to include both start and end index)
    array[start:end+1] = sorted(array[start:end+1])


def check_if_sorted(array):
    n = len(array)
    flag = True
    i = 0
    while i < n-1 and flag:
        flag = array[i] <= array[i + 1]  # verify proper order
        i += 1
    return flag


def median(array, start, end):
    if end - start + 1 < MINIMUM_SIZE:
        partial_sort(array, start,end)
        return array[start + (end-start)//2]
    # find median of medians and recursively call this to find the index
    # find median of medians by splitting array to n/5 arrays and sort each,
    small_arrays = [sorted(array[i:i+5]) for i in range(start,end,5)]
    # print(small_arrays)
    # find median of each
    pivots = [arr[(len(arr)-1) // 2] for arr in small_arrays]
    # print(pivots)
    return median(pivots, 0 , len(pivots) - 1)


def partition(array, low, high, pivot_index):
    # swaps pivot to end and applies partitioning as defined in quicksort, modified code from geeksforgeeks
    array[pivot_index], array[high] = array[high],  array[pivot_index]
    i = low - 1  # index of smaller element
    pivot = array[high]  # pivot
    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if array[j] <= pivot:
            # increment index of smaller element
            i = i + 1
            array[i], array[j] = array[j], array[i]
    # final swap, pivot is at its final position
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1


def select(array, start, end, i):
    if start == end:
        return array[start]
    x = median(array, start, end)
    q = partition(array, start, end, array.index(x))
    k = q - start + 1
    if i == k:
        return array[q]
    else:
        return select(array, start, q-1, i) if i < k else select(array, q+1, end,i - k)


def deterministic_quick_sort(array, start, end):
    # uses median of medians method to find a "good" pivot (not close to the edges)
    if start < end:
        # get pivot with median:
        pivot_elem = median(array, start, end)
        # find pivot index and swap with the end
        piv = array.index(pivot_elem)
        # partition using the pivot:
        piv = partition(array, start, end, piv)
        # and work on the edges
        deterministic_quick_sort(array, start, piv - 1)
        deterministic_quick_sort(array, piv + 1, end)


for _ in range(1000):
    arr = random_array(size=1000, start=0, end=1000)
    if _TEST_SELECT:
        if select(arr, 0, len(arr) - 1, len(arr) // 2) != sorted(arr)[(len(arr) // 2) - 1]:
            print("error in selection algorithm")
            print(f"{select(arr, 0, len(arr) - 1, len(arr) // 2)}, {sorted(arr)[(len(arr) // 2) - 1]}")
    if _TEST_QUICKSORT:
        arr2 = sorted(arr)
        deterministic_quick_sort(arr,0, len(arr) - 1)
        if arr != arr2:  # mind the lack of stability if used with custom objects
            print("error in sorting algorithm")
            print(arr)
            print(arr2)


#print(sorted(array))

# quick_sort(array, 0, len(array)-1)
# if check_if_sorted(array):
#     print(f"sorted successfully")
# else:
#     print(array)


# def partitionff(array, start, end, pivot_index):
#     # array is passed and indices we work on include both start and end
#     # swap pivot to end
#     array[pivot_index], array[end] = array[end],  array[pivot_index]
#     # find place for pivot
