import math

isdebug = False

def debug(str):
    if isdebug:
        print(str)


class AvlTreeNode(object):
    def __init__(self):
        self.value = 0
        self.left = None
        self.right = None
        self.parent = None
        self.balance_factor = 0

    def isright(self):
        if self.parent:
            return self.parent.right == self
        else:
            return False

    def isleft(self):
        if self.parent:
            return self.parent.left == self
        else:
            return False


class AvlTree(object):
    def __init__(self):
        self.root = None

    def add(self, addednode):
        if self.root is None:
            self.root = addednode
        else:
            self._add(self.root, addednode)

    def _add(self, currentnode, addednode):
        # will added to left tree
        if addednode.value < currentnode.value:
            if currentnode.left is not None:
                self._add(currentnode.left, addednode)
            else:
                currentnode.left = addednode
                addednode.parent = currentnode
                self.update(currentnode.left)
        else:
            if currentnode.right is not None:
                self._add(currentnode.right, addednode)
            else:
                currentnode.right = addednode
                addednode.parent = currentnode
                self.update(currentnode.right)

    # update will
    # - update all parent balance_factor
    # - if parent factor <-1 or >1 rotate avl tree
    def update(self, currentnode):
        if currentnode.balance_factor < -1 or currentnode.balance_factor > 1:
            self.rebalance(currentnode)  # rotate the tree and update the root node
            return

        # update balance_factor
        if currentnode.parent is not None:
            if currentnode.isleft():
                currentnode.parent.balance_factor += 1
            elif currentnode.isright():
                currentnode.parent.balance_factor += -1
            if currentnode.parent.balance_factor != 0:
                self.update(currentnode.parent)

    def rebalance(self, node):
        """
        this func will rotate avl tree
        rotate may update root node
        There are four cases of tree rebalancing
        which can be distinguished by the root's and the child's balanceFactor.
        """
        debug("rebalace start node value {} balance factor {}".format(node.value, node.balance_factor))
        if node.balance_factor < 0:
            if node.right.balance_factor > 0:
                debug("rebalace case 1")
                self.rotate_right(node.right)
                self.rotate_left(node)
            else:
                debug("rebalace case 2")
                self.rotate_left(node)
        elif node.balance_factor > 0:
            if node.left.balance_factor < 0:
                debug("rebalace case 3")
                self.rotate_left(node.left)
                self.rotate_right(node)
            else:
                debug("rebalace case 4")
                self.rotate_right(node)


    def rotate_left(self, rotnode):
        """
        rotate left is like:
           b                   d
          / \                 / \
         a   d     -->       b   e
            / \             / \
           c   e           a   c
        rot_node is node b.
        new_root is rot_node's right child.
        if new_root has left child,
        it will become rot_node's right child.(node c becomes node b's right child)
        """

        debug("rotate left value {}".format(rotnode.value))
        new_root = rotnode.right
        rotnode.right = new_root.left
        if new_root.left:
            rotnode.right = new_root.left
            new_root.left.parent = rotnode
        new_root.parent = rotnode.parent
        if rotnode == self.root:
            self.root = new_root
        else:
            if rotnode.isleft():
                rotnode.parent.left = new_root
            else:
                rotnode.parent.right = new_root

        new_root.left = rotnode
        rotnode.parent = new_root
        rotnode.balance_factor = rotnode.balance_factor + 1 - min(new_root.balance_factor, 0)
        new_root.balance_factor = new_root.balance_factor + 1 + max(rotnode.balance_factor, 0)

    def rotate_right(self, rotnode):
        new_root = rotnode.left
        rotnode.left = new_root.right
        if new_root.right:
            rotnode.left = new_root.right
            new_root.right.parent = rotnode
        new_root.parent = rotnode.parent
        if rotnode == self.root:
            self.root = new_root
        else:
            if rotnode.isleft():
                rotnode.parent.left = new_root
            else:
                rotnode.parent.right = new_root
        new_root.right = rotnode
        rotnode.parent = new_root
        rotnode.balance_factor = rotnode.balance_factor - 1 - max(new_root.balance_factor, 0)
        new_root.balance_factor = new_root.balance_factor - 1 + min(rotnode.balance_factor, 0)

    def delete(self, node):
        """
        has 3 cases:
        - this node is a leaf
        - this node has a child
        - this node has two child
        """

        # case 1:this node is a leaf
        # delete directly and update parents
        if node.right is None and node.left is None:
            debug("delete node is a leaf")
            parent = node.parent
            nodeisleft = node.isleft()
            del node
            if parent:
                if nodeisleft:
                    parent.left = None
                    self.delete_update(parent, -1)
                else:
                    parent.right = None
                    self.delete_update(parent, +1)

        # case2:this node has single child
        elif (node.right is None) != (node.left is None):
            debug("delete node has one child")
            # let node's child replace node's position
            # ie:
            #       a            a
            #      /            /
            #     b     --->   c     b is droped
            #    /
            #   c
            parent = node.parent
            if node.left is not None:
                child = node.left
            elif node.right is not None:
                child = node.right
            child.parent = parent

            nodeisleft = node.isleft()
            del node
            if parent:
                if nodeisleft:
                    parent.left = child
                    self.delete_update(parent, -1)
                else:
                    parent.right = child
                    self.delete_update(parent, +1)

        # case3: this node has two children
        elif node.right is not None and node.left is not None:
            debug("delete node has two child")
            # if target node has two children, we can rm the node in some steps:
            # - Find the maximum node at the target node's LEFT subtree
            # - let target_node.value = max_value_node.value
            # - remove the max_value_node, max_value_node must be a leaf or has only one child.
            current_node = node.left
            # find maximum node
            while 1:
                if current_node.right is not None:
                    current_node = current_node.right
                else:
                    break
            maximum_left_tree_node = current_node

            node.value = maximum_left_tree_node.value
            self.delete(maximum_left_tree_node)

    def delete_update(self, curnode, left_right):
        curnode.balance_factor += left_right
        debug("delete_update curnode value {} balance_factor {}".format(curnode.value, curnode.balance_factor))

        # the tree's (root is the curnode) height isnt change
        # its parent's balance_factor neednt change
        if math.fabs(curnode.balance_factor) == 1:
            pass

        # The height(root is the curnode) of the tree has changed
        # need change parent's balance_factor
        elif math.fabs(curnode.balance_factor) == 0:
            parent = curnode.parent
            if parent:
                is_left_right = -1 if curnode.isleft() else +1
                self.delete_update(parent, is_left_right)

        # if a node's balance_factor==2 need to rotate the subtree
        # rotating the subtree will reduce the height of the subtree,
        # so we also need update the subtree's parent info
        elif math.fabs(curnode.balance_factor) == 2:
            parent = curnode.parent

            is_left_right = -1 if curnode.isleft() else +1
            self.rebalance(curnode)
            if parent:
                self.delete_update(parent, is_left_right)
