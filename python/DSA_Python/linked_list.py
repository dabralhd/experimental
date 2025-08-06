from typing import Any
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def insert_next(self, node, data):
        new_node = Node(data)
        node.next = new_node

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, data):
        node = Node(data)
        if self.head:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = node
        else:
            self.head = node
        self.size = self.size + 1

    def pop_last(self) -> Any:
        curr = self.head
        data = None
        if not curr:
            return
        
        if not curr.next:
            self.head = None
            data = curr.data
        else:
            prev = curr
            curr = curr.next
            while curr.next:
                curr = curr.next
                prev = prev.next
            data = curr.data
            prev.next = None

        self.size = self.size - 1
        return data    

    def to_list(self):
        ret = []
        curr = self.head
        while curr:
            ret.append(curr.data)
            curr = curr.next
        return ret

    def __str__(self):
        curr = self.head
        s = ""
        while curr:
            s = s + str(curr.data) + "->"
            curr = curr.next
        else:
            s = s + "X"
        return s   

def make_ll(arr: list[int]) -> Node:
    '''
    although we dan use helper LinkedList class defined above for inserting new nodes,
    however for practice purpose using bare Node class

    '''
    first = Node()

    for val in arr:
        second = first.insert_next(val)
        second = second.next
    return first.next

# if __name__ == "__main__":
#     l1 = LinkedList()
#     l1.append(1)
#     l1.append(2)
#     l1.append(3)
#     l1.append(4)
#     l1.append(5)
#     l1.append(6)           

#     print(l1)

#     while l1.head:
#         print(f'size: {l1.size}, value: {l1.pop_last()}')