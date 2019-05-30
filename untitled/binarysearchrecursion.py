arr=[2,3,4,10,11]
x=10

def binarysearch(arr,l,r,x):

    if l <= r:
        mid = int((l + r)/2)

        if arr[mid] == x:
            return mid

        elif arr[mid] < x:
             return binarysearch(arr,mid+1,r,x)

        else :
            return binarysearch(arr, l, mid-1, x)
    else :
        return -1

index = binarysearch(arr,0,len(arr)-1,x)
if index == -1:
    print("element not found")
else :
    print(str(x) + " found at index " + str(index))