#!/usr/bin/python

"""
================================================
Network Analysis on a Weighted Edgelist
================================================

This script takes our weigthed edgelist csv file (created with the Create_edgelist.py script) and runs a simple network analysis
on it to calculate the node centrality measures and create a simple network visualisation. 

The script will save 3 visualisation plots as png's into the Output folder, as well as a csv file containing the computed
centrality metrics for the network.


Usage
python3 src/network_analysis.py 

""" 

"""
============
Dependencies
============
"""
# System tools
import os
import sys
import argparse
from operator import itemgetter

# Data analysis
import pandas as pd

# drawing
import networkx as nx
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,20)



"""
===================
Argparse Parameters
===================

"""
# Initialize ArgumentParser class
ap = argparse.ArgumentParser()
    
# Input file 
ap.add_argument("-e", "--edgelist_file",
                type = str,
                required = False,
                default = "data/weighted_edgelist.csv",
                help = "\n[INFO] Path to the file or directory containing text"
                       "\n[INFO] This file must be a .csv file which contains columns for 'nodeA', 'nodeB' and 'weight'.")

# Ouput path 
ap.add_argument("-o", "--output_path",
                type = str,
                required = False,
                default = "Output/",
                help = "\n[INFO] Path to where the weighted edgelist file will be stored"
                       "\n[INFO] The dafault is set as Output/")

ap.add_argument("-m", "--minimum_edgeweight", 
                required=False, 
                type=int,
                default=500,
                help="[INFO] The minimum edge weight threshold of interest") 
                


# Parse arguments
args = vars(ap.parse_args()) 

"""
=============
Main Function 
=============

"""

def main():
    
    print("\nHi again! Let's get you set up to do some network analysis.") 
    print("\nI'm going to take the weighted_edglist you gave me and create a network plot with centralitity metrics")
    print("\nThese will be saved into your Output folder, or another folder defined by yourself!")
    
    
    """
    ------------------------------------------
    Create variables with the input parameters
    ------------------------------------------
    """
    
    edgelist = args["edgelist_file"]
    minimum_edgeweight = args["minimum_edgeweight"]
    output_path = args["output_path"]
    
    # Create a new output directory folder if it does not already exist 
    if not os.path.exists(output_path):   
        os.mkdir(output_path)
        
    """
    --------------------------------------------
    Filter the weights to the minimum edgeweight
    --------------------------------------------
    """
   
    print("\nI'm just checking your minimum edgeweight") 
        
    #Load in the data 
    edges_df = pd.read_csv(edgelist)
    
    #Check to see if the data has already been filtered to the desired minimum edgeweight
    #This is a safety check in case someone is using a dataset which has not been created with Create_edgelist.py script
    #if edges_df["weight"] > minimum_edgeweight: 
        #Filter the edges to the desired weight 
        #filtered_df = edges_df[edges_df["weight"] > minimum_edgeweight]
        
    #else: 
    filtered_df = edges_df
    
    """
    ----------------
    Prepare the plots
    ----------------
    """
    
    print("\nLooks good! Now we'll create the plots...")
    print("\nThere will be 3 of these, one we worked in in class, one ego graph, and one plotted in a circular design")
    
    #Create a G variable to work with networkx 
    G=nx.from_pandas_edgelist(filtered_df, 'nodeA', 'nodeB', ["weight"])
    
    """
    First plot 
    """
    #Call pygraphviz
    pos = nx.nx_agraph.graphviz_layout(G, prog="neato")
    
    #Draw the plot with the node labels included in small font 
    nx.draw(G, pos, with_labels=True, node_size=20, node_color ="c", font_size=12)
    
    #Save the plot
    plot1_output = os.path.join(output_path, "pygraphviz_plot.png")
    plt.savefig(plot1_output, dpi=80, bbox_inches = "tight")
    
    print("\nFirst plot complete") 
    
    """
    Second plot
    """
    #Here we'll create an ego graph with the node with the most connections at the centre to see who is at the hub of this network
    
    #Find node with largest degree 
    node_and_degree = G.degree()
    (largest_hub, degree) = sorted(node_and_degree, key=itemgetter(1))[-1]
    
    #Create graph of this node 
    ego_graph = nx.ego_graph(G, largest_hub)
    
    #Draw the graph with spring layout
    pos = nx.spring_layout(ego_graph)
    nx.draw(ego_graph, pos, node_color="b", node_size=50, with_labels=True)
    
    #Save plot 
    plot2_output = os.path.join(output_path, "egograph_plot.png")
    plt.savefig(plot2_output, dpi=80, bbox_inches = "tight")
    
    print("\nSecond plot complete") 
    
    """
    Third plot
    """
    #This is just an alternative way to draw the network using a circular layout - but is not always so interpretable 
    
    #Create graph
    nx.draw_circular(G, with_labels = True, font_weight= 'bold')
    
    #Save the graph 
    plot3_output = os.path.join(output_path, "circulargraph_plot.png")
    plt.savefig(plot3_output, dpi=80, bbox_inches = "tight")
    
    print("\nThird plot complete")
    
    
    """
    -------------------
    Centrality Measures 
    -------------------
    """
    
    print("\nNow I'll calculate the centrality measures")
    
    #Calculate the centrality measures using networkx 
    degree_value = nx.degree_centrality(G) #degrees 
    betweenness_value = nx.betweenness_centrality(G) #betweenness 
    eigenvector_value = nx.eigenvector_centrality(G) #eigenvector
    
    # Saving these values into a dataframe (centrality_measures_df) 
    centrality_measures_df = pd.DataFrame({
        'degree':pd.Series(degree_value),
        'betweenness':pd.Series(betweenness_value),
        'eigenvector':pd.Series(eigenvector_value)  
    }).sort_values(['degree', 'betweenness', 'eigenvector'], ascending=False)
    
    # saving the csv file
    centrality_outpath = os.path.join(output_path, "centrality_measures.csv") 
    centrality_measures_df.to_csv(centrality_outpath)
    
    print(f"All done - that's you finished! Head over to {output_path} to see the results!") 
    
    
if __name__=="__main__":
    #execute main function
    main()    
        
    

    
    
    
        
   
