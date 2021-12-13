from treelib import Tree

def tree_to_binary(tree):

    for node in tree.all_nodes():
        node_data = node.data
        num_of_children = len(node.fpointer)
        node_children_list = node.fpointer.copy()
        if num_of_children > 2:
            for i in range(num_of_children - 2):
                tag = 'Dummy' + str(i) + str(node.tag)
                data = node.data
                tree.create_node(tag= tag, identifier = tag, parent=node, data = data)
            for i in range(num_of_children - 2):
                updated_node_id = node_children_list[i+1]
                updated_node_parent_id = 'Dummy' + str(i) + str(node.tag)
                tree.move_node(updated_node_id, updated_node_parent_id)
            updated_node_id = node_children_list[num_of_children - 1]
            updated_node_parent_id = 'Dummy' + str(num_of_children - 3) + str(node.tag)
            tree.move_node(updated_node_id, updated_node_parent_id)
            for i in range(num_of_children - 3):
                updated_node_parent_id = 'Dummy' + str(i) + str(node.tag)
                updated_node_id = 'Dummy' + str(i+1) + str(node.tag)
                tree.move_node(updated_node_id, updated_node_parent_id)

    return tree


