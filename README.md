# Color_the_graph

A label propagation algorithm for community detection in large-scale networks

## What is Color_the_graph

Color_the_graph is an implementation of the community detection algorithm described in the paper of
Usha Nandini, Reka Albert, and Soundar Kumara - Near linear time algorithm to detect community structures
in large-scale networks.

The algorithm uses label propagation method implemented in two variants:

(1) Async: starts from the random labels assigned to ech node.
Then each node updates its label depending on which label its neighbours mostly have.

See ./ctg_py

(2) Sync: spawns one process for each network node. Then nodes exchange their labels
until either predefined threshold or maximum numner of cycles are exceeded. 

See ./ctg_erl

