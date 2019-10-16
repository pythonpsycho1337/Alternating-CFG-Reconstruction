import os, sys, networkx, angr

from angr.knowledge_plugins.cfg.cfg_node import CFGENode
from angrutils import plot_cfg

def main(file,outputDirectory):
    p = angr.Project(file,load_options={'auto_load_libs': False})

    print("Loading BBG from angr..")
    cfgEmulated = p.analyses.CFGEmulated()

    print("Converting the BBG to a CFA")
    
    #Create a CFA from the BBG provided obtained with angr
    CFA = networkx.DiGraph()
    for node in list(cfgEmulated.graph.nodes.keys()):
        if (node.is_simprocedure):
            continue

        CFA.add_node(hex(node.addr))

        prev = None
        for blockNode in node.instruction_addrs:
            CFA.add_node(hex(blockNode))
            if (prev != None):
                CFA.add_edge(hex(prev),hex(blockNode))
            prev = blockNode

        #Prev will now be the last instruction in the block
        last = prev
        if (last == None):
            last = node.addr

        #Add edges from last instruciton in each block to the entry of suceeding blocks
        successors = getNonSimprocedureSuccessors(node)
        for successor in successors:
            CFA.add_edge(hex(last),hex(successor.addr))

    #Output resulting graph in a .dot file
    basename = os.path.basename(file)
    networkx.drawing.nx_pydot.write_dot(CFA, outputDirectory + "/" + basename + "_ccfa_angr.dot")

    #Illustrate the BBG as a PNG
    plot_cfg(cfgEmulated, os.path.abspath(outputDirectory+"/"+basename))

    #Export the CFA as a networkx edgelist
    #networkx.readwrite.edgelist.write_weighted_edgelist(CFA, os.path.abspath(outputDirectory+"/"+basename+".nx"), delimiter=",")

#Returns the set of all successors that are not simprocedures
#Note that it skips every simprocedure node until a non-simprocedure node is found
def getNonSimprocedureSuccessors(node):
    answer = []
    for s in node.successors:
        if not s.is_simprocedure:
            answer.append(s)
        else:
            answer += getNonSimprocedureSuccessors(s)
    return answer

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 generateCFA.py [binary] [output directory]")
    else:
        main(sys.argv[1],sys.argv[2])