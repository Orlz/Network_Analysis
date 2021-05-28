[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![describtor - e.g. python version](https://img.shields.io/badge/Python%20Version->=3.6-blue)](www.desired_reference.com) ![](https://img.shields.io/badge/Software%20Mac->=10.14-pink)

# Network Analysis 

## Creating reusable network analysis pipelines 


<div align="center"><img src="https://github.com/Orlz/CDS_Visual_Analytics/blob/main/Portfolio/networking.png"/></div>

Network analysis is at the centre of so much of what we do here in language analytics. In simple terms, a network refers to a system of objects which are connected to one another through links (or relationships). The objects of the network are known as ‘nodes’ and can represent anything from a person, to a word, to a school of thought. The links that connect the objects are referred to as ‘edges’ – which can be as simple as a one directed relationship connecting two nodes, or a complex web of shared connections and links.

Network analysis tends to focus on the visualisation of networks, which often overshadows the arguably more interesting centrality metrics which can be calculated within a network. This assignment considers both the visualisation and centrality metrics in equal measures, and builds scripts which can be used to conduct simple network analysis on any csv or txt file with a column of text.  

## Table of Contents 

- [Assignment Description](#Assignment)
- [Scripts and Data](#Scripts)
- [Methods](#Methods)
- [Operating the Scripts](#Operating)
- [Discussion of results](#Discussion)

## Assignment Description

**Creating reusable network analysis pipelines**

In this assignment we were asked to build pipelines which could be used to conduct a simple network analysis, using a given dataset with the columns “nodeA” and “nodeB”. The networks were to be based on entities appearing together in documents. 

The assignment asked us to complete the following steps: 
1. Create a script which is able to run from the command line 
2. The script should be able to take any weighted edge list as input 
3. It should then create a network graph and save it into an output folder 
4. It should also create a data frame showing the degree, betweenness and eigenvector centrality for each node. This should be saved in the output folder also. 

**Purpose of the assignment:**

This assignment is designed to test that you have an understanding of:
1.	how to create command-line tools with python 
2.	how to perform network analysis using networkx 
3.	how to create reusable and reproducible pipelines for network analysis 

**Personal focus of the assignment:**

For this assignment, I wanted to focus on the idea that “the most useful tools are generalisable”. Therefore, I saw the network analysis as an opportunity to focus on reproducibility and consider how to produce scripts which can be used across different datasets. To do this, I added an additional script named “Create_Edgelist.py” which is able to take any txt or csv file, enable any SpaCy entity label and turn it into a weighted edge list with the column headings needed for the main script, “network_analysis.py”. I also focused on the communicative element of the script and tried to find a better way to visualise the network. 


## Scripts and Data

**Scripts**

There are 2 scripts which can be found in the src folder: 

| Script | Description|
|--------|:-----------|
Create_Edgelist.py| Takes any txt or csv with a text column and creates a weighted edglist csv   
network_analysis.py | Takes our weigthed edgelist file and runs a simple network analysis on it to calculate the node centrality measures and create visualisations.

**Data**

The user is welcome to use any txt or csv file which contains text. There have been two sample datasets provided in the data folder: the fake_or_real_news.csv which was used for the original analysis, or Blackmore's 'Erema'. 

_Sample datasets included in the data folder_


| Script | Description|
|--------|:-----------|
fake_or_real_news.csv| News headlines which were used to make the original network analysis    
Blackmore_Erema_1877.txt | The txt file copy of the novel 'Erema' from 1877
weighted_edgelist.csv | a ready-made weighted edgelist file if the user wishes to skip te Create_Edgelist.py script.


## Methods 

A network can be considered in a number of ways and differs greatly between contexts in terms of size (the number of nodes within the network) and density (the connectivity within the network). There are however quantitative metrics which help us to bring some understanding to the vast field of network theory, these metrics are as follows and are calculated for each node in the network:

```
Metric                 |  Description                
 ----------------------| --------------------             
Eigenvector Centrality |  a measure of how well connected the node is to other well connected nodes in the network,
                       |  i.e., how important is the node to the network? 
Betweenness centrality |  a measure of how much the node connects other nodes within the network,              
                       |  i.e., how much is this node enabling the flow of communication?                   
Degree centrality      |  a measure of how many edges connect the node to other nodes                    
```


By considering the visual display of a network and the centrality metrics which belong to each node together, we can begin to build quite complex insights on top of a fairly simple theoretical foundation – that in one way or another, everything can be considered as either a node or an edge, connected together. 

#### Creating the weighted edgelist 

To create the edge list csv, the file containing text was processed with the following steps: 
1.	Determine whether the file is a csv or text file and load it accordingly as a data frame with one column containing text 
2.	Extract the desired entity label by firstly running the text through the Spacy nlp pipeline, which assigns each word its entity label, and then looping through the text to extract all the named entities of the desired label and appending them into an empty list 
3.	Create the edgelist by looping through the entity list and using itertools.combinations() to create combinations of 2 edges 
4.	Count the edges using Counter() and store the source, target, and weight value into new empty lists 
5.	Combine these three lists into a dataframe whereby the source = nodeA, the key = nodeB, and the weight = the weight column in the output csv file. 
6.	Filter the edgelist data frame to contain only edges with a weight above the defined minimum value (filter_size)
7.	Save the filtered edgelist as a csv file. 

The output file contains three columns of nodes and their associated edge weights, filtered to include only those considered to be large enough to make it into the network. This reduces noise within the network, enabling better visualisation. 

#### Network Analysis 

The network was created by using networkx, which is a package commonly used in research for the creation and study of networks. More information on the package can be found [here](https://networkx.org/)

The weighted edgelist file was loaded into the script and passed to networkx, which processed the nodes and calculated the degree, betweenness, and eigenvector centrality metrics for each. Three plots were then created with the help of pygraphviz: 

```
Metric                 |  Description                
 ----------------------| --------------------             
pygraphviz_plot.png    |  A plot with a weblike structure, similar to the one constructed in class 
egograph_plot.png      |  An ego graph with the most connected node at the centre of the visualisation                           
circular_plot.png      |  A circular style visualisation to visualise the links between nodes more clearly                
```


## Operating the Scripts

***1. Clone the repository***

The easiest way to access the files is to clone the repository from the command line using the following steps 

```bash
#clone repository
git clone https://github.com/Orlz/Network_Analysis.git
```

***2. Upload your data*** (_Optional_) 

If the user would like to use their own data, this must be uploaded into the working directory. It is recommended to add this into the data folder. 

Alternatively, the user is welcome to skip the first script and continue on using the already created weighted edgelist. 


***3. Create the virtual environment***

You'll need to create a virtual environment which will allow you to run the script using all the relevant dependencies. This will require the requirements.txt file attached to this repository. 


To create the virtual environment you'll need to open your terminal, navigate to the directory, and type the following code: 

```bash
bash create_virtual_environment.sh
```
And then activate the environment by typing:

```bash
$ source language_analytics02/bin/activate
```

***4. Run the Script***

There are two scripts to be run for this assignment, the first is _optional_

#### Create_Edgelist.py

(parameters = 5, required = 1) 

```
Letter call  | Parameter        | Required? | Input Type     | Description                                         
-----------  | -------------    |--------   | -------------  |                                                     
`-i`         | `--input_path`   | Yes       | String         | Path to where the text file is stored.               
`-c`         | `--column_name`  | No        | String         | Name of the column which contains the txt (for csv)  
`-e`         | `--entity_label` | No        | String         | The SpaCy entity label to be extracted and analysed          
`-o`         | `--output_path`  | No        | String         | The path to where the output should be stored   
`-f`         | `--filter_size`  | No        | Integer        | The minimum edgelist weight to be included 
```

**Usage**

```bash
$ python3 src/Create_Edgelist.py --input_path real_or_fake_news.csv
```     

#### network_analysis.py 

(parameters = 3, required = 0) 

```
Letter call  | Parameter              | Required? | Input Type     | Description                                         
-----------  | ---------------------- |--------   | -------------  |                                                     
`-e`         | `--edgelist_file`      | No        | String         | Path to where the text file is stored.                      
`-o`         | `--output_path`        | No        | String         | The path to where the output should be stored   
`-m`         | `--minimum_edgeweight` | No        | Integer        | The minimum edgelist weight threshold
```


**Usage**

```bash
$ python3 src/network_analysis.py
```

## Discussion of Results 

Focusing in on our network analysis, we encounter the difficulties of visualising networks with a large number of nodes included. Put simply, they can be hard to interpret. This only increases the need for a focus on centrality measures alongside the visualisation, because limiting nodes to only a few takes away from the usefulness of the network and can lead to shallow representations. We often don’t want to reduce out network down to only a few key people, because the real beauty of networks is in their vast inclusion. We do however want to know who the key people are, how central they are to the network, and in what way do they play a part in the network. This is what centrality measures tell us. Let's take a look at some of the more interesting nodes: 

| Node | Degree| Betweenness| Eigenvector | 
|--------| -----------|-----------| :-----------|
Clinton| 0.79 |0.73 | 0.54
Donald Trump|	0.16 |	0.012 | 	0.26
Obama	| 0.08 | 	0.0| 	0.16 

We'll consider some of the US political figures... Here we see that Clinton scores the highest across all three centrality metrics. He/she is well connected to other important nodes (eigenvector), enables the flow of communication among the other nodes around it (betweenness) and is connected in general to many other nodes (degree). On the otherhand, we have Obama, who scores fairly highly on being connected to other important nodes within the network (eigenvector), but does not appear to be enabling much communication, indicating that he is not at the centre of the network and more in a space of his own. We should take these results with a pinch of salt, as the network was created using a combination of real and fake headlines, but it is interesting to demonstrate how even very important characters to the network such as Obama in reality are not as central as they might seem. 

**Visualisations** 
<div align="center"><img src="https://github.com/Orlz/Network_Analysis/blob/main/Output/pygraphviz_plot.png"/></div>

Our network here was filtered with a light-weight value of 500 or above, which still left 169 people connected together. Some of these people are highly connected, with their names frequently occurring together, such as the Clintons, who appear at the centre of the network. Others such as “Scalia” float on their own, disconnected from all the other nodes. Closer inspection brings to light a common problem in simple network analysis such as this - we see that the word ‘Clinton’ is represented as a number of separate nodes within the network. We have the “Clinton” node right at the centre, which could represent either Hilary or Bill, however we also have the names “Hilary”, “Clintons”, “Bill”, and “Bill Clinton”, all as separate nodes. This is a problem, because we’re misrepresenting people and the edges between these 5 separate nodes are not truly reflecting the strength of these edges and are hard to interpret who they really mean. This could be filtered out with some additional pre-processing of the data, but for a generalisable script we want to be able to pre-process the data in the same way each time. Not every dataset we want to analyse will need to specifically label the Clinton’s (thank goodness!) but they will need to be accurately represented in the data. These examples only highlight one of the true struggles with language analytics, that creating generalisable scripts can be something of a difficult task because the context of language can be so varied!


___Teaching credit___ 

Many thanks to Ross Deans Kristiansen-McLachlen for providing an interesting and supportive venture into the world of Language Analytics! 

<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>



