from avltree import AvlTree, AvlTreeNode


def test_case_1():
    """
    result:
          2
        1   4
           3 5
    """
    print("test case 1")
    tree = AvlTree()
    test_data = [1, 2, 3, 4, 5]
    for item in test_data:
        temp_node = AvlTreeNode()
        temp_node.value = item
        tree.add(temp_node)

    assert tree.root.value == 2
    assert tree.root.right.right.value == 5


def test_case_2():
    print("test case 2")
    tree = AvlTree()
    test_data = [8, 5, 9, 10, 3, 6, 7]
    for item in test_data:
        temp_node = AvlTreeNode()
        temp_node.value = item
        tree.add(temp_node)
    # this tree is :
    #             8
    #           5   9
    #          3 6   10
    #             7
    #
    # remove 3
    # the tree will becomes:
    #             8
    #           6   9
    #          5 7   10

    dele_node = tree.root.left.left
    tree.delete(dele_node)
    print("    {}({})".format(tree.root.value, tree.root.balance_factor))
    l1_1 = tree.root.left
    l1_2 = tree.root.right
    print("   /   \\")
    print(" %s(%s)    %s(%s)" % (l1_1.value, l1_1.balance_factor, l1_2.value, l1_2.balance_factor))

    l2_1 = l1_1.left
    l2_2 = l1_1.right
    l2_4 = l1_2.right
    print("/ \\       \\")
    print("%s %s        %s" % (l2_1.value, l2_2.value, l2_4.value))

    assert tree.root.value == 8
    assert tree.root.right.value == 9
    assert tree.root.right.balance_factor == -1
    assert tree.root.left.right.value == 7
    assert tree.root.left.right.balance_factor == 0


def test_case_3():
    """
    tree:
        8
       5  9
           10

    the tree removed 10 will becomes:
        8
       5 9
    """
    print("test case 3")
    tree = AvlTree()
    test_data = [8, 5, 9, 10]
    for item in test_data:
        temp_node = AvlTreeNode()
        temp_node.value = item
        tree.add(temp_node)
    dele_node = tree.root.right.right
    tree.delete(dele_node)
    print("    {}({})".format(tree.root.value, tree.root.balance_factor))
    l1_1 = tree.root.left
    l1_2 = tree.root.right
    print("   /   \\")
    print(" %s(%s)    %s(%s)" % (l1_1.value, l1_1.balance_factor, l1_2.value, l1_2.balance_factor))

    assert tree.root.right.value == 9
    assert tree.root.right.balance_factor == 0

def test_case_4():
    """
    if arr [8, 5, 9, 10,4,3,6] added in a tree one by one.
    finally the tree will be :
          8
        /  \
       4   9
      / \   \
     3  5   10
        \
        6

    and then, remove 9, because node 9 only has single child, so
    9's child will replace 9's location like:

          8
        /  \
       4   10
      / \
     3  5
        \
        6
    and the tree(the rotnode is 8) need to be rebalanced.

    the result will be:

             5(0)
           /      \
        4(1)      8(0)
         /      /   \
      3(0)    6(0)  10(0)
    """
    print("test case 4")
    tree = AvlTree()
    test_data = [8, 5, 9, 10, 4, 3, 6]
    for item in test_data:
        temp_node = AvlTreeNode()
        temp_node.value = item
        tree.add(temp_node)

    dele_node = tree.root.right
    tree.delete(dele_node)

    print("     {}({})".format(tree.root.value, tree.root.balance_factor))
    print("   /       \\")
    l1_1 = tree.root.left
    l1_2 = tree.root.right
    print("%s(%s)       %s(%s)" % (l1_1.value, l1_1.balance_factor, l1_2.value, l1_2.balance_factor))
    print("  /          / \\")
    l2_1 = l1_1.left
    l2_3 = l1_2.left
    l2_4 = l1_2.right
    print(" %s(%s)      %s(%s)   %s(%s)   " % (
        l2_1.value, l2_1.balance_factor, l2_3.value, l2_3.balance_factor, l2_4.value, l2_4.balance_factor))


def test_case_5():
    """
    will build a tree like:
         5(0)
       /     \
    4(1)     8(0)
     /      /   \
    3(0)   6(0) 10(0)
    """
    print("test case 5")
    tree = AvlTree()
    test_data = [8, 4, 10, 3, 5, 6]
    for item in test_data:
        temp_node = AvlTreeNode()
        temp_node.value = item
        tree.add(temp_node)

    print("    {}({})".format(tree.root.value, tree.root.balance_factor))
    print("   /      \\")
    l1_1 = tree.root.left
    l1_2 = tree.root.right
    print("%s(%s)        %s(%s)" % (l1_1.value, l1_1.balance_factor, l1_2.value, l1_2.balance_factor))
    print(" /          /    \\")
    l2_1 = l1_1.left
    l2_3 = l1_2.left
    l2_4 = l1_2.right
    print("%s(%s)       %s(%s)   %s(%s)" % (l2_1.value, l2_1.balance_factor
                                            , l2_3.value, l2_3.balance_factor
                                            , l2_4.value, l2_4.balance_factor))

    assert tree.root.left.left.value == 3
    assert tree.root.left.balance_factor == 1
    assert l2_4.value == 10


def test_case_6():
    """
    this tree is like:
         10                       10            10           10
        / \                      /  \          / \          / \
       6  12                    3   12        3  12        7  12
      / \  \     -- rm 6 -->   / \   \   -->   \  \  -->  / \  \
     3  7  14                 3  7   14        7  14     3  8  14
         \                       \             \
         8                       8             8
    """

    print("test case 6")
    tree = AvlTree()
    test_data = [10, 6, 12, 14, 3, 7, 8]
    for item in test_data:
        temp_node = AvlTreeNode()
        temp_node.value = item
        tree.add(temp_node)

    dele_node = tree.root.left
    tree.delete(dele_node)

    print("      {}({})".format(tree.root.value, tree.root.balance_factor))
    l1_1 = tree.root.left
    l1_2 = tree.root.right
    print("   {}({})    {}({})".format(l1_1.value, l1_1.balance_factor, l1_2.value, l1_2.balance_factor))

    l2_1 = l1_1.left
    l2_2 = l1_1.right
    l2_4 = l1_2.right
    print("{}({})  {}({})    {}({})".format(l2_1.value, l2_1.balance_factor,
                                            l2_2.value, l2_2.balance_factor,
                                            l2_4.value, l2_4.balance_factor))

    assert tree.root.left.left.value == 3
    assert tree.root.right.balance_factor == -1

func_arr = [
    test_case_1,
    test_case_2,
    test_case_3,
    test_case_4,
    test_case_5,
    test_case_6
]

for item in func_arr:
    item()
