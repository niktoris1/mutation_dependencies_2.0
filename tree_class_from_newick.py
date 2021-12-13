from treelib import Tree
import re

def MakeTreeClassTree(file_name):
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

    file = open(file_name, "r")
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
    print('STARTED TREE BUILDING')

    tree_class_tree.create_node(raw_nodes["name"], raw_nodes["id"]) # we build a tree from newick here
    for children_node in raw_nodes["children"]:
        add_children(tree_class_tree, children_node)

    print('ENDED TREE BUILDING')

    return tree_class_tree


