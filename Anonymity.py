import networkx as nx
from random import choice
from math import inf
import pandas as pd

import Queries as queries


def perturbation(graph, p):
    g = graph.copy()
    edges_to_remove = int(len(g.edges()) * p)
    
    removed_edges = []
    for i in range(edges_to_remove):
        random_edge = choice(list(g.edges()))
        g.remove_edges_from([random_edge])
        removed_edges.append(random_edge)

    while(edges_to_remove > 0):
        first_node = choice(list(g.nodes()))
        second_node = choice(list(g.nodes()))
        if(second_node == first_node):
            continue
        if g.has_edge(first_node, second_node) or (first_node, second_node) in removed_edges or (second_node, first_node) in removed_edges:
            continue
        else:
            g.add_edge(first_node, second_node)
            edges_to_remove -= 1
    
    return g


def deanonymize_vertexref(g, pert_g, i):
    vertexref = queries.vertex_refinement(g, i)
    vertexref_pert = queries.vertex_refinement(pert_g, i)
    eq = eq_class(vertexref)
    eq_pert = eq_class(vertexref_pert)
    
    result_eq = {}
    for index in range(0, max(len(eq), len(eq_pert))):
        result = []
        if index < len(eq_pert):
            for value in eq_pert[index]:
                if index < len(eq): 
                    if value in eq[index]:
                        result.append(value)
            result_eq[index] = result

    return deanonymize(result_eq.values(), len(pert_g.nodes))


def deanonymize_edgefacts(g, pert_g, edge_factors):
    edgefacts = queries.edge_facts_subgraph(g, pert_g, edge_factors)
    eq = eq_class(edgefacts)

    return deanonymize(eq, len(pert_g.nodes))


def deanonymize(eq, nodes_number):
    # eq = eq(facts).values()
    # eq = eq(facts)

    result = {}    
    result['20-inf'] = get_k_anonimity_range(eq, 21, inf) / nodes_number
    result['11-20'] = get_k_anonimity_range(eq, 11, 20) / nodes_number
    result['5-10'] = get_k_anonimity_range(eq, 5, 10) / nodes_number
    result['2-4'] = get_k_anonimity_range(eq, 2, 4) / nodes_number
    result['1'] = get_k_anonimity_range(eq, 1, 1) / nodes_number

    return result


def eq_class(facts: dict):
    # eq_class = []
    # for value in facts.values():
    #     value = sorted(value)                
    #     eq_class.append(value)
    eq_class = {}
    for key, degrees in facts.items():
        k = tuple(sorted(degrees))
        
        if k not in eq_class:
            eq_class[k] = []
        
        eq_class[k].append(key)

    return list(eq_class.values())

def get_k_anonimity_range(vals, minv, maxv):
    result = 0
    if len(vals) > 0:
        for value in vals:
            if len(value) >= minv and len(value) <= maxv:
                result += len(value)
    return result