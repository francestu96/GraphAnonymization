from random import choice
import networkx as nx
import itertools

from sys import stderr


def vertex_refinement(g, i):
    neighbors = {n: get_neighbours(g, n, i-1) for n in g.nodes()}

    res = {}
    for k,v in neighbors.items():
        if i == 0:
            res[k] = [0]
        else:
            res[k] = sorted([g.degree(n) for n in v])

        print('  Vertex Refinement[{} i] {:.3%}\t\r'.format(i, (list(neighbors.keys()).index(k) + 1)/len(neighbors.items())), file=stderr, end='')
    print()
    return res


def get_neighbours(g, start, k):
    nbrs = set([start])
    for i in range(k):
        nbrs = set((nbr for n in nbrs for nbr in g[n]))
    return nbrs

def edge_facts_subgraph(g, g_pert, edge_factors):
    res = {}
    nodes_number = len(g.nodes) * len(g_pert.nodes)

    i = 0
    for start in g.nodes:
        fact = get_subgraph(g, edge_factors, start)
        res[start] = []
        for node in g_pert.nodes:
            subgraph = get_subgraph(g_pert, edge_factors, node)
            if nx.is_isomorphic(fact, subgraph):
                    res[start].append(node)          
            i += 1
            print('  Edge Factors[{} edges] {:.3%}\t\r'.format(edge_factors, i/nodes_number), file=stderr, end='')
    print()
    return res


def get_subgraph(g, edge_factors, start):
    graph = nx.Graph()
    graph.add_node(start)

    for node, edges in nx.bfs_successors(g, start):
        for edge in edges:
            if edge_factors == 0:
                break

            graph.add_edge(node, edge)
            edge_factors -= 1

    return graph

# def edge_facts_subgraph(g, edge_number):
#     count = 0
#     res = {}
#     for start_node in g.nodes:
#         res[start_node] = []

#         i = 0
#         subgraph = nx.bfs_tree(g, start_node)
#         for node in subgraph:            
#             if edge_number == i:
#                 break

#             res[start_node].append(node)
#             i += 1

#         count += 1
#         print('  Subgraph Knowledge[{} edges] {:.3%}\t\r'.format(edge_number, count/len(g.nodes)), file=stderr, end='')
#     print()
#     return res