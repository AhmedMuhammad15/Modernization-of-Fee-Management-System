def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        merge_sort(left)
        merge_sort(right)
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i]['roll_no'] <= right[j]['roll_no']:
                arr[k] = left[i]; i += 1
            else:
                arr[k] = right[j]; j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]; i += 1; k += 1
        while j < len(right):
            arr[k] = right[j]; j += 1; k += 1
    return arr

def binary_search(arr, target_roll):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid]['roll_no'] == target_roll: return mid
        elif arr[mid]['roll_no'] < target_roll: low = mid + 1
        else: high = mid - 1
    return -1