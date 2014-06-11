# Color_the_graph

A label propagation algorithm for community detection in large-scale networks

## What is Color_the_graph

Color_the_graph is an implementation of the community detection algorithm described in the paper of
Usha Nandini, Reka Albert, and Soundar Kumara - Near linear time algorithm to detect community structures
in large-scale networks.

The algorithm uses label propagation method, which starts from the random labels assigned to ech node.
Then each node updates its label depending on which label its neighbours mostly have.

## Prerequisites

Color_the_graph requires python-graph.

## Install and run

	% git clone https://github.com/cloudozer/color_the_graph
	% python color_the_grap.py sample.data

## Data format

The data file contains graph edges in the following format:

	[{<<"10.192.20.102">>,<<"199.59.150.39">>},
	 {<<"10.120.3.25">>,<<"10.120.10.97">>},
	 {<<"74.125.224.198">>,<<"2620:10a:6000:2000::3db">>},
	 ...,
	]
