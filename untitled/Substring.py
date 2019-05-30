a="abcaa"


def substring1(a):
    count = 0
    length = len(a)
    for i in range(0,length):
        j=i+1
        while(j<=length):
            print(a[i:j])
            j=j+1
            count = count + 1
    print(count)




def substring(str,n):
    count1 = 0
    for Len in range(1,n+1):
        for i in range(n-Len + 1):
            j=i+Len-1

            for k in range(i,j+1):
                print(str[k],end="")
            count1 = count1 + 1
            print()
    print(count1)
substring(a,len(a))
substring1(a)
