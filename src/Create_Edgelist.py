#!/usr/bin/env python

"""
================================================
Creating Weighted Edgelists from files with text 
================================================

The most useful python tools are generalisable. Therefore, a focus throughout this script is to give the user the option to adapt the script to fit with their own text file. Luckily SpaCy and argparse can help with this mission! 

This script is therefore able to take any csv or txt file with text, extract the desired entity label, and create a weighted edgelist csv file with the column headings as they need to be for the network analysis script. The many argparse parameters are in place to give the user flexibility to make the script fit to their own preferences. 

Usage
python3 src/Create_Edgelist.py --input_path data/Blackmore_Erema_1877.txt

""" 

"""
============
Dependencies
============
"""
#system tools
import os

# Working with the text data 
import pandas as pd #dataframes
from collections import Counter  #counting occurances 
from itertools import combinations   #efficiency and creating complex combinations
from tqdm import tqdm  #informs of timing

# SpaCY (natural language processing tools) 
import spacy
nlp = spacy.load("en_core_web_sm")

#Argparse (enabling generalisability) 
import argparse 

"""
===================
Argparse Parameters
===================

"""
# Initialize ArgumentParser class
ap = argparse.ArgumentParser()
    
# Input file 
ap.add_argument("-i", "--input_path",
                type = str,
                required = True,
                help = "\n[INFO] Path to the file or directory containing text"
                       "\n[INFO] This file must be a .csv or .txt file with a column which contains text")

#Column name 
ap.add_argument("-c", "--column_name",
                type = str,
                required = False,
                default = "text",
                help = "\n[INFO] The name of the column which holds the text to be analysed"
                       "\n[INFO] This should be spelled correctly to ensure the script can find your text."
                       "\n[INFO] It should also have speech marks around it to denote that it's a string variable."
                       "\n[INFO] Psst: This is case sensitive so make sure to check if your column uses a capital letter!")

# Named entity label
ap.add_argument("-e", "--entity_label",
                type = str,
                required = False,
                default = "PERSON",
                help = "\n[INFO] Please define which named entity you're interested in extracting"
                       "\n[INFO] Options include 'DATE', 'EVENT', 'LAW', 'MONEY', 'TIME', 'WORK_OF_ART' and more."
                       "\n{INFO} A full list of label options can be found in the label scheme gere https://spacy.io/models/en"
                       "\n{INFO} But don't worry, we've set the default to 'PERSON' so this is just an optional parameter!")

# Ouput path 
ap.add_argument("-o", "--output_path",
                type = str,
                required = False,
                default = "../Output/",
                help = "\n[INFO] Path to where the weighted edgelist file will be stored"
                       "\n[INFO] The dafault is set as ../Output/")

# Filter size 
ap.add_argument("-f", "--filter_size",
                type = int,
                required = False,
                default = 500,
                help = "\n[INFO] The minimum size the edgeweight needs to be to be included in the weighted edgelist."
                       "\n[INFO] This is an integer number and will depend on how large the dataset is that you're using."
                       "\n[INFO] The default has been set to 500."
                       "\n[INFO] You should aim to have no more than ~ 150 edges included in your final list.")
    
# Parse arguments
args = vars(ap.parse_args()) 

"""
=========
Functions 
=========

"""

"""
Function to extract the entity info
"""
def extract_entities(text_df, entity_label):
    text_entities = []
    
    for text in tqdm(text_df):
        #safety check to skip over files which do not return text 
        #somefiles are not recognisable and it's better to discover this early 
        if isinstance(text, str) == False:
            print("\nThis file did not return text, I'll continue on without it") 
            #if this is the case, the file is skipped
            continue
        #create a temporary list 
        tmp_entities = []
        #create a spaCy doc object (increasing spacy's length abilities) 
        nlp.max_length = 1500000
        doc = nlp(text)
        #for every named entity 
        for entity in doc.ents: 
            #if that entity is the requested label 
            if entity.label == entity_label:
                #append it to the temporary list 
                tmp_entities.append(entity.text)
        #Append this temp list to the main list
        text_entities.append(tmp_entities) 
        
    return text_entities 


"""
Function to create the edgelist
""" 
def create_edgelist (text_entities):
    #create an empty list for the edges
    edgelist = []
    
    #loop through every entity in the text_entities
    for text in text_entities: 
        
        #use itertools.combinations to create the edgelist
        #We're using combinations of 2 edges 
        edges = list(combinations(text,2))
        
        #for each pair of 'nodes'
        for edge in edges: 
            #append this to the final edgelist
            edgelist.append(tuple(sorted(edge)))
    
    return edgelist

"""
Function to count the edges 
"""
#This function creates a dataframe from the Counter object, showing each node pair and the edge weight.
def count_edges(edgelist):
    #create an empty list for the counted edges 
    counted_edges = []
    
    #for every key and value in the edgelist items 
    for key, value in Counter(edgelist).items():
        source = key[0]
        target = key[1]
        weight = value
        #append these to the counted_edges list together 
        counted_edges.append((source, target, weight))
     
    #make this into a dataframe using pandas 
    edges_df = pd.DataFrame(counted_edges, columns=["nodeA", "nodeB", "weight"])
    
    return edges_df


"""
=============
Main Function
=============

"""
def main():
    
    print("\nHey there, let's create a weighted edgelist csv file for you to feed into a network analysis.") 
    print("\nI'll just get us all set up with the parameters you've given me...") 
    
    """
    ------------------------------------------
    Create variables with the input parameters
    ------------------------------------------
    """
    
    text_file = args["input_path"]
    column_name = args["column_name"]
    entity_label = args["entity_label"]
    filter_size = args["filter_size"]
    output_path = args["output_path"]
    
    # Create a new output directory folder if it does not already exist 
    if not os.path.exists(output_path):   
        os.mkdir(output_path) 
        
    """
    --------------------
    Pre-process the data 
    --------------------
    """
    
    #First we want to load the file as a dataframe
    #As the script can take both csv and txt files, we need to check the data is in the right format with an if else statement
    #Txt files require a bit more modelling to read the text in a way that will be easy to process and convert to a dataframe
    #The output of this part should be a dataframe called text_df which contains only the column with the text 
    
    # If the input text_file is a csv 
    if text_file.endswith(".csv"):
        #Create a pandas dataframe 
        text_df = pd.read_csv(text_file)
        #Subset only the text column from it 
        text_df = text_df[column_name]
        #print(f"This file contains {len(text_df)} lines")
        #Check to see if if the file is very large 
        if len(text_df) > 1500: 
            #downsample it to be just 1000 lines
            text_df = text_df.sample(1000)
            print("The file has been downsized to a random sample of 1000 lines") 
            
            
     
    # Else, if the textfile is a txt file 
    elif text_file.endswith(".txt"):
        #Create an empty list
        text_list = []
        #Open the text file using the open() function and name 'f'
        with open(text_file, "r", encoding = "utf-8") as f:
            #read the text in line by line 
            line = f.readline()
            #Stay on this line of text to append it individually
            while line:
                line = f.readline()
                #append this line to the list 
                text_list.append(line)
                #print(f"This file contains {len(text_list)} lines")
                #Check if the list is going to be too big 
                if len(text_list) > 1500: 
                    #Take a chunck from the beginning (to avoid any non-sensical lines at the beginning) 
                    text_list = text_list[100:1100]
                    #print("The file has been downsized to a random sample of 1000 lines")
        #rename variable
        text_df = text_list
        
    else: 
        print("\n[INFO] This file is not in the correct format. Please upload a .txt or a .csv file.") 
        
    
    
    
    """
    -------------------
    Create the edgelist 
    -------------------
    """
    print("\nGreat, the data is all processed. Now we can begin to count the edges") 
    
    #Function to create the edgelist 
    def create_edgelist (text_df, entity_label):
        
        """
        Extracting the entities
        """
        #Create an empty list for the text entities
        text_entities = []
        for text in tqdm(text_df):
            #create temporary list to store to 
            tmp_entities = []
            #create a spaCy doc object
            nlp.max_length = 1500000
            doc = nlp(text)
            #for every named entity 
            for entity in doc.ents: 
                #if that entity is the requested label 
                if entity.label == entity_label:
                    #append it to the temporary list 
                    tmp_entities.append(entity.text)
            #Append this temp list to the main list
            text_entities.append(tmp_entities) 
            
            print("\nI've extracted the entities. I'm now creating the edgelist...")
         
        
        """
        Creating the edgelist
        """
        #create an empty list for the edges
        edgelist = []
    
        #loop through every entity in the text_entities
        for text in text_entities: 
        
            #use itertools.combinations to create the edgelist
            #We're using combinations of 2 edges 
            edges = list(combinations(text,2))
        
            #for each pair of 'nodes'
            for edge in edges: 
                #append this to the final edgelist
                edgelist.append(tuple(sorted(edge)))
                
        print("\nThe edgelist has been created. Now we can count the edges")
                
        """
        Count the edges
        """
        #create an empty list for the counted edges 
        counted_edges = []
    
        #for every key and value in the edgelist items 
        for key, value in Counter(edgelist).items():
            source = key[0]
            target = key[1]
            weight = value
            #append these to the counted_edges list together 
            counted_edges.append((source, target, weight))
     
        #make this into a dataframe using pandas 
        edges_df = pd.DataFrame(counted_edges, columns=["nodeA", "nodeB", "weight"])
        
        print(f"\nCounting complete. There are {len(counted_edges)} edges detected.") 
        print("\nNow we'll filter them to keep only the most important ones")
        
        return edges_df
    
    """
    -------------------
    Filter the edgelist 
    -------------------
    """    
    
    #Filter the edgelist based on the edgeweight
    filtered_edgelist = edges_df[edges_df["weight"]> filter_size]
    
    """
    -----------------
    Save the edgelist 
    -----------------
    """
    
    #Save this subset of filtered edges as a csv file
    output_path = os.path.join(output_path, "weighted_edgelist.csv")
    filtered_edgelist.to_csv(output_path, index = False)
    
    print("Your edgelist is ready to be fed in for some network analysis!") 
    
    
if __name__=="__main__":
    #execute main function
    main()    
    