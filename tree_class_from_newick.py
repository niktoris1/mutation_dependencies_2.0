from treelib import Tree
import re
import logging # a workaround to kill warnings
logging.captureWarnings(True)

def MakeTreeClassTree(newick_file_name, dict_name_muts = None, dict_name_times = None, dict_name_types = None):
    def parse(newick):
        tokens = re.finditer(r"([^:;,()\s]*)(?:\s*:\s*([\d.]+)\s*)?([,);])|(\S)", newick + ";")

        def recurse(nextid=0, parentid=-1):  # one node
            thisid = nextid
            children = []

            name, length, delim, ch = next(tokens).groups(0)
            if ch == "(":
                while ch in "(,":
                    node, ch, nextid = recurse(nextid + 1, thisid)
                    children.append(node)
                name, length, delim, ch = next(tokens).groups(0)
            return {"id": thisid, "name": name, "length": float(length) if length else None,
                    "parentid": parentid, "children": children}, delim, nextid

        return recurse()[0]

    file = open(newick_file_name, "r")
    text_newick = file.read()
    raw_nodes = parse(text_newick)

    name_id_dict = {} # dictionary in type id: name

    def add_children(some_tree, node): #adds all children to the tree by checking all parent ids
        if node["parentid"] is not None:
            node_name = re.split('\|', node["name"])[0]
            some_tree.create_node(node_name, node["id"], parent=node["parentid"],
                                  data=NodeWithData(dict_name_muts[node_name],
                                                    dict_name_times[node_name],
                                                    dict_name_types[node_name]))
        else:
            raise ValueError("The head vertex supposed to be added manually")
        name_id_dict[node_name] = node["id"]
        for child_node in node["children"]:
            add_children(some_tree, child_node)

    class NodeWithData:
        def __init__(self, mutation, time, type):
            self.mutation = mutation
            self.time = time
            self.type = type

    # we build a tree from newick here

    tree_class_tree = Tree()
    node_name = re.split('\|', raw_nodes["name"])[0]
    tree_class_tree.create_node(raw_nodes["name"], raw_nodes["id"],
                                data = NodeWithData(dict_name_muts[node_name],
                                                    dict_name_times[node_name],
                                                    dict_name_types[node_name]))

    for children_node in raw_nodes["children"]:
        add_children(tree_class_tree, children_node)

    return tree_class_tree


