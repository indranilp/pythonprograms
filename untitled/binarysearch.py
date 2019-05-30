arr=[2,3,4,10,11]
x=10

def binarysearch(arr,l,r,x):

    while l <= r:
        mid = int((l + r)/2)

        if arr[mid] == x:
            return mid

        elif arr[mid] < x:
            l = mid + 1

        else :
            r = mid -1
    return -1

index = binarysearch(arr,0,len(arr)-1,x)
if index == -1:
    print("element not found")
else :
    print(str(x) + "found at index " + str(index))