#/usr/bin/python

#     Message Passing Algoritm Implementation for Sum-Product:
#     Written by: Ramezan Paravi

import numpy as np 
import sys
import itertools
from numpy import prod
from collections import deque
import pydotplus
import matplotlib.pyplot as plt

import networkx as nx



# function f: Returns f(x, [x_1,x_2,...,x_j])  of a factor node
def f(x,y):
        return (x+ sum(y))%7

#class of factor grpah which consists of factor nodes and variable nodes
class FactorGraph:
    def __init__(self):
        self.FacNodeList=[] #factor nodes list
        self.VarNodeList=[] #variable node list
        self.NodeList=[] # all nodes together

        self.VarLabels=[] # label of variable nodes
        self.FacLabels=[] # label of factor nodes

        self.NumFacNode=0
        self.NumVarNode=0

        self.NumEdges=0


#****************************************************************************************************

    def AddVarNode(self, label, alphabet_size=2):
        self.NumVarNode=self.NumVarNode+1
        self.VarLabels.append(label)
        if len(self.VarLabels) != len(set(self.VarLabels)):
            print "Variable nodes have repeated items."
            sys.exit()
        else:
            newNode=VarNode(label,"var", alphabet_size) # creates an instance of cariable node
            self.VarNodeList.append(newNode)
            return newNode

#****************************************************************************************************

    def AddFactorNode(self,label,var_list):
        self.NumFacNode=self.NumFacNode+1
        self.FacLabels.append(label)
        if len(self.FacLabels) != len(set(self.FacLabels)):
            print "Factor nodes have repeated items."
            sys.exit()
        else:
            for l in var_list:
                if not (l in self.VarLabels):
                    print "Unknown variable in " + label
                    sys.exit()
            newNode=FacNode(label,"factor", var_list)
            self.FacNodeList.append(newNode)
            return newNode

#****************************************************************************************************
    
    def FindVarNode(self,ID):
        for w in self.VarNodeList:
            if w.NodeLabel==ID:
                return w

    def FindVarNodeIndex(self,ID):
            for i in range(0,len(self.NodeList)):
                if self.NodeList[i].NodeLabel==ID:
                    return i


#*****************************************************************************************************

    def BuildGraph(self):
        for w in self.FacNodeList:
            for ID in w.NeighLabels:
                self.NumEdges=self.NumEdges+1
                t=self.FindVarNode(ID)
                w.NeighList.append(t)
                t.NeighList.append(w)
        self.NodeList.extend(self.VarNodeList)
        self.NodeList.extend(self.FacNodeList)


    def is_tree(self):
        if self.NumEdges==len(self.NodeList)-1:
            return True
        else:
            return False
#******************************************************************************************************
    def TopBotMessagePassing(self,ID):
        for s in self.NodeList:
            s.color='w'
            s.pi=[]
            s.visit_index=[]
           
        s=self.FindVarNode(ID)
        s.color='g'
        s.back_message=[]
        if s.leaf_index==1:
            s.back_message.append([1]*len(s.alphabet))
        else:
            l=len(s.alphabet)
            for w in s.NeighList:
                temp=[0]*l
                for i in range(0,l):
                    temp[i]=1
                    for element in itertools.product(s.NeighList):
                        if (element[0]!=w):
                            temp[i]=temp[i]*element[0].message[i]           
                s.back_message.append(temp)
                s.visit_index.append(w.NodeLabel)
                #print "message sent from " + s.NodeLabel + " to " + w.NodeLabel + " is : " + str(temp)

        print "Marginal of node "+ s.NodeLabel+" is: " + str(s.marginal)

        Q=deque([s])
        while len(Q)>0:
            u=Q.popleft()
            for v in u.NeighList:
                if v.color=='w':
                    if (v.NodeType=="factor" and v.leaf_index==0):
                        v.back_message=[]
                        for p in v.NeighList:
                            if p!=u:
                                l=len(p.alphabet)
                                all_alphabets=[]
                                all_back_messages=[]
                                for element in itertools.product(v.NeighList):
                                    if element[0]!=p:
                                        all_alphabets.append(element[0].alphabet)
                                    if element[0]==u:
                                        desired_index=u.visit_index.index(v.NodeLabel)
                                        all_back_messages.append(element[0].back_message[desired_index])
                                    elif element[0]!=p:
                                        all_back_messages.append(element[0].message)
                                cartesian_alphabets=list(itertools.product(*all_alphabets))
                                cartesian_messages=list(itertools.product(*all_back_messages))
                                temp=[]
                                for j in range(0,l):
                                    temp.append(0)
                                    for k in range(0,len(cartesian_messages)):
                                        temp[j]=temp[j]+f ( p.alphabet[j] , cartesian_alphabets[k] )*prod(cartesian_messages[k])
                                v.back_message.append(temp)
                                v.visit_index.append(p.NodeLabel)
                                #print "message sent from " + v.NodeLabel + " to " + p.NodeLabel + " is : " + str(temp)

                                #Computing Marginals
                                
                                if p.leaf_index==1:
                                    p.marginal.extend(temp)
                                    print "Marginal of node "+ p.NodeLabel+" is: " + str(p.marginal)
                                else:
                                    
                                    l=len(p.alphabet)
                                    p.marginal=[0]*l
                                    for q in p.NeighList:
                                        for i in range(0,l):
                                            p.marginal[i]=1
                                            for element in itertools.product(p.NeighList):
                                                if element[0]==v:
                                                    p.marginal[i]=p.marginal[i]*temp[i]
                                                else:
                                                    p.marginal[i]=p.marginal[i]*element[0].message[i]
                                    print "Marginal of node "+ p.NodeLabel+" is: " + str(p.marginal)
                                   

                    elif (v.NodeType=="var" and v.leaf_index==0):
                        v.back_message=[]
                        l=len(v.alphabet)
                        for p in v.NeighList:
                            temp=[0]*l
                            if p!=u:
                                for i in range(0,l):
                                    temp[i]=1
                                    for element in itertools.product(v.NeighList):
                                        if (element[0]==u and element[0]!=p):
                                            desired_index=u.visit_index.index(v.NodeLabel)
                                            temp[i]=temp[i]*element[0].back_message[desired_index][i]
                                        elif element[0]!=p:
                                            temp[i]=temp[i]*element[0].message[i]
                                v.back_message.append(temp)
                                v.visit_index.append(p.NodeLabel)
                    v.color='g'
                    v.pi.append(u)
                    Q.append(v)
            u.color='b'

#***********************************************************************************************************
    def GraphReset(self):
        for s in self.NodeList:
            s.color='w'
            s.childs=[]
            s.pi=[]
            s.leaf_index=0
        for s in self.VarNodeList:
            s.marginal=[]

    def BotTopMessagePass(self,L,G):
        self.GraphReset()
        for s in self.NodeList:
            if s.color=='w':
                self.BotTopMessagePassVisit(s,L,G)

    def BotTopMessagePassVisit(self, u,L,G):
        u.color='g'
        G.add_node(u.NodeLabel)
        for v in u.NeighList:
            if v.color=='w':
                G.add_edge(u.NodeLabel,v.NodeLabel)
                v.pi.append(u)
                u.childs.append(v)
                self.BotTopMessagePassVisit(v,L,G)

        u.color='b'

        if (len(u.NeighList)==1 and self.FindVarNodeIndex(u.NodeLabel)!=0):
                u.leaf_index=1
                if u.NodeType=="var":
                    u.message=[1]*len(u.alphabet)
                if u.NodeType=="factor":
                    for x in u.pi[0].alphabet:
                    	u.message.append(f(x,[0]))
        else:
                if u.NodeType=="var":
                    u.message=[0]*len(u.alphabet)
                    for i in range(0,len(u.alphabet)):
                        u.message[i]=1
                        for w in u.childs:
                            u.message[i]=u.message[i]*w.message[i]

                if u.NodeType=="factor":
                    l=len(u.pi[0].alphabet)
                    u.message=[0]*l
                    all_alphabets=[]
                    all_messages=[]
                    for element in itertools.product(u.childs):
                        all_alphabets.append(element[0].alphabet)
                        all_messages.append(element[0].message)
                    cartesian_alphabets=list(itertools.product(*all_alphabets))
                    cartesian_messages=list(itertools.product(*all_messages))
                    for j in range(0,l):
                        u.message[j]=0
                        for k in range(0,len(cartesian_messages)):
                            u.message[j]=u.message[j]+f ( u.pi[0].alphabet[j] , cartesian_alphabets[k] )*prod(cartesian_messages[k])
        

        # if u.NodeLabel!=self.NodeList[0].NodeLabel:
        #     G.add_edge(u.NodeLabel,u.pi[0].NodeLabel,label=u.message)  
        if self.FindVarNodeIndex(u.NodeLabel)==0:
            u.marginal=u.message
        if L=="print":
            if self.FindVarNodeIndex(u.NodeLabel)!=0:
                print "Message from " + u.NodeLabel +" to " + u.pi[0].NodeLabel +" is: " + str(u.message)
            else:
                print "Marginal of root node "+ u.NodeLabel +" is: " + str(u.message)
                
           



#**********************************************************************************************************
    def Marginal(self,s,L=""):
        if self.is_tree()==False:
            print "The Graph is not tree."
            sys.exit()
        else:
            if not (s in self.VarLabels):
                print "Error: " + s+" is not a variable node"
                print "Provide a variable node."
                sys.exit()


        #Dangle Tree Data Structure From Node s 
        root_index=self.FindVarNodeIndex(s)
        self.NodeList[0], self.NodeList[root_index]=self.NodeList[root_index],self.NodeList[0]
        self.VarNodeList[0], self.VarNodeList[root_index]=self.VarNodeList[root_index],self.VarNodeList[0]
        if L=="print":
            print "Root is: " + s
        G=nx.DiGraph()
        self.BotTopMessagePass(L,G)
        
        # edge_labels=dict([((u,v,),d['label'])
        #         for u,v,d in G.edges(data=True)]) 
        #pos=nx.graphviz_layout(G,prog="neato",rankdir='LR')
        pos=nx.spring_layout(G)
        nx.draw_networkx_nodes(G,pos,node_size=500,nodelist=self.VarLabels,node_shape='o',node_color="r", alpha=1.0)
        nx.draw_networkx_nodes(G,pos,node_size=500,nodelist=self.FacLabels,node_shape='s',node_color="y", font_color='w')
        nx.draw_networkx_edges(G,pos,width=2,arrows=False, style='solid',alpha=0.5,edge_color='b')
        #nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_size=10,font_family='sans-serif')
        nx.draw_networkx_labels(G,pos)
        
        plt.axis('off')
        if True:
            plt.show()

        #Dangle Back Data Structure From Node s 
        self.NodeList[0], self.NodeList[root_index]=self.NodeList[root_index],self.NodeList[0]
        self.VarNodeList[0], self.VarNodeList[root_index]=self.VarNodeList[root_index],self.VarNodeList[0]

    def All_Marginals(self):
        if self.is_tree()==False:
            print "The Graph is not tree."
            sys.exit()
        print ""
        print "All marginals in the factor graph:"    
        G=nx.DiGraph()
        self.BotTopMessagePass("",G)
        self.TopBotMessagePassing(self.NodeList[0].NodeLabel)
        

#***********************************************************************************************************************************************


class VarNode:
    def __init__(self, label, NodeType, alphabet_size=2 ):
        self.NodeType=NodeType
        self.NodeLabel=label
        self.NeighList=[]
        self.alphabet=range(1,alphabet_size+1)
        self.message=[]
        self.marginal=[]
        self.back_message=[]

        # Traverse Purpose Attributes
        self.color='w'
        self.pi=[]
        self.childs=[]
        self.leaf_index=0
        self.visit_index=[]
        



#***********************************************************************************************************************************************

class FacNode:
    def __init__(self, label, NodeType, var_list):
        self.NodeType=NodeType
        self.NodeLabel=label
        self.NeighLabels=var_list
        self.NeighList=[]
        self.message=[]
        self.back_message=[]

        # Traverse Purpose Attributes
        self.color='w'
        self.pi=[]
        self.childs=[]
        self.leaf_index=0
        self.visit_index=[]

#***************************************************************************************************

# Main Function

def main():
    #Constructs an instance of factor graph
    T=FactorGraph()
    # Add variable nodes: AddVarNode(label, alphabet size)
    T.AddVarNode("x1", 2)
    T.AddVarNode("x2", 2)
    T.AddVarNode("x3", 2)
    T.AddVarNode("x4", 3)
    T.AddVarNode("x5", 2)
    T.AddVarNode("x6", 2)
    T.AddVarNode("x7", 2)
    T.AddVarNode("x8", 3)


    #add factor nodes: AddFstorNode(label, [adjacent var nodes]) 
    T.AddFactorNode("f1",["x1","x2","x3"])
    T.AddFactorNode("f2",["x3","x4","x6"])
    T.AddFactorNode("f3",["x4","x5","x7","x8"])

    # Build Factor Graph
    T.BuildGraph()

    #Checks if there is loop in the bipartite factor graph or the factor graph is diconnected.
    T.is_tree() 

    #Returns marginal for a specific variable node and prints the path
    T.Marginal("x4","print")


    #Returns all marginals at the same using a bottom-top and a top-bottom round of message propagation 
    T.All_Marginals()


if __name__ == '__main__':
    main()