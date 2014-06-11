#!/usr/bin/python
#
# label propagation algorithm that
# splits the graph into parts. 
# Each node inside any part has more internal edges than external 
#
####################################################### 

import sys

# Import pygraph
from pygraph.classes.graph import graph

from random import random



def main(input_data_file):
    N_nbr = 12
    E_nbr = 40
    network_data = input_data_file
    #data_file = 'community.dat'
    fraction_of_picked_data = 1

    #gr = build_graph(N_nbr, E_nbr)
    #gr = import_network(network_data)
    gr = import_network_erl(network_data, fraction_of_picked_data)
    #gr = build_2_star_graph(150,75)
    
    
    #mark_randomly(gr)
    
    gr = extract_communities(gr)
    color_graph(gr)
    
    print_communities(gr)
    #print_communities_1(data_file)
    
    #draw_graph(gr)


    
def mark_randomly(gr):
    N = len(gr.nodes())/3
    for node in gr.nodes():
        gr.add_node_attribute(node,('col',int(N*random())))


def print_communities_1(data):
    comm_dict = {}

    with open(data) as f:
        line = f.readline()
        while line != '':
            link = line.split()
            n = int(link[0])
            comm = int(link[1])
            if comm in comm_dict:
                comm_dict[comm] += 1
            else:
                comm_dict[comm] = 1
            line = f.readline()

    f.close()
    print "\n%i communities were extracted by asyncronous algorithm" % len(comm_dict.keys()) 


def print_communities(gr):
    
    colors = [ (n, dict(gr.node_attributes(n)).get('col')) for n in gr.nodes() ]
    #print colors
    
    cluster_dict = {}
    for c in colors:
        if c[1] in cluster_dict:
            cluster_dict[c[1]] += 1
        else:
            cluster_dict[c[1]] = 1

    print "\n%i communities were extracted" % len(cluster_dict.keys())

    stat = {}
    for c in cluster_dict:
        if cluster_dict[c] in stat:
            stat[cluster_dict[c]] += 1
        else:
            stat[cluster_dict[c]] = 1
            
        #print "Cluster %s has %i nodes" % (c, cluster_dict[c])
    
    print "Cluster_size - occurrences"
    for s in stat:
        print "\t%i - %i" % (s, stat[s])

def import_network(data_file):
    gr = graph()

    with open(data_file) as f:
        line = f.readline()
        while line != '':
            link = line.split()
            n1 = int(link[0])
            n2 = int(link[1])
            #print n1,n2
            if not gr.has_node(n1): 
                gr.add_node(n1)
                gr.add_node_attribute(n1, ('col', n1))
            if not gr.has_node(n2): 
                gr.add_node(n2)
                gr.add_node_attribute(n2, ('col', n2))

            if not gr.has_edge((n1,n2)): 
                gr.add_edge((n1,n2))
            #s = raw_input()
            line = f.readline()

    f.close()
    return gr


def import_network_erl(data_file,eps):
    gr = graph()
    
    with open(data_file) as f:
        line = f.readline()
        while line != '':
            
            if not coin(eps): 
                line = f.readline()
                continue

            link = line.split('"')
            #print link
            #_ = raw_input()
            n1 = link[1]
            n2 = link[3]
            #print n1,n2
            if not gr.has_node(n1): 
                gr.add_node(n1)
                gr.add_node_attribute(n1, ('col', n1))
            if not gr.has_node(n2): 
                gr.add_node(n2)
                gr.add_node_attribute(n2, ('col', n2))

            if not gr.has_edge((n1,n2)): 
                gr.add_edge((n1,n2))
            #s = raw_input()
            line = f.readline()

    f.close()
    print "Graph has %i nodes and %i edges\n" % (len(gr.nodes()), len(gr.edges()) )
    return gr


def build_2_star_graph(n1,n2):
    """
    builds a graph consisting of two stars of n1 and n2 nodes connected with each other
    """
    gr = graph()
    gr.add_node(0)
    gr.add_node_attribute(0, ('col', 0))

    for i in range(1,n1):
        gr.add_node(i)
        gr.add_node_attribute(i, ('col', i))
        gr.add_edge((0,i))

    gr.add_node(n1)
    gr.add_node_attribute(n1, ('col', n1))
    gr.add_edge((0,n1))

    for i in range(n1+1,n1+n2):
        gr.add_node(i)
        gr.add_node_attribute(i, ('col', i))
        gr.add_edge((n1,i))

    return gr


def build_graph(node_nbr, edge_nbr):
    """
    builds a random graph having given number of <node_nbr> and <edge_nbr>
    """
    gr = graph()

    for i in range(node_nbr):
        gr.add_node(i)
        gr.add_node_attribute(i, ('col', i))

    for i in range(edge_nbr):
        n1 = int(random()*node_nbr*5) % node_nbr 
        n2 = int(n1 + random()*node_nbr/4) % node_nbr
        if n1 == n2:
            n2 = (n2+1) % node_nbr
        
        if not gr.has_edge((n1,n2)):
            gr.add_edge((n1,n2))
        else:
            #print "Edge:(%i,%i) is already in the graph" % (n1,n2)
            pass
    #print "Edges:", gr.edges()

    return gr


def extract_communities(gr):
    #iter_nbr = 3 + len(gr.edges()) / len(gr.nodes())
    conv = 0
    iter_nbr = 0

    while conv < 0.99 and iter_nbr < 20:
        conv = change_community(gr)
        iter_nbr += 1
        print "Iteration %i, convergence - %.2f" % (iter_nbr, conv)
        #_ = raw_input()

    return gr


def shuffle(nodes):
    N = len(nodes)
    for i in range(N):
        el = nodes.pop(int(N*random()))
        nodes.append(el)

    return nodes


def change_community(gr):
    convergence = 0.0
    nodes = shuffle(gr.nodes())
    
    for node in nodes:
        old_color = dict(gr.node_attributes(node)).get('col')

        colors = [ dict(gr.node_attributes(n)).get('col') for n in gr.neighbors(node) ]
        color_dict = {c: colors.count(c) for c in set(colors)}
        #print color_dict
        max_val = max(color_dict.values())

        variants = []
        for c in color_dict:
            if color_dict[c] == max_val:
                variants.append(c)

        new_color = randomly_pick(variants)
        gr.add_node_attribute(node,('col',new_color))

        if new_color == old_color:
            convergence += 1

    return convergence/len(gr.nodes())




def randomly_pick(variants):
    nbr = len(variants)
    i = 0
    while True:
        if coin(1.0/nbr):
            return variants[i]
        else:
            nbr -= 1
            i += 1


def coin(p):
    return random() < p


def copy_graph(gr):
    """
    returns a copy of the graph <gr>
    """
    new_gr = graph()
    for n in gr.nodes():
        new_gr.add_node(n)

    #print "New graph edges:", new_gr.edges()
    for ed in gr.edges():
        if new_gr.has_edge(ed): 
            #print "Edge is already in the graph:", ed
            pass
        else:
            #print " Adding edge", ed
            new_gr.add_edge(ed)

    return new_gr


def color_graph(gr):
    color = [ 'red', 'magenta', 'green', 'cyan', 'blue', \
        'navy', 'grey', 'black' ]
    
    colors = [dict(gr.node_attributes(n)).get('col') for n in gr.nodes() ]

    for n in gr.nodes():
        #print "Node: %i, color %i"  % (n, dict(gr.node_attributes(n)).get('col'))
        c = colors.index(dict(gr.node_attributes(n)).get('col'))
        if c == None : col = 'black'
        else: 
            col = color[c%8]
            
        gr.add_node_attribute(n, ('color', col))
        gr.add_node_attribute(n, ('fillcolor', col))
        
        

def draw_graph(gr):
    """
    draws the graph to file
    """
    p = 100.0 / (len(gr.nodes())+1)
    gr_ext = graph()

    
    for node in gr.nodes():
        if coin(p):
            if not gr_ext.has_node(node):
                gr_ext.add_node(node,attrs=gr.node_attributes(node))
            for n in [ ed[0] for ed in gr.edges() if ed[1] == node ]:
                if coin(0.3):
                    if not gr_ext.has_node(n):
                        gr_ext.add_node(n,attrs=gr.node_attributes(n))
                    # print "Edges:",gr_ext.edges()
                    if not gr_ext.has_edge((node,n)):
                        gr_ext.add_edge((node,n)) 
        

    #dot = write(gr_ext)
    #gvv = gv.readstring(dot)
    #gv.layout(gvv,'dot')
    #gv.render(gvv,'png','community.png')    


if __name__ == '__main__':
    args = sys.argv[:]
    if len(args) == 2:
        main(args[1])
    else:
        print "Usage: <python> <color_the_graph.py> <data_file>"
        