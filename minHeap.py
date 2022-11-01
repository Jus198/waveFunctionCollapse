"""
Ian Barber,Alex Woodring, Max Huang, and Angelo Savich
Project 8 - Heaps - Solution Code
CSE 331 Spring 2022

"""
from typing import List, Tuple, Any


class MinHeap:
    """
    Partially completed data structure. Do not modify completed portions in any way
    """
    __slots__ = ['data']

    def __init__(self):
        """
        Initializes the priority heap
        """
        self.data = []

    def __str__(self) -> str:
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self.data)

    __repr__ = __str__

    def to_tree_format_string(self) -> str:
        """
        Prints heap in Breadth First Ordering Format
        :return: String to print
        """
        string = ""
        # level spacing - init
        nodes_on_level = 0
        level_limit = 1
        spaces = 10 * int(1 + len(self))

        for i in range(len(self)):
            space = spaces // level_limit
            # determine spacing

            # add node to str and add spacing
            string += str(self.data[i]).center(space, ' ')

            # check if moving to next level
            nodes_on_level += 1
            if nodes_on_level == level_limit:
                string += '\n'
                level_limit *= 2
                nodes_on_level = 0
            i += 1

        return string

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   Modify below this line

    def __len__(self) -> int:
        """
        Returns number of elements in minheap
        :return: int
        """
        return len(self.data)

    def empty(self) -> bool:
        """
        Returns true if minheap is empty
        :return: Boolean
        """
        return len(self.data) == 0

    def top(self) -> int:
        """
        Returns smallest value in the minheap
        :return: int val, or None
        """
        if len(self.data) > 0:
            return self.data[0]
        return None

    def get_left_child_index(self, index: int) -> int:
        """
        Returns the left child's index, or None if the child doesn't exist
        :param index: index we are getting child from
        :return: int, or None
        """
        new_index = index * 2 + 1
        if new_index > len(self.data) - 1:
            return None
        return new_index

    def get_right_child_index(self, index: int) -> int:
        """
        Returns the right child's index, or None if the child doesn't exist
        :param index: index we are getting child from
        :return: int, or None
        """
        new_index = index * 2 + 2
        if new_index > len(self.data) - 1:
            return None
        return new_index

    def get_parent_index(self, index) -> int:
        """
        Returns the parent's index
        :param index: index we are using to calculate parent
        :return: int index of parent
        """
        if index == 0:
            return None
        index -= 1
        if index % 2 == 1:
            index -= 1
        return index//2

    def get_min_child_index(self, index: int) -> int:
        """
        Finds the minimum child of index and returns the child's index
        :param index: index we are searching for children from
        """
        if index is None:
            return None

        left = self.get_left_child_index(index)
        right = self.get_right_child_index(index)

        if left is None:
            return None

        if right is None:
            return left

        if self.data[left] < self.data[right]:
            return left
        return right

    def percolate_up(self, index: int) -> None:
        """
        Brings a small value from the bottom of the heap to the top recursively
        :param index: index of value being brought up
        """
        parent_index = self.get_parent_index(index)
        if parent_index is not None:
            if self.data[index] < self.data[parent_index]:
                self.data[index], self.data[parent_index] = self.data[self.get_parent_index(index)], self.data[index]
                self.percolate_up(parent_index)

    def percolate_down(self, index: int) -> None:
        """
        Brings a value down in the minheap until it is in the correct spot
        :param index: index of value we are bringing down
        """
        min_child = self.get_min_child_index(index)
        if min_child is None:
            return
        if self.data[index] > self.data[min_child]:
            self.data[index], self.data[min_child] = self.data[min_child], self.data[index]
            self.percolate_down(min_child)
            return

    def push(self, val: int) -> None:
        """
        Adds new value to the minheap
        :param val: val of new item in minheap
        """
        self.data.append(val)
        self.percolate_up(len(self.data)-1)
        return

    def pop(self) -> int:
        """
        Removes lowest value from minheap
        :return: lowest value in minheap, or None
        """
        last = self.data.pop()
        if len(self.data) > 0:
            ret = self.data[0]
            self.data[0] = last
            self.percolate_down(0)
            return ret
        return last


    #def lower_priority(self, ):

class MaxHeap:
    """
    Partially completed data structure. Do not modify completed portions in any way
    """
    __slots__ = ['data']

    def __init__(self):
        """
        Initializes the priority heap
        """
        self.data = MinHeap()

    def __str__(self):
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self.data.data)

    __repr__ = __str__

    def __len__(self):
        """
        Length override function
        :return: Length of the data inside the heap
        """
        return len(self.data)

    def print_tree_format(self):
        """
        Prints heap in bfs format
        """
        self.data.to_tree_format_string()

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   Modify below this line

    def empty(self) -> bool:
        """
        Boolean for if the maxheap is empty
        :return: boolean, true if empty
        """
        return len(self.data.data) == 0

    def top(self) -> int:
        """
        Returns the highest value in the maxheap, doesn't remove
        :return: int, highest value in maxheap
        """
        if self.empty():
            return None
        return -1 * self.data.top()

    def push(self, key: int) -> None:
        """
        Adds new value to the maxheap
        :param key: value of new input
        """
        self.data.push(-1 * key)
        return

    def pop(self) -> int:
        """
        Removes largest value in the maxheap and removes it
        :return: int, largest value, or None if no values
        """
        ret = self.data.pop()
        if ret is not None:
            return -1 * ret
        return None


def current_medians(values) -> List[int]:
    """
    For each item in list, adds an item to the return list that is the median of the item and all items before it
    :param: values, list of items we are creating a list from
    :return: list of doubles
    """
    higher = MinHeap()
    lower = MaxHeap()

    medians = []

    x = 0
    for value in values:
        x += 1

        if lower.empty():
            lower.push(value)
        elif value < lower.top():
            lower.push(value)
        else:
            higher.push(value)

        if len(higher) == len(lower) + 2:
            lower.push(higher.pop())
        elif len(lower) == len(higher) + 2:
            higher.push(lower.pop())

        if x % 2 == 1:
            if len(lower) > len(higher):
                medians.append(lower.top())
            else:
                medians.append(higher.top())
        else:
            medians.append((lower.top() + higher.top())/2)
    return medians
