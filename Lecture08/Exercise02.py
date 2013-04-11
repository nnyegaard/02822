import networkx as nx
import matplotlib.pyplot as plt
import random

g = nx.Graph()


def create_init_network(graph):
    #Use the range 1 to 6, so that the number range is correct, when we want to add a node later.
    [graph.add_node(i) for i in range(1, 6)]

    #Random generate edges between the 5 nodes. When choice from the nodes, we can have a worst case scenario where
    #only 2 nodes will have edges. But the BA network only need 2 or higher nodes that have edges to start.
    #We use the variable _ because we don't use the iterator variable.
    #[graph.add_edge(random.choice(graph.nodes()), random.choice(graph.nodes())) for _ in graph.nodes()]
    for _ in graph.nodes():
        a = random.choice(graph.nodes())
        b = random.choice(graph.nodes())
        if a is not b:
            graph.add_edge(a, b)


def add_one_node_with_three_connections(graph):
    #Add a node that has 1 higher number then the highest numbered node in the network
    node_to_add = len(graph.nodes()) + 1
    graph.add_node(node_to_add)

    #The probability of selecting the different nodes based on degrees
    p = []
    for node in graph.nodes():
        [p.append(node) for _ in range(0, graph.degree(node))]

    #Add the node to 3 other nodes selected random, by selecting from the probability list
    for _ in range(3):
        graph.add_edge(node_to_add, random.choice(p))


create_init_network(g)


def create_X_node_network(x):
    for _ in range(x):
        add_one_node_with_three_connections(g)


create_X_node_network(295)

nx.draw(g)

for node in g.nodes():
    print "My node {0}, its degree {1}, edges {2} and self loops {3}".format(node, g.degree(node),
                                                                             g.edges(node), g.selfloop_edges(node))


def test():
    g = nx.Graph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_node(4)
    #g.add_edge(1, 2)
    #g.add_edge(1, 3)
    for _ in g.nodes():
        a = random.choice(g.nodes())
        b = random.choice(g.nodes())
        if a is not b:
            g.add_edge(a, b)

    for node in g.nodes():
        print "My node {0}, its degree {1} and edges {2}, selfloops {3}".format(node, g.degree(node), g.edges(node),
                                                                                g.number_of_selfloops())

    print nx.number_of_edges(g)
    print nx.number_connected_components(g)

    nx.draw(g)

#test()
plt.show()
