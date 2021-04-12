# python3


import math

class Heap():

    def __init__(self, data, size):
        self.data = data
        self.size = size
        self.swaps = []
    
    # for zero-based indexing
    # left_child of node[i] = 2i + 1
    # right child of node[i] = 2i + 2
    # parent of node[i] = round_up(i/2) - 1

    def get_parent(self, i):
        index = math.ceil(i/2) - 1
        return index if index > 0 and index < self.size else i

    def get_left_child(self, i):
        index = 2*i + 1
        return index if index < self.size else i

    def get_right_child(self, i):
        index = 2*i + 2
        return index if index < self.size else i

    def swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
        self.swaps.append((i, j))

    def sift_down(self, i):
        # to sift a node down in min heap, check that it is strictly greater than any of its children. 
        # If both are >, swap it with the greater of the 2 children
        # If one of them are >, swap with that child
        # If neither are >, do nothing
        node = self.data[i]
        left_child = self.get_left_child(i)
        right_child = self.get_right_child(i)
        

        if node > self.data[left_child] and node > self.data[right_child]:

            if self.data[left_child] <= self.data[right_child]:
                j =  left_child

            else:
                j = right_child

            self.swap(i, j)
            self.sift_down(j)
        
        elif node > self.data[left_child]:
            j = left_child
            self.swap(i, j)
            self.sift_down(j)
        
        elif node > self.data[right_child]:
            j = right_child
            self.swap(i, j)
            self.sift_down(j)

    
    # to build a min heap from an array, sift down all nodes from the top to second-last layer (nodes i = n/2 to 1, n = len(array))
    def build_heap(self):
        for i in range(self.size//2, -1, -1):
            self.sift_down(i)


def main():
    n = int(input())
    data = list(map(int, input().split()))
    assert len(data) == n

    heap = Heap(data, len(data))
    heap.build_heap()
    

    print(len(heap.swaps))
    for i, j in heap.swaps:
        print(i, j)


if __name__ == "__main__":
    main()
   
