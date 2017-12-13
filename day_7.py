""""
--- Day 7: Recursive Circus ---
Wandering further through the circuits of the computer, you come upon a tower of
programs that have gotten themselves into a bit of trouble. A recursive
algorithm has gotten out of hand, and now they're balanced precariously in a
large tower.

One program at the bottom supports the entire tower. It's holding a large disc,
and on the disc are balanced several more sub-towers. At the bottom of these
sub-towers, standing on the bottom disc, are other programs, each holding their
own disc, and so on. At the very tops of these sub-sub-sub-...-towers, many
programs stand simply keeping the disc below them balanced but with no disc of
their own.

You offer to help, but first you need to understand the structure of these
towers. You ask each program to yell out their name, their weight, and (if
they're holding a disc) the names of the programs immediately above them
balancing on that disc. You write this information down (your puzzle input).
Unfortunately, in their panic, they don't do this in an orderly fashion; by the
time you're done, you're not sure which program gave which information.

For example, if your list is the following:

pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)

...then you would be able to recreate the structure of the towers that looks like this:

                gyxo
              /     
         ugml - ebii
       /      \     
      |         jptl
      |        
      |         pbga
     /        /
tknk --- padx - havc
     \        \
      |         qoyq
      |             
      |         ktlj
       \      /     
         fwft - cntj
              \     
                xhth
                
In this example, tknk is at the bottom of the tower (the bottom program), and is
holding up ugml, padx, and fwft. Those programs are, in turn, holding up other
programs; in this example, none of those programs are holding up any other
programs, and are all the tops of their own towers. (The actual tower balancing
in front of you is much larger.)

Before you're ready to help them, you need to make sure your information is
correct. What is the name of the bottom program?

Your puzzle answer was bsfpjtc.

--- Part Two ---
The programs explain the situation: they can't get down. Rather, they could get
down, if they weren't expending all of their energy trying to keep the tower
balanced. Apparently, one program has the wrong weight, and until it's fixed,
they're stuck here.

For any program holding a disc, each program standing on that disc forms a
sub-tower. Each of those sub-towers are supposed to be the same weight, or the
disc itself isn't balanced. The weight of a tower is the sum of the weights of
the programs in that tower.

In the example above, this means that for ugml's disc to be balanced, gyxo,
ebii, and jptl must all have the same weight, and they do: 61.

However, for tknk to be balanced, each of the programs standing on its disc and
all programs above it must each match. This means that the following sums must
all be the same:

ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243

As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the
other two. Even though the nodes above ugml are balanced, ugml itself is too
heavy: it needs to be 8 units lighter for its stack to weigh 243 and keep the
towers balanced. If this change were made, its weight would be 60.

Given that exactly one program is the wrong weight, what would its weight need
to be to balance the entire tower?

Your puzzle answer was 529.
"""

from typing import List
import queue

class Node:
    """ A class that represents tree node """
    def __init__(self, name: str):
        self.name = name
        self.weight = 0
        self.children_weight = 0
        self.parent: Node = None
        self.children: List[Node] = list()

    def get_total_weight(self):
        """ Returns a total weight of the node """
        self.update_children_weight()
        return self.weight + self.children_weight

    def update_children_weight(self):
        """ Updates weight of all children """
        if (self.children_weight == 0) and self.children:
            self.children_weight = sum(map(lambda n: n.get_total_weight(), self.children))

    def get_leafs(self):
        """ Returns all sub-nodes that are leafs """
        leafs = list({node for node in self.children if not node.children})
        for node in self.children:
            leafs.extend(node.get_leafs())
        return leafs

    def get_siblings(self):
        """ Returns node's siblings """
        if self.parent is None:
            return list()
        else:
            return self.parent.children

def read_tree(file_name: str) -> Node:
    """ Reads tree from the file and returns a root node """

    all_nodes = dict()
    def get_node(name: str) -> Node:
        """ Gets a node by name from the list of all nodes, or creates a new one """

        if name in all_nodes:
            return all_nodes[name]
        else:
            new_node = Node(name)
            all_nodes[name] = new_node
            return new_node

    with open(file_name) as file:
        for line in file:
            parts = line.strip('\r\n').split(' ')

            node = get_node(parts[0])
            node.weight = int(parts[1][1:-1])

            if len(parts) > 2:
                for i in range(3, len(parts)):
                    child_name = parts[i].strip(',')
                    child_node = get_node(child_name)
                    node.children.append(child_node)
                    child_node.parent = node

    return list({n for n in all_nodes.values() if n.parent is None})[0]

def is_parent_lighter(node: Node) -> bool:
    """ Determines if the parent of the node is lighter than its (parent's) siblings """
    parent_siblings = node.parent.get_siblings()
    if len(parent_siblings) < 2:
        if node.parent.parent is None:
            return False
        return is_parent_lighter(node.parent)

    parent_index = parent_siblings.index(node.parent)
    parent_sibling_index = (parent_index+1) % len(parent_siblings)
    return node.parent.get_total_weight() < parent_siblings[parent_sibling_index].get_total_weight

def get_correct_weight(root_node: Node) -> int:
    """ Returns the correct weight for the only unbalanced node """
    nodes = queue.Queue()
    processed_nodes = set()
    for leaf in root_node.get_leafs():
        nodes.put(leaf)

    while nodes:
        node: Node = nodes.get()
        if node in processed_nodes:
            continue

        siblings = node.get_siblings()
        nodes.put(node.parent)

        for i in range(1, len(siblings)):
            total_weight_i = siblings[i].get_total_weight()
            total_weight_i_1 = siblings[i-1].get_total_weight()
            if siblings[i].get_total_weight() != siblings[i-1].get_total_weight():
                if len(siblings) > 2:
                    # if there are more than 2 siblings, compare weight with another sibling
                    if total_weight_i != siblings[(i+1) % len(siblings)].get_total_weight():
                        # i-th sibling has total weight different from (i-1)-th and (i+1)-th
                        # siblings, so we adjust its weight to match the total weight of
                        # (i-1)-th sibling
                        return siblings[i].weight + (total_weight_i_1 - total_weight_i)
                    else:
                        # i-th sibling has the same total weight as (i+1)-th sibling, so we adjust
                        # the (i-1)-th sibling weight to match the total weight of i-th sibling
                        return siblings[i-1].weight + (total_weight_i - total_weight_i_1)
                else:
                    # if there are two siblings, compare weight of parent
                    if is_parent_lighter(siblings[i]):
                        # the parent is lighter than its siblings, so we take the lighter node
                        # and add to its weight
                        return min(siblings[i].weight, siblings[i-1].weight) + \
                            abs(total_weight_i - total_weight_i_1)
                    else:
                        # the parent is heavier than its siblings, so we take the heavier node
                        # and substract from its weight
                        return max(siblings[i].weight, siblings[i-1].weight) - \
                            abs(total_weight_i - total_weight_i_1)

        for sibling in siblings:
            processed_nodes.add(sibling)

def main():
    """ Main function """
    root_node = read_tree('day_7_input.txt')
    root_node.update_children_weight()
    print(root_node.name)
    print(get_correct_weight(root_node))

main()
