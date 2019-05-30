arr=[7,9,5,1,11]

for i in range(0,len(arr)):
    for j in range(i+1,len(arr)):
        if arr[i] > arr[j]:
            arr[i],arr[j] = arr[j],arr[i]
        print(arr)
    print("==================")

print(arr)


