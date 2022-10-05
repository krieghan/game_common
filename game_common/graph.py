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

    def get_data(self):
        return self.data

    def calculate_heuristic_cost(self, target_node):
        return self.get_data().calculate_heuristic_cost(target_node.get_data())

class NodeTraversalError(Exception):
    pass

class NodeData(Interface):
    def is_traversable():
        pass

    def calculate_heuristic_cost(target_data):
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

        del self.priority_by_element[min_element]
        return (min_element, min_priority)

    def contains(self, element):
        return self.priority_by_element.get(element) is not None

    def is_empty(self):
        return not self.priority_by_element



def get_path_to_target(start_node, target_node):
    closed_set = set()
    open_set = IndexedPriorityQueue()

    heuristic_costs = dict()
    parenting = dict()
    heuristic_total_cost =\
            start_node.calculate_heuristic_cost(target_node)
    heuristic_costs[start_node] = heuristic_total_cost
    parenting[start_node] = (None, 0)
    open_set = IndexedPriorityQueue()
    open_set.enqueue(start_node, heuristic_total_cost)
    
    while not open_set.is_empty():
        (current_node, _priority) = open_set.dequeue()
        if current_node is target_node:
            break
        closed_set.add(current_node)
        _current_parent, current_cost = parenting[current_node]
        neighbor_cost = current_cost + 1
        nodes_to_add = current_node.get_connected_nodes()
        for node_to_add in nodes_to_add:
            if node_to_add in closed_set:
                continue

            if (node_to_add is not target_node and 
                not node_to_add.get_data().is_traversable()):
                continue

            heuristic_cost_for_node = heuristic_costs.get(node_to_add)
            if heuristic_cost_for_node is None:
                heuristic_cost_for_node =\
                    heuristic_costs[node_to_add] =\
                        node_to_add.calculate_heuristic_cost(target_node)
            (current_parent, best_cost_so_far) =\
                parenting.get(node_to_add, (None, None))
            if best_cost_so_far is None or best_cost_so_far > neighbor_cost:
                parenting[node_to_add] = (current_node, neighbor_cost)

            open_set.enqueue(
                node_to_add,
                heuristic_cost_for_node + neighbor_cost)

    if parenting.get(target_node) is None:
        return None
    else:
        return construct_path(start_node, target_node, parenting)

def construct_path(start_node, target_node, parenting):
    path = []
    current_node = target_node

    while current_node is not None:
        path.append(current_node)
        (current_node, _current_priority) = parenting.get(current_node)

    return list(reversed(path))




