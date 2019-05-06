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

    def upheap(self):
        node = self.last_insertion
        
        while node is not self.root and node.value[0] > node.parent.value[0]:
            node.swap(node.parent)
            node = node.parent

    #Max Heap node struct         
    class Node:
        def __init__(self,parent,value):
            self.value = value
            self.parent = parent
            self.left = None
            self.right = None 
        
        def swap(self,other):
            self.value, other.value = other.value, self.value


class PrioritySumDigits(MaxHeap):
    def upheap(self):
        node = self.last_insertion

        while node is not self.root and node.value[1] >= node.parent.value[1]:
            if node.value[1] > node.parent.value[1] or (node.value[1] == node.parent.value[1] and (node.value[0] > node.parent.value[0])):
                node.swap(node.parent)
            node = node.parent


#TODO: Fix, 1000 not giving 1
def sum_of_digits(val):
    n_digits = int(math.log(val,10)) + 1
    sum = 0
    for i in range(1,n_digits+1):
        sum += int((val / pow(10,i) - val // pow(10,i)) * 10)
    return sum

if __name__ == "__main__":
    
    with open(sys.argv[1]) as input_file:
        test_cases = int(input_file.readline().replace("\n", ""))

        for i in range(0, test_cases):
            n,k = input_file.readline().replace("\n","").split(" ")
                
            balls = [(int(i),sum_of_digits(int(i))) for i in input_file.readline().replace("\n","").replace("\t", " ").split(" ")]
            toss_result = input_file.readline().replace("\n","").lower()

            scott_heap = MaxHeap()
            rusty_heap = PrioritySumDigits()
            for ball in balls:
                scott_heap.insert(ball)
                rusty_heap.insert(ball)
            print(rusty_heap.root.value, max(balls, key = lambda x: x[1]))


