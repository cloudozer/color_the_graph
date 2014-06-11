#!/usr/bin/python
#
# pumping the water
# 
#
####################################################### 

import gdspy
import numpy as np
import gv

# Import pygraph
from pygraph.classes.graph import graph
from pygraph.readwrite.dot import write

from random import random

def main():
	gr = build_graph()

	for i in range(1000):
		gr = update(gr, 0.01, 0.2)
	draw_graph(gr)
	
	for i in range(100):
		gr = update(gr, 0.01, 0.2)
	draw_graph(gr)


def update(gr, leakage, resistance):
	new_gr = copy_graph(gr)

	for node in gr.nodes(): 
		old_level = dict(gr.node_attributes(node)).get('level')
		node_leakage = old_level * leakage
		outcome = sum( [ resistance * \
			(dict(gr.node_attributes(node)).get('level') - dict(gr.node_attributes(n)).get('level')) \
			for n in gr.neighbors(node) ] )
		income = dict(gr.node_attributes(node)).get('in', 0)
		new_level = old_level - node_leakage - outcome + income
		new_gr.add_node_attribute(node, ('level', new_level))
	
	return new_gr


def build_graph():
	gr = graph()

	for i in range(1,11):
		gr.add_node(i)
		gr.add_node_attribute(i, ('level', 0) )

	gr.add_edge((1,3))
	gr.add_edge((1,4))
	gr.add_edge((2,3))
	gr.add_edge((2,5))
	gr.add_edge((5,3))
	gr.add_edge((5,6))
	gr.add_edge((6,3))
	gr.add_edge((4,6))
	gr.add_edge((6,7))
	gr.add_edge((7,8))
	gr.add_edge((7,10))
	gr.add_edge((8,9))
	gr.add_edge((9,10))

	#gr.add_edge((2,8))

	gr.add_node_attribute(3, ('in', 10))

	return gr


def copy_graph(gr):
	"""
	returns a copy of the graph <gr>
	"""
	new_gr = graph()

	for n in gr.nodes():
		new_gr.add_node(n)
		#new_gr.add_node_attribute(n, ('level', dict(gr.node_attributes(n)).get('level')))
		if dict(gr.node_attributes(n)).get('in') != None:
			new_gr.add_node_attribute(n, ('in', dict(gr.node_attributes(n)).get('in')))
			

	for ed in gr.edges():
		if not new_gr.has_edge(ed):
			new_gr.add_edge(ed)

	return new_gr


def draw_graph(gr):
    """
    draws the graph to file
    """
    print "Nodes levels after 100 steps:"
    for node in gr.nodes():
    	print "Node: %i - level:%.1f" % (node, dict(gr.node_attributes(node)).get('level'))

    dot = write(gr)
    gvv = gv.readstring(dot)
    gv.layout(gvv,'dot')
    gv.render(gvv,'png','pumping.png') 

if __name__ == '__main__':
	main()
