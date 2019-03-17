from collections import deque
from typing import Deque, Optional

from sortedcontainers import SortedSet

from .errors import DifferentModel


class ModelTrie:
    part_list = []
    head = None

    def add(self, part) -> None:
        part_tokens = deque(part.model.split(" "))
        if not self.head:
            self.head = Node(part_tokens.popleft())
        elif self.head:
            if not self.head.value == part_tokens.popleft():
                raise DifferentModel

        current_node = self.head
        for token in part_tokens:
            if token in current_node.children:
                current_node = current_node.children[token]
            else:
                new_node = Node(token)
                current_node.children.update({token: new_node})
                current_node = new_node
        self.part_list.append(part)

    def retrieve_model(self) -> Deque[str]:
        if len(self.head.children) == 1:
            possible_second_value, next_node = self.head.children.popitem()
            if is_model_number(possible_second_value):
                return deque((self.head.value,))
            elif len(next_node.children) == 1:
                possible_third_value, _ = next_node.children.popitem()
                if not is_model_number(possible_third_value):
                    return deque((self.head.value, possible_second_value, possible_third_value))
            return deque((self.head.value, possible_second_value))
        return deque((self.head.value,))


def is_model_number(string: str) -> bool:
    return any(x for x in string if x.isnumeric()) and any((x for x in string if x.isalpha())) or string.isnumeric()


class BrandTrie:

    def __init__(self):
        self.head = Node(None)

    def add(self, brand_tokens: Deque[str]) -> None:
        current_node = self.head
        for x, token in enumerate(brand_tokens):
            if token in current_node.children and x == len(brand_tokens) - 1:
                current_node = current_node.children[token]
                current_node.completed = True
                current_node.children = dict()
            elif token in current_node.children:
                current_node = current_node.children[token]
            elif not current_node.completed:
                new_node = Node(token)
                current_node.children.update({token: new_node})
                current_node = new_node

    def get_all_brands(self) -> SortedSet:
        return_set = SortedSet()
        for value, node in self.head.children.items():
            if len(node.children) == 1 and not node.completed:
                _, child_node = node.children.popitem()
                if not child_node.value == value:
                    if len(child_node.children) == 1 and not child_node.completed:
                        _, second_child_node = child_node.children.popitem()
                        if f"{value} {child_node.value}" not in return_set \
                                and not second_child_node.value == child_node.value:
                            return_set.add(f"{value} {child_node.value} {second_child_node.value}")
                    else:
                        return_set.add(f"{value} {child_node.value}")
                else:
                    return_set.add(value)
            else:
                return_set.add(value)
        return return_set


class Node:

    def __init__(self, value: Optional[str]) -> None:
        self.value = value
        self.children = {}
        self.completed = False

    def __repr__(self):
        return f"Node(value={self.value}, children={str(self.children)})"
