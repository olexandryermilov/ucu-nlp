from collections import defaultdict


class Graph:
    def __init__(self):
        # function for adding edge to graph
        self.graph = defaultdict(list)
        self.visited_list = []

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def generate_edges(self):
        edges = []

        # for each node in graph
        for node in self.graph:

            # for each neighbour node of a single node
            for neighbour in self.graph[node]:
                # if edge exists then append
                edges.append((node, neighbour))
        return edges

    def find_paths(self, current_vertex, visited, depth, min_depth, max_depth):
        visited.append(current_vertex)
        for vertex in self.graph[current_vertex]:
            if vertex not in visited:
                if depth == max_depth:
                    break
                depth += 1
                self.find_paths(vertex, visited.copy(), depth, min_depth, max_depth)
        if len(visited) >= min_depth:
            self.visited_list.append(visited)
