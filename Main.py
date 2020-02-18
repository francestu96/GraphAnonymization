import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import Anonymity as anonymity
import Graph as graph
import Queries as queries
from mpl_toolkits.mplot3d import axes3d
from datetime import datetime

def plot_vertex_refinement(vr, pert, colors):
    for i in range (0, 5):
        x, y = zip(*vr[i].items())        
        plt.plot(x, y, colors[i], label="i=" + str(i))
    plt.title("Perturbation: {:.0%}".format(pert))
    plt.legend()
    plt.savefig('img/vertex_refinement_pert_{}.png'.format(int(pert * 100)), dpi=500)        
    plt.close()

def plot_edge_factors(ef, pert, colors):
    for i in range (0, 5):
        x, y = zip(*ef[i].items())        
        plt.plot(x, y, colors[i], label="edge_facts=" + str((i+1) * 10))
    plt.title("Perturbation: {:.0%}".format(pert))
    plt.legend()
    plt.savefig('img/edge_factors_pert_{}.png'.format(int(pert * 100)), dpi=500)        
    plt.close()

# g = graph.create_ex_graph()
# g = graph.read_graph('res/HepTh.txt', 'HepTh')
g = graph.create_scale_free_graph(500)

colors = ["r", "g", "b", "y", "k"]
pert_range = [0, 0.02, 0.05, 0.1]
vr_range = [1, 2, 3, 4, 5]
ef_range = [10, 20, 30, 40, 50]
start = datetime.now()

for pert in pert_range:
    print('\nPerturbation ({:.0%})'.format(pert))

    pert_g = anonymity.perturbation(g, pert)

    vr = [anonymity.deanonymize_vertexref(g, pert_g, i) for i in vr_range]
    ef = [anonymity.deanonymize_edgefacts(g, pert_g, n) for n in ef_range]

    plot_vertex_refinement(vr, pert, colors)
    plot_edge_factors(ef, pert, colors)
    graph.draw_graph(pert_g, pert, nx.spring_layout(g))

end = datetime.now()
duration = end - start

print('Execution time: {}'.format(duration))