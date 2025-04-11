from collections import deque


def kahn(graph):
    """
    Accepts a graph in the form of a dict where keys are node names and
    values are list of dependent nodes.

    Returns:
    - topologically sorted nodes, None - if no cycle detected
    - None, cycle nodes - if cycle detected

    """
    # Compute in-degree for each node
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # Initialize a queue with nodes of in-degree 0
    queue = deque([node for node in graph if in_degree[node] == 0])
    topo_order = []

    # Process nodes in the queue
    while queue:
        u = queue.popleft()
        topo_order.append(u)

        # Decrease in-degree for neighbors
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    # Check for cycles
    if len(topo_order) == len(graph):
        return topo_order, None  # No cycle

    # Find remaining nodes (they form cycles)
    remaining_nodes = [node for node in graph if in_degree[node] > 0]

    # Extract a cycle from remaining nodes
    cycle = find_cycle(graph, remaining_nodes)

    return None, cycle


def find_cycle(graph, remaining_nodes):
    """Finds a cycle in the remaining nodes using DFS."""
    visited = set()
    path = []
    cycle_nodes = []

    def dfs(node):
        nonlocal cycle_nodes
        if node in path:
            # Cycle detected: extract the cycle from the path
            idx = path.index(node)
            cycle_nodes = path[idx:] + [node]
            return True
        if node in visited:
            return False

        visited.add(node)
        path.append(node)

        for neighbor in graph[node]:
            if dfs(neighbor):
                return True

        path.pop()
        return False

    for node in remaining_nodes:
        if dfs(node):
            return cycle_nodes
    return remaining_nodes  # Fallback: return all remaining nodes if no explicit cycle is found

