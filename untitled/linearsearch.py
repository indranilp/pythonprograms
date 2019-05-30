arr=[2,3,4,10,11]
x=10

def search(arr,x):
    for i in range(0,len(arr)):
        if arr[i] == x:
            return i
    else :
        return -1

index = search(arr,x)
if index == -1:
    print("element not found")
else :
    print(str(x) + "found at index " + str(index))