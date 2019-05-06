#!/usr/bin/python3.6
import sys
import math

class MaxHeap:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = self.Node(None, value)
            self.last_insertion = self.root
        else:
            insertion = self.next_insertion()

            if not insertion.left:
                insertion.left = self.Node(insertion, value)
                self.last_insertion = insertion.left
            else:
                insertion.right = self.Node(insertion, value)
                self.last_insertion = insertion.right
            self.upheap()
    
    def next_insertion(self):
        node = self.last_insertion

        while True:
            if node is self.root:
                while node.left:
                    node = node.left
                return node

            if node is node.parent.left:
                if not node.parent.right:
                    return node.parent

                node = node.parent.right
                while node.left:
                    node = node.left
                return node
            node = node.parent


    # Virtual method to be overriden by each player class based on how they plau
    def upheap(self):
        pass

    #Max Heap node struct         
    class Node:
        def __init__(self,parent,value):
            self.value = value
            self.parent = parent
            self.left = None
            self.right = None 
        
        def swap(self,other):
            tmp_node = other
            self = other
            other = tmp_node


def sum_of_digits(val):
    n_digits = int(math.log(val,10)) + 1
    sum = 0
    for i in range(1,n_digits+1):
        sum += int((val / pow(10,i) - val // pow(10,i)) * 10)
    return sum

if __name__ == "__main__":

                    #         1
                    #     2       3
                    #   4  5    6   7

    heap = MaxHeap()


    # with open(sys.argv[1]) as input_file:
    #     test_cases = input_file.readline().replace("\n", "")

    #     for i in range(0, int(test_cases)):
    #         n,k = input_file.readline().replace("\n","").split(" ")
    #         balls = [(int(i),sum_of_digits(int(i))) for i in input_file.readline().replace("\n","").replace("\t", " ").split(" ")]
    #         toss_result = input_file.readline().replace("\n","").lower()
