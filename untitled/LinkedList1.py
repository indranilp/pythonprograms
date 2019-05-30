# Print nth node from last/reverse/

class Node:

    def __init__(self,data):
        self.data = data
        self.next = None


class LinkedList:

    def __init__(self):
        self.head = None

    #create ndoe and make linked list

    def push(self,data):
        newnode = Node(data)
        newnode.next = self.head
        self.head = newnode

    # Utility function to print the linked LinkedList
    def printList(self):
        temp = self.head
        list = ""
        while (temp):
            list = list + str(temp.data)
            if temp.next != None:
                list = list + "-->"
            temp = temp.next
        print(list)

    # Function to reverse the linked list
    def reverse(self):
        prev = None
        current = self.head
        while(current is not None):
            next = current.next
            current.next = prev
            prev = current
            current = next
        self.head = prev

    # Function to get the nth node from
    # the last of a linked list
    def printNthFromLast(self, n):
        temp = self.head  # used temp variable

        length = 0
        while temp is not None:
            temp = temp.next
            length += 1

        # print count
        if n > length:  # if entered location is greater
            # than length of linked list
            print('Location is greater than the' +
                  ' length of LinkedList')
            return
        temp = self.head
        for i in range(0, length - n):
            temp = temp.next
        print(temp.data)



llist = LinkedList()
llist.push(10)
llist.push(20)
llist.push(30)
llist.push(80)
llist.push(40)
llist.printList()
llist.reverse()
llist.printList()
llist.printNthFromLast(4)

