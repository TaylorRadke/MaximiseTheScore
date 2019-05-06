#!/usr/bin/python3.6
import sys
import math

class Queue(list):
    def enq(self,value):
        self.insert(0,value)
    
    def dq(self):
        return self.pop()

    def empty(self):
        return len(self) == 0

class MaxHeap:
    def __init__(self):
        self.size = 0
        self.root = None
    
    def isEmpty(self):
        return self.size == 0

    def get_root(self):
        return self.root

    def add_node(self, value):
        if not self.root:
            self.root = self.Node(self, value)
            return

        next_insertion = self.find_next_insertion()
        if next_insertion:
            print(next_insertion.value, value)
            if not next_insertion.left:
                next_insertion.left = self.Node(next_insertion,value)
            else:
                next_insertion.right = self.Node(next_insertion, value)
    
    def find_next_insertion(self):
        q = Queue()
        q.enq(self.root)

        while not q.empty():
            node = q.dq()
            if node.left == None or node.right == None:
                return node
            else:
                q.enq(node.left)
                q.enq(node.right)

    # Virtual method to be overriden by each player class based on how they plau
    def heapify(self):
        pass
            
                
    class Node:
        def __init__(self,parent,value):
            self.value = value
            self.parent = parent
            self.left = None
            self.right = None 


def sum_of_digits(val):
    n_digits = int(math.log(val,10)) + 1
    sum = 0
    for i in range(1,n_digits+1):
        sum += int((val / pow(10,i) - val // pow(10,i)) * 10)
    return sum

if __name__ == "__main__":

    heap = MaxHeap()
    
    # with open(sys.argv[1]) as input_file:
    #     test_cases = input_file.readline().replace("\n", "")

    #     for i in range(0, int(test_cases)):
    #         n,k = input_file.readline().replace("\n","").split(" ")
    #         balls = [(int(i),sum_of_digits(int(i))) for i in input_file.readline().replace("\n","").replace("\t", " ").split(" ")]
    #         toss_result = input_file.readline().replace("\n","").lower()
