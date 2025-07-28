class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        node = Node(data)
        if self.head:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = node
        else:
            self.head = node

    def __str__(self):
        curr = self.head
        s = ""
        while curr:
            s = s + str(curr.data) + "->"
            curr = curr.next
        else:
            s = s + "X"
        return s       

if __name__ == "__main__":
    l1 = LinkedList()
    l1.append(1)
    l1.append(2)
    l1.append(3)
    l1.append(4)
    l1.append(5)
    l1.append(6)           

    print(l1) 