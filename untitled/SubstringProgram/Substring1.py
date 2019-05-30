'''perm_identity
Distinct palindromic sub-strings of the given string using Dynamic Programming

Input: str = “abaaa”
Output: 5
Palindromic sub-strings are “a”, “aa”, “aaa”, “aba” and “b”

Input: str = “abcd”
Output: 4
'''

def check_palindrome(str):
    if str == str[::-1]:
        return True
    return False


a="abaaa"
for i in range(0,len(a)):
    j=i+1
    while(j<=len(a)):
        status = check_palindrome(a[i:j])
        if status == True:
            print(a[i:j])
        j=j+1

