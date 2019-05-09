#!/usr/bin/python3.6
import sys
import math
from time import time


class MaxHeap:
    
    def __init__(self):    
        self.root = None
        self.insertion_stack = []
        self.score = 0

    def insert(self, value):
        if self.root is None:
            self.root = self.Node(None, value)
            self.last_insertion = self.root
        else:
            parent = self.next_insertion(self.last_insertion)

            if parent.left is None:
                parent.left = self.Node(parent, value)
                self.last_insertion = parent.left
            else:
                parent.right = self.Node(parent, value)
                self.last_insertion = parent.right

            self.upheap(self.last_insertion)
            
        self.insertion_stack.append(self.last_insertion)

    def next_insertion(self,node):
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
        
        return self.next_insertion(node.parent)

    def upheap(self, node):
        if node is not self.root and node > node.parent:
            node.swap(node.parent)
            self.upheap(node.parent)

    def heapify(self, values):
        for value in values:
            self.insert(value)
        return self

    def remove_max(self):
        #Get current max value in root
        
        max_value = self.root.value

        if len(self.insertion_stack) == 1:
            return max_value
    
        #Swap root value with last inserted node
        self.root.swap(self.last_insertion)
        
        self.delete_last_inserted()

        self.sort(self.root)
        
       # self.sort(None,self.root)
        return max_value
    
    def sort(self, node):
        if node.left:
            if node.right:
                if node.left > node and node.left > node.right:
                    node.swap(node.left)
                elif node.right > node and node.right > node.left:
                    node.swap(node.right)
                self.sort(node.left)
                self.sort(node.right)
            else:
                if node.left > node:
                    node.swap(node.left)
                self.sort(node.left)

    def delete_last_inserted(self):
        #Pop current last insertion of stack
        self.insertion_stack.pop()
        # Set child of parent to None
        self.last_insertion.delete()
        if self.insertion_stack:
            self.last_insertion = self.insertion_stack[-1]
        else:
            #Heap is empty
            self.root = None

    def remove_value(self,value):
        #Find first occurrence of value in heap
        frontier = [self.root]

        while frontier:
            node = frontier.pop()
            if node.value == value:
                break
            else:
                if node.left:
                    frontier.append(node.left)
                if node.right:
                    frontier.append(node.right)

        node.swap(self.last_insertion)
        
        self.delete_last_inserted()

        if not self.is_empty():
            self.sort(self.root)
        
    def is_empty(self):
        return self.root is None

    #Max Heap node struct         
    class Node:
        def __init__(self,parent,value):
            self.value = value
            self.parent = parent
            self.left = None
            self.right = None 
        
        def __gt__(self,other):
            return self.value[0] > other.value[0]

        def __lt__(self,other):
            return self.value[0] < other.value[0]

        def __eq__(self,other):
            return self.value[0] == other.value[0]

        def __ne__(self,other):
            return self.value[0] != other.value[0]

        def swap(self,other):
            self.value, other.value = other.value, self.value
        
        def is_left_child(self):
            return self is self.parent.left if self.parent else False
        
        def delete(self):
            if self.parent:
                if self.is_left_child():
                    self.parent.left = None
                else:
                    self.parent.right = None


class PrioritySumDigits(MaxHeap):
    #Override how this class prioritises a nodes value

    class Node(MaxHeap.Node):
        def __eq__(self,other):
            return self.value[0] == other.value[0] and self.value[1] == other.value[1]

        def __ne__(self,other):
            return self.value[0] != other.value[0] and self.value[1] != other.value[1]

        def __gt__(self,other):
            if self.value[1] != other.value[1]:
                return self.value[1] > other.value[1]
            else:
                return self.value[0] > other.value[0]
            
        def __lt__(self,other):
            if self.value[1] != other.value[1]:
                return self.value[1] < other.value[1]
            else:
                return self.value[0] < other.value[0]

def sum_of_digits(val):
    sum = 0
    for n in range(0, int(math.log10(val)+1)):
        sum += ((1 / pow(10,n) * (val % pow(10,n + 1) - (val % pow(10,n)))))
    return int(sum)


def main(input_file):
    with open(input_file) as input_file:
        with open("output.txt",'w') as output_file:
            test_cases = int(input_file.readline().replace("\n", ""))

            for i in range(0, test_cases):
                n, k = input_file.readline().replace("\n","").split(" ")
                n, k = int(n), int(k)

                balls = [(int(i),sum_of_digits(int(i))) for i in input_file.readline().replace("\n","").replace("\t", " ").split(" ")]
                toss_result = input_file.readline().replace("\n","").lower()

                value_priority_player = MaxHeap().heapify(balls)
                digit_sum_priority_player = PrioritySumDigits().heapify(balls)
            
                if toss_result == 'heads':
                    current_player, waiting_player = value_priority_player, digit_sum_priority_player
                elif toss_result == 'tails':
                    current_player, waiting_player = digit_sum_priority_player, value_priority_player

                turns = 0
                while turns < n:
                    #  print(current_player)
                   # print(current_player)
                    value, digit_sum = current_player.remove_max()
                    current_player.score += value
                    waiting_player.remove_value((value,digit_sum))
                    turns+=1

                    if turns % k == 0:
                        current_player, waiting_player = waiting_player, current_player

                output_file.write(f"{str(value_priority_player.score)} {str(digit_sum_priority_player.score)}\n")

if __name__ == "__main__":
    main(sys.argv[1])