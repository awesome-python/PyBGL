#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Non-recursive implementation of Depth First Search algorithm.
#
# Based on https://www.boost.org/doc/libs/1_68_0/boost/graph/breadth_first_search.hpp by Andrew Lumsdaine, Lie-Quan Lee, Jeremy G. Siek
#
# This file is part of the pybgl project.
# https://github.com/nokia/pybgl

__author__     = "Marc-Olivier Buob"
__maintainer__ = "Marc-Olivier Buob"
__email__      = "marc-olivier.buob@nokia-bell-labs.com"
__copyright__  = "Copyright (C) 2018, Nokia"
__license__    = "BSD-3"

from collections           import deque
from pybgl.graph           import Graph, EdgeDescriptor, out_edges, source, target
from pybgl.incidence_graph import in_edges
from pybgl.graph_traversal import WHITE, GRAY, BLACK
from pybgl.property_map    import ReadWritePropertyMap

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# /!\ DO NOT MODIFY THIS FILE
# It conforms to https://www.boost.org/doc/libs/1_68_0/boost/graph/breadth_first_search.hpp
# We just moved some parameters.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class DefaultBreadthFirstSearchVisitor():
    def __init__(self): super().__init__()
    def discover_vertex(self, u :int, g :Graph): pass
    def examine_edge(self, e :EdgeDescriptor, g :Graph): pass
    def examine_vertex(self, u :int, g :Graph): pass
    def tree_edge(self, e :EdgeDescriptor, g :Graph): pass
    def non_tree_edge(self, e :EdgeDescriptor, g :Graph): pass
    def gray_target(self, e :EdgeDescriptor, g :Graph): pass
    def black_target(self, e :EdgeDescriptor, g :Graph): pass
    def finish_vertex(self, u :int, g :Graph): pass

# Multiple sources
def breadth_first_search_graph(
    g           :Graph,
    sources     :set, # Or a generator e.g. vertices(g)
    pmap_vcolor :ReadWritePropertyMap,
    vis         = DefaultBreadthFirstSearchVisitor(),
    # N.B: The following parameter does not exist in libboost:
    if_push     = None, # if_push(e :EdgeDecriptor, g :Graph) -> bool returns True iff e is relevant
    forward     = True  # allows to go through an IncidenceGraph backward
):
    _out_edges = out_edges if forward else in_edges
    _target    = target    if forward else source

    if not if_push: if_push = (lambda e, g: True)

    stack = deque()
    for s in sources:
        pmap_vcolor[s] = GRAY
        vis.discover_vertex(s, g)
        stack.append(s)

    while stack:
        u = stack.pop()

        vis.examine_vertex(u, g)
        for e in _out_edges(u, g):
            v = _target(e, g)
            vis.examine_edge(e, g)
            color_v = pmap_vcolor[v]
            if color_v == WHITE:
                vis.tree_edge(e, g)
                pmap_vcolor[v] = GRAY
                vis.discover_vertex(v, g)
                if if_push(e, g):
                    stack.appendleft(v)
            elif color_v == GRAY:
                vis.gray_target(e, g)
            else:
                vis.black_target(e, g)
        pmap_vcolor[u] = BLACK
        vis.finish_vertex(u, g)

# Single source
def breadth_first_search(
    s :int,
    g :Graph,
    pmap_vcolor :ReadWritePropertyMap,
    vis         = DefaultBreadthFirstSearchVisitor(),
    # N.B: The following parameters doe not exists in libboost:
    if_push     = None, # if_push(e :EdgeDecriptor) -> bool returns True iff e is relevant
    forward     = True
):
    breadth_first_search_graph(g, {s}, pmap_vcolor, vis, if_push, forward)

