from treelib import Tree
import re

def MakeTreeClassTree(newick_file_name, name_muts_dict = None, name_type_dict = None, name_time_dict = None):
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
            some_tree.create_node(node["name"], node["id"], parent=node["parentid"])
        else:
            some_tree.create_node(node["name"], node["id"])
        name_id_dict[node["name"]] = node["id"]
        for child_node in node["children"]:
            add_children(some_tree, child_node)

    tree_class_tree = Tree()

    tree_class_tree.create_node(raw_nodes["name"], raw_nodes["id"], data = []) # we build a tree from newick here
    for children_node in raw_nodes["children"]:
        add_children(tree_class_tree, children_node)

    #for node in tree_class_tree.all_nodes():
    #    tree_class_tree.data = [name_muts_dict[node["name"]], name_type_dict[node["name"]], name_time_dict[node["name"]]]

    return tree_class_tree


