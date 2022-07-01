
from dataclasses import dataclass

from typing import List, Dict


@dataclass
class GraphNode:
    neighbors: List["GraphNode"]
    map: Dict[str, "GraphNode"]
    name: str
    freq: int
    visited: bool = False

    def __init__(self, name: str, freq: int):
        self.name = name
        self.freq = freq
        self.neighbors = []
        self.map = {}
    
    def add_neighbor(self, node: "GraphNode"):
        if node.name in self.map:
            return False

        self.neighbors.append(node)
        self.map[node.name] = node
        return True


class Graph():
    
    def __init__(self):
        self.nodes: List[GraphNode] = []
        self.map: Dict[str, GraphNode] = {}
    
    def has_node(self, name: str) -> bool:
        return name in self.map

    def create_node(self, name: str, freq: int) -> GraphNode:
        if name in self.map:
            return self.get_node(name)

        node = GraphNode(name, freq)
        self.nodes.append(node)
        self.map[name] = node
        
        return node

    def get_node(self, name: str) -> GraphNode:
        return self.map[name]
    
    def add_edge(self, start_name: str, end_name: str):
        start_node = self.get_node(start_name)
        end_node = self.get_node(end_name)

        if start_node and end_node:
            start_node.add_neighbor(end_node)
            end_node.add_neighbor(start_node)


def construct_graph(names: dict, synonyms: dict) -> Graph:
    graph = Graph()
    for name, freq in names.items():
        graph.create_node(name, freq)
    
    for name1, name2 in synonyms:
        graph.add_edge(name1, name2)
    
    return graph

def calc_total_freq(node: GraphNode) -> int:
    if node.visited:
        return 0
    
    node.visited = True
    total_freq = node.freq
    for neighbor in node.neighbors:
        total_freq += calc_total_freq(neighbor)
    
    return total_freq

if __name__ == "__main__":
    names = {
        "John": 3,
        "Jonathan": 4,
        "Johnny": 5,
        "Chris": 1,
        "Kris": 3,
        "Brian": 2,
        "Bryan": 4,
        "Carleton": 4,  
    }

    synonyms = [
        ("John","Jonathan"),
        ("Jonathan","Johnny"),
        ("Chris","Kris"),
        ("Brian","Bryan"),
    ]

    graph: Graph = construct_graph(names, synonyms)

    name_total_freq_map = {}
    for node in graph.nodes:
        if not node.visited:
            total_freq = calc_total_freq(node)
            name_total_freq_map[node.name] = total_freq

    print(name_total_freq_map)