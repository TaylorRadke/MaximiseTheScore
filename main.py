#!/usr/bin/python3.6
import sys
import math

class MaxHeap:
    
    def __init__(self):    
        self.root = None
        self.insertion_stack = []
        self.score = 0

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

        self.upheap(self.last_insertion)
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

    def upheap(self, node):
        while node is not self.root and node > node.parent:
            node.swap(node.parent)
            node = node.parent

    def downheap(self, node):
        left = node.left
        right = node.right

        if left:
            if right:
                if left > node and left > right:
                    #  print(f"left, swapping {left.value[0]} with {node.value[0]}")
                    node.swap(left)
                    self.downheap(left)
                elif right > node and right > left:
                    #  print(f"right, swapping {right.value[0]} with {node.value[0]}")
                    node.swap(right)
                    self.downheap(right)
            elif not right and left > node:
                #print(f"left, swapping {left.value[0]} with {node.value[0]}")
                node.swap(left)
                self.downheap(left)

    def heapify(self, values):
        for val in values:
            self.insert(val)

    def remove_max(self):
        #Get current max value in root

        max_value = self.root.value
        
        if not self.root.left and not self.root.right:
            self.root = None
            return max_value

        #Swap root value with last inserted node
        self.root.swap(self.last_insertion)
        
        self.delete_last_inserted()

        self.downheap(self.root)
        return max_value
    
    def delete_last_inserted(self):
        #Pop current last insertion of stack
        self.insertion_stack.pop()
        # Set child of parent to None
        self.last_insertion.delete()
        if self.insertion_stack:
            self.last_insertion = self.insertion_stack[-1]
        else:
            self.root = None

    def remove_value(self,value):
        #Find first occurrence of value in heap
        frontier = []
        frontier.append(self.root)

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
            if node is not self.root:
                if node.value > node.parent.value:
                    self.upheap(node)
                else:
                    self.downheap(node) 
            else:
                self.downheap(node)
    
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

        def __eq__(self,other):
            return self.value[0] == other.value[0]

        def __ne__(self,other):
            return self.value[0] != other.value[0]

        def swap(self,other):
            self.value, other.value = other.value, self.value
        
        def is_left_child(self):
            return self is self.parent.left if self.parent else False
        
        def is_right_child(self):
            return self is self.parent.right if self.parent else False
        
        def delete(self):
            if self.parent:
                if self.is_left_child():
                    self.parent.left = None
                elif self.is_right_child():
                    self.parent.right = None


class PrioritySumDigits(MaxHeap):
    #Override how this class prioritises a nodes value
    class Node(MaxHeap.Node):
        def __eq__(self,other):
            return self.value[0] == other.value[0] and self.value[1] == other.value[1]

        def __ne__(self,other):
            return self.value[0] != other.value[0] and self.value[1] != other.value[1]

        def __gt__(self,other):
            if self.value[1] > other.value[1]:
                return True
            elif self.value[1] < other.value[1]:
                return False
            elif self.value[1] == other.value[1]:
                return self.value[0] > other.value[0]

def sum_of_digits(val):
    n_digits = int(math.log(val,10)) + 1
    sum = 0
    for i in range(1,n_digits+1):
        sum += int((val / pow(10,i) - val // pow(10,i)) * 10)
    return sum


if __name__ == "__main__":
    with open(sys.argv[1]) as input_file:
        results = []
        test_cases = int(input_file.readline().replace("\n", ""))

        for i in range(0, test_cases):
            n,k = input_file.readline().replace("\n","").split(" ")
                
            balls = [(int(i),sum_of_digits(int(i))) for i in input_file.readline().replace("\n","").replace("\t", " ").split(" ")]
            toss_result = input_file.readline().replace("\n","").lower()

            value_priority_player = MaxHeap()
            sum_of_digits_priority_player = PrioritySumDigits()

            value_priority_player.heapify(balls)
            sum_of_digits_priority_player.heapify(balls)
            
            if toss_result == 'heads':
                current_player = value_priority_player
                waiting_player = sum_of_digits_priority_player
            elif toss_result == 'tails':
                current_player = sum_of_digits_priority_player
                waiting_player = value_priority_player

            while not current_player.is_empty():
                for _ in range(int(k)):
                    if not current_player.is_empty():
                        value, digit_sum = current_player.remove_max()
                        current_player.score += value
                        waiting_player.remove_value((value,digit_sum))
                    else:
                        break
                current_player, waiting_player = waiting_player, current_player

            results.append((value_priority_player.score, sum_of_digits_priority_player.score))
        with open("output.txt",'w') as output_file:
            for result in results:
                score1, score2 = result
                output_file.write(f"{str(score1)} {str(score2)}\n")

