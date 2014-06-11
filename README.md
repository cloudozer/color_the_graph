# Color_the_graph
### A lable propagation algorithm for community detection in large-scale networks

June 11, 2014

## What is Color_the_graph

Color_the_graph is an implementation of the community detection algorithm described in the paper of
Usha Nandini, Reka Albert, and Soundar Kumara - Near linear time algorithm to detect community structures
in large-scale networks

The algorithm uses lable propagation method, which starts from the random lables assigned to ech node.
Then each node updates its lable depending on which lable its neighbours mostly have.


## References
Usha Nandini, Reka Albert, and Soundar Kumara - Near linear time algorithm to detect community structures
in large-scale networks. Published by Pennsylvania State University in September 11, 2007.

## How to install it
% git clone color_the_graph

Check and if needed install python-graph
Check and if needed install gv and graphviz 


## How to run it
% python color_the_grap.py data_file

data_file is a text file containing graph edges in the following format:

[{<<"10.192.20.102">>,<<"199.59.150.39">>},
 {<<"10.120.3.25">>,<<"10.120.10.97">>},
 {<<"74.125.224.198">>,<<"2620:10a:6000:2000::3db">>},
 ....
]


### Prerequisites
Python 2.x

### Libraries
* pygraph
* gv
* graphviz

## Input file containing the graph
The data file containing graph edges should have the following format:

[{<<"10.192.20.102">>,<<"199.59.150.39">>},
 {<<"10.120.3.25">>,<<"10.120.10.97">>},
 {<<"74.125.224.198">>,<<"2620:10a:6000:2000::3db">>},
 ....
]

