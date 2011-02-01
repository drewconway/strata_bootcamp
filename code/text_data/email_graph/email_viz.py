#!/usr/bin/env python
# encoding: utf-8
"""
email_viz.py

Purpose:  Visualize ann9enigma@gmail.com e-mail network with NetworkX

Author:   Drew Conway
Email:    drew.conway@nyu.edu
Date:     2011-01-30

Copyright (c) 2011, under the Simplified BSD License.  
For more information on FreeBSD see: http://www.opensource.org/licenses/bsd-license.php
All rights reserved.
"""

import sys
import os
import csv
import networkx as nx
import re
import matplotlib.pylab as plt

def lattice_plot(component_list, file_path):
    """
    Creates a lattice style plot of all graph components
    """
    graph_fig=plt.figure(figsize=(20,10))    # Create figure
    
    # Set the number of rows in the plot based on an odd or
    # even number of components  
    num_components=len(component_list)
    if num_components % 2 > 0:
        num_cols=(num_components/2)+1
    else:
        num_cols=num_components/2
    
    # Plot subgraphs, with centrality annotation
    plot_count=1
    for G in component_list:
        # Find actor in each component with highest degree
        in_cent=nx.degree(G)
        in_cent=[(b,a) for (a,b) in in_cent.items()]
        in_cent.sort()
        in_cent.reverse()
        high_in=in_cent[0][1]
        
        # Plot with annotation
        plt.subplot(2,num_cols,plot_count)
        nx.draw_spring(G, node_size=35, with_labels=False)
        plt.text( 0,-.1,"Highest degree: "+high_in, color="darkgreen")
        plot_count+=1
    
    plt.savefig(file_path)


def ego_plot(graph, n, file_path):
    """Draw the ego graph for a given node 'n' """
    ego_plot=plt.figure(figsize=(10,10))
    ego=nx.ego_graph(graph,n) # Get ego graph for n
    
    # Draw graph
    pos=nx.spring_layout(ego, iterations=5000)
    nx.draw_networkx_nodes(ego,pos,node_color='b',node_size=100)
    nx.draw_networkx_edges(ego,pos)
    # Create label offset
    label_pos=dict([(a,[b[0],b[1]+0.03]) for (a,b) in pos.items()])
    nx.draw_networkx_labels(ego, pos=label_pos,font_color="darkgreen")
    
    # Draw ego as large and red
    nx.draw_networkx_nodes(ego,pos,nodelist=[n],node_size=300,node_color='r', font_color="darkgreen")
    plt.savefig(file_path)
    

def getEmail(email_string):
    """Convert an email string on the type 'Ann Smith <ann.smith@email.com>'
    to only 'ann.smith@email.com'
    """
    # Need to clean up the messy CSV data to ge the graph right
    if email_string.find("<") > -1:
        email_address=re.split("[<>]",email_string)     # First, extract Address from brackets
        address_index=map(lambda x: x.find("@"), email_address) # Find where address is
        address_index=map(lambda y: y>0, address_index).index(True) 
        email_address=email_address[address_index]  # Get address string
        email_address=email_address.replace('"','') # Do final string cleaning
        return email_address.strip()
    else:
        return email_string


def graphFromCSV(file_path, create_using=nx.DiGraph()):
    """
    Create a NetworkX graph object from a csv file
    """
    # Create NetworkX object for storing graph
    csv_graph = create_using
    
    # Create reader CSV reader object from file path
    csv_file=open(file_path, "rb")
    csv_reader=csv.reader(csv_file)

    #  Add rows from CSV file as 
    for row in csv_reader:
        clean_edges=map(getEmail, row)
        csv_graph.add_edge(clean_edges[0], clean_edges[1])

    # Return graph object
    return csv_graph


def main():
    # Create a NetworkX graph object 
    gmail_graph=graphFromCSV("../email_analysis/email_graph.csv")

    # Draw entire graph
    full_graph=plt.figure(figsize=(10,10))
    nx.draw_spring(gmail_graph, arrows=False, node_size=50, with_labels=False)
    plt.savefig("../../../images/graphs/full_graph.png")
    
    # Draw ann9enigma@gmail.com's Ego graph
    ego_plot(gmail_graph, "ann9enigma@gmail.com", "../../../images/graphs/ann9enigma_ego.png")

    # Create a lattice plot of all weakly connected components
    gmail_components=nx.weakly_connected_component_subgraphs(gmail_graph)
    lattice_plot(gmail_components, "../../../images/graphs/gmail_subgraphs.png")
    

if __name__ == '__main__':
    main()

