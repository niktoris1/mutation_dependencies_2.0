from treelib import Tree
import re
import logging # a workaround to kill warnings
logging.captureWarnings(True)

def MakeTreeClassTree(newick_file_name, dict_name_muts = None, dict_name_times = None, dict_name_types = None, extrenal_dicts_exist = 0):
    # extrenal_dicts_exist = 0 if there are external dicts with time and type
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

    with open(newick_file_name, "r") as file:
        text_newick = file.read()
        raw_nodes = parse(text_newick)

        if extrenal_dicts_exist == 0:
            dict_name_muts = {} # we know of no muts in this case
            dict_name_times = {}
            dict_name_types = {}

            def DFS(node_dict, current_time):
                new_time = node_dict['length'] + current_time
                name = re.split('\|', str(node_dict['name']))[0]
                dict_name_times.update({name: new_time})
                dict_name_muts.update({name: []})
                if len(node_dict['children']) == 0:
                    dict_name_types.update({name: 'Sample'})
                else:
                    dict_name_types.update({name: 'Coalescence'})

                for child in node_dict['children']:
                    DFS(child, new_time)

            DFS(raw_nodes, 0)



        def add_children(some_tree, node): #adds all children to the tree by checking all parent ids
            if node["parentid"] is not None:
                node_name = re.split('\|', node["name"])[0]
                some_tree.create_node(node_name, node["id"], parent=node["parentid"],
                                      data=NodeWithData(dict_name_muts[node_name],
                                                        dict_name_times[node_name],
                                                        dict_name_types[node_name]))
            else:
                raise ValueError("The head vertex supposed to be added manually")
            for child_node in node["children"]:
                add_children(some_tree, child_node)

        class NodeWithData:
            def __init__(self, mutations, time, type):
                self.mutations = mutations
                self.time = time
                self.type = type

        # we build a tree from newick here

        tree_class_tree = Tree()
        node_name = re.split('\|', raw_nodes["name"])[0]
        tree_class_tree.create_node(raw_nodes["name"], raw_nodes["id"],
                                    data= NodeWithData(dict_name_muts[str(node_name)],
                                                        dict_name_times[str(node_name)],
                                                        dict_name_types[str(node_name)]))

        for children_node in raw_nodes["children"]:
            add_children(tree_class_tree, children_node)

        return tree_class_tree


