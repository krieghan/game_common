from zope.interface import Interface

class Node(object):
    def __init__(self, data):
        self.data = data
        self.nodes = set()

    def add_connected_node(self, node):
        self.nodes.add(node)

    def remove_connected_node(self, node):
        self.nodes.remove(node)

    def add_two_way_connected_node(self, node):
        self.add_connected_node(node)
        node.add_connected_node(self)

    def remove_two_way_connected_node(self, node):
        self.remove_connected_node(node)
        node.remove_connected_node(self)

    def remove_all_two_way_connected_nodes(self):
        for node in self.nodes:
            self.remove_two_way_connected_node(node)

    def get_connected_nodes(self):
        return self.nodes

class NodeData(Interface):
    def is_traversable():
        pass

class IndexedPriorityQueue(object):
    def __init__(self):
        self.priority_by_element = {}

    def enqueue(self, element, priority):
        self.priority_by_element[element] = priority

    def dequeue(self):
        min_element = None
        min_priority = None
        for (element, priority) in self.priority_by_element.items():
            if min_priority is None or priority < min_priority:
                min_priority = priority
                min_element = element

        del self.priority_by_element[element]
        return (min_element, min_priority)



def get_path_to_target(start_node, target_node):
    nodes = start_node.get_connected_nodes()
    heuristic_lowest_cost_so_far = dict()
    real_costs = dict()
    heuristic_lowest_cost_so_far[start_node] = 0
    real_costs[start_node] = 0
    for node in nodes:


        

    

