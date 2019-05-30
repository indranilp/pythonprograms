class LinkedList:

    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head == None

    def insert(self,item):
        newnode = Node(item)
        newnode.setNext(self.head)
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

    def size(self):
        temp = self.head
        count = 0
        while(temp):
            count = count + 1
            temp = temp.next
        return count

    def search(self,item):
        temp = self.head
        while(temp):
            if(temp.data == item):
                return True
            temp = temp.next
        return False


    def remove(self,item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData()  == item:
                found = True
            else:
                previous = current
                current =current.getNext()
        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())


    def reverse(self):
        current = self.head
        previous = None
        next = current.getNext()
        while(current):
            current.setNext(previous)
            previous = current
            current = next
            if next:
                next = next.getNext()
        self.head = previous

    # Function to reverse the linked list
    def reverse1(self):
        prev = None
        current = self.head
        while(current is not None):
            next = current.next
            current.next = prev
            prev = current
            current = next
        self.head = prev



class Node:

    def __init__(self,initdata):
        self.data =initdata
        self.next = None

    def getData(self):
        return self.data

    def setData(self,newdata):
        self.data = newdata

    def getNext(self):
        return self.next

    def setNext(self,newnext):
        self.next = newnext



mylist = LinkedList()
print(vars(mylist))
print(mylist.isEmpty())
mylist.insert(85)
mylist.insert(5)
mylist.insert(20)
mylist.insert(15)
print(mylist.isEmpty())
mylist.printList()
print(mylist.size())
print(mylist.search(5))
mylist.remove(5)
print(mylist.search(5))
mylist.printList()
mylist.reverse1()
mylist.printList()