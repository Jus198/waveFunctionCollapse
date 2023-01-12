class TileMinHeap:
    def __init__(self):
        # list of tuples, (TileName, priority)
        self.data = []
        self.name2position = {}
    
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

        if self.data[left][1] < self.data[right][1]:
            return left
        return right

    def percolate_up(self, index: int) -> None:
        """
        Brings a small value from the bottom of the heap to the top recursively
        :param index: index of value being brought up
        """
        parent_index = self.get_parent_index(index)
        if parent_index is not None:
            if self.data[index][1] < self.data[parent_index][1]:
                self.data[index], self.data[parent_index] = self.data[parent_index], self.data[index]
                self.name2position[self.data[index][0]] = parent_index
                self.name2position[self.data[parent_index][0]] = index
                self.percolate_up(parent_index)

    def percolate_down(self, index: int) -> None:
        """
        Brings a value down in the minheap until it is in the correct spot
        :param index: index of value we are bringing down
        """
        min_child = self.get_min_child_index(index)
        if min_child is None:
            return
        if self.data[index][1] > self.data[min_child][1]:
            self.data[index], self.data[min_child] = self.data[min_child], self.data[index]
            self.name2position[self.data[index][0]] = min_child
            self.name2position[self.data[min_child][0]] = index
            self.percolate_down(min_child)
            return

    def push(self, val: int) -> None:
        """
        Adds new value to the minheap
        :param val: val of new item in minheap
        """
        self.data.append(val)
        self.name2position[val[0]] = len(self.data)-1
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
    
    def lowerPriority(self, name):
        self.percolate_up(self.name2position[name])
        return