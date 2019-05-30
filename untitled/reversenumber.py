num=123
temp=0
while num > 0:
    rem=(num%10)
    num = num //10
    temp = temp *10 + rem
    print(temp)

