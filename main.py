#!/usr/bin/python3.6
import sys
import math

class MaxHeap:
    
    def __init__(self):    
        self.root = None
        self.insertion_stack = []

    def insert(self, value):
        if not self.root:
            self.root = self.Node(None, value)
            self.last_insertion = self.root
        else:
            parent = self.next_insertion()

            if not parent.left:
                parent.left = self.Node(parent, value)
                self.last_insertion = parent.left
            else:
                parent.right = self.Node(parent, value)
                self.last_insertion = parent.right

        self.upheap()
        self.insertion_stack.append(self.last_insertion)
    
    def next_insertion(self):
        node = self.last_insertion

        while True:
            if node is self.root:
                while node.left:
                    node = node.left
                return node

            if node.is_left_child():
                if node.parent.right:
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

    def downheap(self, node):
        left = node.left
        right = node.right

        if left:
            if right:
                if left.value[0] > node.value[0] or right.value[0] > node.value[0]:
                    if left.value[0] > right.value[0]:
                      #  print(f"left, swapping {left.value[0]} with {node.value[0]}")
                        node.swap(left)
                        self.downheap(left)
                    elif right.value[0] > left.value[0]:
                      #  print(f"right, swapping {right.value[0]} with {node.value[0]}")
                        node.swap(right)
                        self.downheap(right)
            else:
                if left.value[0] > node.value[0]:
                    #print(f"left, swapping {left.value[0]} with {node.value[0]}")
                    node.swap(left)
                    self.downheap(left)
            

    def heapify(self, values):
        for val in values:
            self.insert(val)

    def remove_max(self):
        #Get current max value in root

        max_value = self.root.value
        
        if self.last_insertion is self.root:
            return max_value

        #Swap root value with last inserted node
        self.root.swap(self.last_insertion)

        #Pop current last insertion of stack
        self.insertion_stack.pop()

        # Set child of parent to None
        if self.last_insertion.is_left_child():     self.last_insertion.parent.left = None
        elif self.last_insertion.is_right_child():  self.last_insertion.parent.right = None

        self.last_insertion = self.insertion_stack[-1]

        self.downheap(self.root)
        return max_value

    #Max Heap node struct         
    class Node:
        def __init__(self,parent,value):
            self.value = value
            self.parent = parent
            self.left = None
            self.right = None 
        
        def swap(self,other):
            self.value, other.value = other.value, self.value
        
        def is_left_child(self):
            return self is self.parent.left if self.parent else False
        
        def is_right_child(self):
            return self is self.parent.right if self.parent else False



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

            value_priority_player = MaxHeap()
            sum_of_digits_priority_player = PrioritySumDigits()

            value_priority_player.heapify(balls)

            for _ in balls:
                print(value_priority_player.remove_max())



            print("=" * 30)


