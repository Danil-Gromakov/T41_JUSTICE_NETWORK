#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import networkx as nx
import matplotlib.pyplot as plt
import collections


# In[2]:


G = nx.Graph()


# In[3]:


coordinats = {}

with open('lat_lon_US.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        
        name = row["Place Name"].split(",")[0].replace("State","").strip()
        coordinats[name] = (float(row["Latitude"]),float(row["Longitude"]))
       


# In[4]:


with open('TrumpProsecutors.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    n= 0
    for row in reader:
        n +=1
        id = n 
        
        #To prepare name of District to be able use like key for coordinats dict
        #To make these equal
        
        District = row['District'].split("of")
        District = District[-1].replace("U.S. Attorney for the S.D.","").replace("State","").strip()

        #To make list of nodes
        
        G.add_node(id,name = row['Attorney'],
                   District=District,
                   Full_name = row['District'],
                   Date_Appointment = row['Date of Appointment'],
                   End_Date = row['End Date'],
                   Barr_Appointment = row['Barr Appointment'])
        


# In[5]:


list_Districts = []

 

for d in G.nodes.data():
    
    list_Districts.append(d[1]["District"])
    
list_single_distr = set(list_Districts)

#To find count of connections
list_count = collections.Counter(list_Districts)


# In[6]:


#To make edges for network and add lat,lon, count of conections

list_temp = []

for i in list_single_distr:
    list_temp = []
    for d in G.nodes.data():
        if i == d[1]["District"]:
            list_temp.append(d[0])
   
    for n in list_temp:

        if list_temp[0] != n:
            G.add_edge(list_temp[0],n)
            
        elif list_temp[0] == n:
            G.add_edge(list_temp[0],78)#Washington

            G.nodes[list_temp[0]]["count"] = list_count[i]
            G.nodes[list_temp[0]]["lat"] = coordinats[i][0]
            G.nodes[list_temp[0]]["lon"] = coordinats[i][1]


 


# In[7]:


#optional

for d in G.nodes.data():
    deegre = G.degree[d[0]]
    adj = list(G.adj[d[0]])
    #print(adj)


# In[8]:


"""plt.figure(figsize=(10,9))
pos = nx.random_layout(G)
nx.draw_networkx(G, pos)
"""


# In[9]:


nx.write_gexf(G, "TrumpProsecutors_network.gexf")

