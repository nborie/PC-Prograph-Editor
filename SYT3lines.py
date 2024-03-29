"""
This module implement 3 line rectangular Young tableau and the set of all
of them.

EXAMPLES:

>>> SYT3lines([[5, 9, 11, 12], [2, 6, 7, 10], [1, 3, 4, 8]])
---------------------
|  5 |  9 | 11 | 12 |
---------------------
|  2 |  6 |  7 | 10 |
---------------------
|  1 |  3 |  4 |  8 |
---------------------
"""
#*****************************************************************************
#  Copyright (C) 2021 Nicolas Borie <nicolas dot borie at univ-eiffel . fr>
#
#  Distributed under the terms of Creative Commons Attribution-ShareAlike 3.0
#  Creative Commons CC-by-SA 3.0
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  The full text of the CC-By-SA 3.0 is available at:
#
#            https://creativecommons.org/licenses/by-sa/3.0/
#            https://creativecommons.org/licenses/by-sa/3.0/fr/
#*****************************************************************************

from math import log, factorial
from copy import deepcopy
from random import randint


def is_SYT3line(values, verbose=False):
    """
    Returns `True` is values is the content of a
    three lines standard Young tableau.

    EXAMPLES:

    >>> is_SYT3line([[3], [2], [1]], True)
    True
    >>> is_SYT3line([[], [], []])
    True
    >>> is_SYT3line([[], []], True)
    Content does not contain 3 lines.
    False
    >>> is_SYT3line([[7, 8, 9], [4, 5, 6], [1, 2, 3]], True)
    True
    >>> is_SYT3line([[7, 8, 9], [4, 6, 5], [1, 2, 3]], True)
    The 3 lines are not increasing.
    False
    >>> is_SYT3line([[7, 8], [4, 5, 6], [1, 2, 3]], True)
    The 3 lines does not have same lenght.
    False
    >>> is_SYT3line([], True)
    Content seems to be empty.
    False
    >>> is_SYT3line([[]], True)
    Content does not contain 3 lines.
    False
    >>> is_SYT3line([[], [], [1]], True)
    The 3 lines does not have same lenght.
    False
    >>> is_SYT3line([[5, 6], [3, 4], [2, 1]], True)
    The 3 lines are not increasing.
    False
    >>> is_SYT3line([[5, 4], [3, 6], [1, 2]], True)
    The 3 lines are not increasing.
    False
    """
    if not values:
        if verbose:
            print('Content seems to be empty.')
        return False
    n = len(values[0])
    if len(values) != 3:
        if verbose:
            print('Content does not contain 3 lines.')
        return False
    for j in range(1, 3):
        if len(values[j]) != n:
            if verbose:
                print('The 3 lines does not have same lenght.')
            return False
    for j in range(3):
        for i in range(1, n):
            if values[j][i] < values[j][i-1]:
                if verbose:
                    print('The 3 lines are not increasing.')
                return False
    for i in range(n):
        for j in range(1, 3):
            if values[j-1][i] < values[j][i]:
                if verbose:
                    print('The colonms are not increasing.')
                return False
    if sorted(sum([list(vals) for vals in values], [])) != list(range(1, 3*n + 1)):
        if verbose:
            print('The content is not standard (values in 1 to 3n).')
        return False

    return True


def right_rotation_prod(t, p1, p2):
    """
    Proceed a right rotation over edge linking product `p1` and `p2`
    inside `t`. Coproduct `p1` must be on the left input of coproduct
    `p2`.

    EXAMPLES:

    >>> rrp = right_rotation_prod
    >>> rrp([[4, 7, 9], [2, 5, 8], [1, 3, 6]], 4, 7)
    [[6, 7, 9], [2, 4, 8], [1, 3, 5]]
    >>> rrp(rrp([[4, 7, 9], [2, 5, 8], [1, 3, 6]], 4, 7), 7, 9)
    [[6, 8, 9], [2, 4, 7], [1, 3, 5]]
    >>> rrp(rrp(rrp([[4, 7, 9], [2, 5, 8], [1, 3, 6]], 4, 7), 7, 9), 6, 8)
    [[7, 8, 9], [2, 4, 6], [1, 3, 5]]
    >>> rrp([[4, 7, 9], [2, 5, 8], [1, 3, 6]], 7, 9)
    [[4, 8, 9], [2, 5, 7], [1, 3, 6]]
    >>> rrp(rrp([[4, 7, 9], [2, 5, 8], [1, 3, 6]], 7, 9), 4, 8)
    [[7, 8, 9], [2, 4, 6], [1, 3, 5]]
    """
    n = len(t[0])
    for i in range(n-1):
        if t[0][i+1] <= p2 and t[0][i+1] > p1:
            t[0][i] = t[0][i+1]-1
    for j in range(1, 3):
        for i in range(n):
            if t[j][i] < p2 and t[j][i] > p1:
                t[j][i] = t[j][i] - 1
    return t


def left_rotation_prod(t, p1, p2):
    """
    """
    raise NotImplementedError("Please code me!")


def left_rotation_coprod(t, i1, i2):
    """
    Proceed a left rotation over edge linking coproduct `i1` and `i2`
    inside `t`. Coproduct `i2` must be on the right ouput of coproduct
    `i1`.

    EXAMPLES:

    >>> lrc = left_rotation_coprod
    >>> lrc([[4, 7, 9], [2, 5, 8], [1, 3, 6]], 1, 3)
    [[4, 7, 9], [3, 5, 8], [1, 2, 6]]
    >>> lrc(lrc([[4, 7, 9], [2, 5, 8], [1, 3, 6]], 1, 3), 1, 6)
    [[5, 7, 9], [4, 6, 8], [1, 2, 3]]
    >>> lrc([[4, 7, 9], [2, 5, 8], [1, 3, 6]], 3, 6)
    [[5, 7, 9], [2, 6, 8], [1, 3, 4]]
    >>> lrc(lrc([[4, 7, 9], [2, 5, 8], [1, 3, 6]], 3, 6), 1, 3)
    [[5, 7, 9], [3, 6, 8], [1, 2, 4]]
    >>> lrc(lrc(lrc([[4, 7, 9], [2, 5, 8], [1, 3, 6]], 3, 6), 1, 3), 2, 4)
    [[5, 7, 9], [4, 6, 8], [1, 2, 3]]
    """
    n = len(t[0])
    for i in range(n-1, -1, -1):
        if t[2][i] <= i2 and t[2][i] > i1:
            t[2][i] = t[2][i-1]+1
    for j in range(2):
        for i in range(n):
            if t[j][i] < i2 and t[j][i] > i1:
                t[j][i] = t[j][i] + 1
    return t


def right_rotation_coprod(t, o1, o2):
    """
    """
    raise NotImplementedError("Please code me!")


def jump_over_rotation(t, k):
    """
    Rotation comming from the triangulations point of view making a
    jump of a coproduct over product. Before the left output of the
    coproduct is connected to the right input of the product and after
    the input of the coproduct is connected the single output of the
    product over it.

    EXAMPLES:

    >>> jump_over_rotation([[4, 7, 9], [2, 5, 8], [1, 3, 6]], 3)
    [[3, 7, 9], [2, 5, 8], [1, 4, 6]]
    >>> jump_over_rotation([[4, 7, 9], [2, 5, 8], [1, 3, 6]], 6)
    [[4, 6, 9], [2, 5, 8], [1, 3, 7]]
    >>> jump_over_rotation([[4, 6], [2, 5], [1, 3]], 3)
    [[3, 6], [2, 5], [1, 4]]
    """
    n = len(t[0])
    for j in range(3):
        for i in range(n):
            if t[j][i] == k:
                t[j][i] = k+1
            elif t[j][i] == k+1:
                t[j][i] = k
    return t

def land_over_rotation(t, i, j, k):
    """
    Rotation comming from the triangulations point of view making a
    land of a coproduct comming over a product. Before the input of
    the coproduct is connected the single output of the product over
    it. After the right output of the coproduct is connected to the
    left input of the product

    i : label of the wire connected the two operators
    i-1 : last right input of product
    i+1 : fisrt left output of coproduct
    j : left input of product
    k : right output of coproduct

    EXAMPLES:

    >>> lor = land_over_rotation
    >>> lor([[3, 6],[2, 5],[1, 4]], 4, 2, 6)
    [[5, 6], [3, 4], [1, 2]]
    >>> lor([[3, 6, 9],[2, 5, 8],[1, 4, 7]], 4, 2, 6)
    [[5, 6, 9], [3, 4, 8], [1, 2, 7]]
    >>> lor([[3, 6, 9],[2, 5, 8],[1, 4, 7]], 7, 5, 9)
    [[3, 8, 9], [2, 6, 7], [1, 4, 5]]
    """
    n = len(t[0])
    for m in range(3):
        for p in range(n):
            if t[m][p] >= j and t[m][p] < i:
                t[m][p] += k-i
            elif t[m][p] >= i and t[m][p] < k:
                t[m][p] += j-i
    t[0].sort()
    t[1].sort()
    t[2].sort()
    return t


class SYT3lines():
    """
    A class modeling 3 lines rectangular standard Young tableau

    EXAMPLES:

    >>> SYT3lines([[7, 8, 9], [4, 5, 6], [1, 2, 3]])
    -------------
    | 7 | 8 | 9 |
    -------------
    | 4 | 5 | 6 |
    -------------
    | 1 | 2 | 3 |
    -------------
    """
    def __init__(self, values, check=True, verbose=False):
        """
        TESTS:

        >>> T = SYT3lines([[4, 6], [2, 5], [1, 3]])
        >>> T = SYT3lines([[], [], []])
        """
        if check:
            if not is_SYT3line(values, verbose=verbose):
                raise ValueError(str(values) +
                      " is not the content of a 3 lines rectangular standard Young tableau")
        self._content = tuple([tuple(line) for line in values])
        self._size = len(values[0])

    def __repr__(self):
        """
        TESTS:

        >>> SYT3lines([[4, 6], [2, 5], [1, 3]])
        ---------
        | 4 | 6 |
        ---------
        | 2 | 5 |
        ---------
        | 1 | 3 |
        ---------
        """
        g = int(log(3*self._size, 10)+1)
        ans = "-"*((g+3)*self._size+1)
        for line in self._content:
            ans += "\n| " + " | ".join(['%*d'%(g, val) for val in line]) + " |\n"
            ans += "-"*((g+3)*self._size+1)
        return ans

    def __eq__(self, other):
        """
        TESTS:

        >>> T = SYT3lines([[3], [2], [1]])
        >>> S = SYT3lines([[2], [3], [1]], check=False)
        >>> T == S
        False
        >>> T == T
        True
        """
        if other.__class__ is self.__class__:
            return self._content == other._content
        else:
            return self._content == other

    def __hash__(self):
        """
        TESTS:

        >>> SYT3lines([[4, 7, 9], [2, 5, 8], [1, 3, 6]]).__hash__() > 0
        True
        """
        return hash(self._content)
        
    def schutzenberger(self):
        """
        Return the image of `self` by the schutzenberger involution.

        EXAMPLES:

        >>> T = SYT3lines([[6, 8, 9], [2, 5, 7], [1, 3, 4]])
        >>> S = T.schutzenberger(); S
        -------------
        | 6 | 7 | 9 |
        -------------
        | 3 | 5 | 8 |
        -------------
        | 1 | 2 | 4 |
        -------------
        >>> S.schutzenberger() == T
        True
        """
        n = self._size
        complement = 3 * n + 1
        vals = []
        for i in range(3):
            line = []
            for j in range(n):
                line.append(complement - self._content[2-i][n-1-j])
            vals.append(line)
        return SYT3lines(vals, False, False)

    def products_inputs(self):
        """
        Returns the list of product inputs. Each product will be described
        by a couple of integer `(left, right)` where `left` is the label of
        wire linking the left entry of the product and `right` is the label
        of the wire linking the right entry of the product.

        EXAMPLES:

        >>> T = SYT3lines([[4, 7, 10, 12], [2, 5, 8, 11], [1, 3, 6, 9]])
        >>> T.products_inputs()
        [(2, 4), (5, 7), (8, 10), (11, 12)]
        >>> T = SYT3lines([[6, 8, 9], [2, 5, 7], [1, 3, 4]])
        >>> T.products_inputs()
        [(5, 6), (7, 8), (2, 9)]
        >>> T = SYT3lines([[9, 10, 11, 12], [2, 4, 6, 8], [1, 3, 5, 7]])
        >>> T.products_inputs()
        [(8, 9), (6, 10), (4, 11), (2, 12)]
        """
        n = self._size
        done = []
        prods = []
        for i in range(n):
            right = self._content[0][i]
            j = n-1
            while j >= 0:
                if self._content[1][j] < right and self._content[1][j] not in done:
                    left = self._content[1][j]
                    done.append(left)
                    break
                j = j-1
            prods.append( (left, right) )
        return prods

    def coproducts_outputs(self):
        """
        Returns the list of coproduct outputs. Each coproduct will be dgit@github.com:nborie/PC-Prograph-Editor.gitescribed
        by a couple of integer `(left, right)` where `left` is the label of
        wire linking the left output of the coproduct and `right` is the label
        of the wire linking the right output of the coproduct.

        EXAMPLES:

        >>> T = SYT3lines([[9, 10, 11, 12], [2, 4, 6, 8], [1, 3, 5, 7]])
        >>> T.coproducts_outputs()
        [(2, 3), (4, 5), (6, 7), (8, 9)]
        >>> T = SYT3lines([[3, 6], [2, 5], [1, 4]])
        >>> T.coproducts_outputs()
        [(2, 3), (5, 6)]
        """
        n = self._size
        done = []
        coprods = []
        for i in range(n):
            right = self._content[1][i]
            j = n-1
            while j >= 0:
                if self._content[2][j] < right and self._content[2][j] not in done:
                    left = self._content[2][j]
                    done.append(left)
                    break
                j = j-1
            coprods.append( (left+1, right+1) )
        return coprods

    def faces(self):
        """
        Returns the list of faces appearing in the program. The faces are 
        described by the ordered list of labels of the edges delimiting them.

        EXAMPLES::

        >>> T = SYT3lines([[8, 9, 11, 14, 15], [2, 7, 10, 12, 13], [1, 3, 4, 5, 6]])
        >>> T.faces()
        [[1, 2, 10, 12], [1, 3, 14, 15], [2, 3, 4, 5, 6, 7, 9], [7, 8], [6, 8, 9, 10, 11], [5, 11, 12, 13, 15], [4, 13, 14]]
        """
        ans =[]
        prods = self.products_inputs()
        coprods = self.coproducts_outputs()
        # Inner function to build left border
        def next_left(index):
            for (l, r) in coprods:
                if index == l-1:
                    return r
            for (l, r) in prods:
                if index == r:
                    return r+1
            return None
        # Inner function to build right border
        def next_right(index):
            for (l, r) in coprods:
                if index == l-1:
                    return l
            for (l, r) in prods:
                if index == l:
                    return r+1
            return None
        # First left face
        face = []
        current_edge = 1
        while current_edge != self._size*3 + 1:
            face.append(current_edge)
            current_edge = next_right(current_edge)
        ans.append(face.copy())
        # second right face
        face = []
        current_edge = 1
        while current_edge != self._size*3 + 1:
            face.append(current_edge)
            current_edge = next_left(current_edge)
        ans.append(face.copy())
        # Other general faces
        for (l, r) in coprods:
            face = []
            current_edge = l
            while current_edge != None:
                face.append(current_edge)
                current_edge = next_left(current_edge)
            current_edge = r
            while current_edge != None:
                face.append(current_edge)
                current_edge = next_right(current_edge)
            ans.append(face.copy())
        return ans

    def edge_type(self, i):
        """
        Return the type of edge labelled by `i` inside the prograph
        associated with `self`.

        EXAMPLES:

        >>> T = SYT3lines([[3, 6], [2, 5], [1, 4]])
        >>> for i in range(1, 7):
        ...     T.edge_type(i)
        ...
        (0, 2)
        (2, 1)
        (1, 0)
        (0, 2)
        (2, 1)
        (1, 0)
        """
        if i == 1: # This is the type of unflipable edge 1
            return (0, 2)

        if i in self._content[0]:
            go_to = 0 # right input of product
        elif i in self._content[1]:
            go_to = 1 # left input of product
        else:
            go_to = 2 # input of coproduct

        if i-1 in self._content[0]:
            come_from = 0 # output of product
        elif i-1 in self._content[1]:
            come_from = 1 # right output of coproduct
        else:
            come_from = 2 # left output of coproduct

        return (come_from, go_to)

    def is_edge_flipable(self, i):
        """
        Return `True` if the wire labelled by `i` is flipable or not.
        Inside Product-Coproduct Prograph, edge `1` is never flipable
        since highest product is connected to lowest coproduct by the
        only edge crossing infinity. For other edges, the only ones
        not flipable are edge connecting left(resp. right) output of
        coproduct to left(resp. right) entry of product.

        >>> T = SYT3lines([[4, 6], [2, 5], [1, 3]])
        >>> for i in range(1,7):
        ...     T.is_edge_flipable(i)
        ...
        False
        False
        True
        True
        True
        False
        """
        if i == 1:
            return False
        (c, g) = self.edge_type(i)
        return (c, g) not in [(2, 1), (1, 0)]

    def is_edge_reducible(self, i):
        """
        Return `True` if the wire labelled by `i` is flipable
        down. Return `False` otherwise.

        Here two choices were possible due to symmetries
        EST-WEST. Reduced edge connect either:
        - output of product to right input of product (The choice)
        - left output of coproduct to input of coproduct (forced by schützenberger involution)
        - right output of coproduct to left input of product (forced by spherical geometry)


        EXAMPLES:

        >>> T = SYT3lines([[7, 8, 9], [4, 5, 6], [1, 2, 3]])
        >>> [T.is_edge_reducible(i) for i in range(1, 10)]
        [False, False, False, False, False, False, False, False, False]
        >>> T = SYT3lines([[4, 7, 9], [2, 5, 8], [1, 3, 6]])
        >>> [T.is_edge_reducible(i) for i in range(1, 10)]
        [False, False, True, True, True, True, True, True, False]
        """
        if i == 1:
            return False
        (c, g) = self.edge_type(i)
        return (c, g) in [(0, 1), (1, 2), (2, 0), (0, 2)]

    def reducible_edges(self):
        """
        Returns the list of reducibles edges inside `self`.

        EXAMPLES:

        >>> T = SYT3lines([[4, 7, 9], [2, 5, 8], [1, 3, 6]])
        >>> T.reducible_edges()
        [3, 4, 5, 6, 7, 8]
        >>> T = SYT3lines([[7, 8, 9], [4, 5, 6], [1, 2, 3]])
        >>> T.reducible_edges()
        []
        >>> T = SYT3lines([[3, 6, 9], [2, 5, 8], [1, 4, 7]])
        >>> T.reducible_edges()
        [4, 7]
        """
        n = len(self._content[0])
        return [i for i in range(1, 3*n+1) if self.is_edge_reducible(i)]

    def flip_down_edge(self, i):
        """
        Modify `self` by flipping down edge labelled by `i`.

        EXAMPLES:


        """
        if not self.is_edge_reducible(i):
            raise ValueError('Edge %s can not be flipped down'%(str(i)))
        (c, g) = self.edge_type(i)

        if (c, g) == (1, 2): # left rotation for coproduct
            for o1, o2 in self.coproducts_outputs():
                if o2 == i:
                    s = o1 - 1
            return SYT3lines(left_rotation_coprod([list(line) for line in self._content], s, i), False, False)

        elif (c, g) == (0, 1): # right rotation for product
            for i1, i2 in self.products_inputs():
                if i == i1:
                    s = i2
            return SYT3lines(right_rotation_prod([list(line) for line in self._content], i-1, s), False, False)

        elif (c, g) == (2, 0): # left output of coproduct inside right input of product
            return SYT3lines(jump_over_rotation([list(line) for line in self._content], i-1), False, False)

        else:
            if (c, g) != (0, 2):
                raise ValueError("This should never happen! ")
            for o1, o2 in self.coproducts_outputs():
                if o1 == i+1:
                    k = o2
            for i1, i2 in self.products_inputs():
                if i-1 == i2:
                    j = i1
            return SYT3lines(land_over_rotation([list(line) for line in self._content], i, j, k), False, False)

    def lower_elements(self):
        """

        EXAMPLES:
        """
        return [self.flip_down_edge(i) for i in self.reducible_edges()]

        
    def to_bialgebra_layers(self):
        """
        Returns a list of list of operators whose complete assembly
        rebuilt `self`. Algebraicly, `self` can be view as the
        composition of some layers where each layers is a tensor
        product of some products, coproducts and severals times the
        identity function. This method return the minimal list of
        layers whose assembly rebuilt `self`.

        EXAMPLES:

        >>> SYT3lines([[4, 6], [2, 5], [1, 3]]).to_bialgebra_layers()
        [['C'], ['Id', 'C'], ['P', 'Id'], ['P']]
        >>> SYT3lines([[5, 6], [2, 4], [1, 3]]).to_bialgebra_layers()
        [['C'], ['Id', 'C'], ['Id', 'P'], ['P']]
        >>> SYT3lines([[4, 6], [3, 5], [1, 2]]).to_bialgebra_layers()
        [['C'], ['C', 'Id'], ['P', 'Id'], ['P']]
        >>> SYT3lines([[3, 6], [2, 5], [1, 4]]).to_bialgebra_layers()
        [['C'], ['P'], ['C'], ['P']]
        >>> SYT3lines([[5, 6], [3, 4], [1, 2]]).to_bialgebra_layers()
        [['C'], ['C', 'Id'], ['Id', 'P'], ['P']]
        """
        layers = []
        all_products = self.products_inputs()
        all_coprods = self.coproducts_outputs()
        done_coprods = []
        layer_labels = [1] # the fisrt coproduct !
        while all_products or (len(done_coprods) < len(self._content[0])):
            new_layer = []
            new_labels = []
            i = 0
            while (i < len(layer_labels)):
                if layer_labels[i] in self._content[2]:
                    new_layer.append("C")
                    done_coprods.append(layer_labels[i])
                    for l, r in all_coprods:
                        if l == layer_labels[i]+1:
                            new_labels.append(l)
                            new_labels.append(r)
                    i += 1
                elif (i+1 < len(layer_labels)) and (layer_labels[i], layer_labels[i+1]) in all_products:
                    new_layer.append("P")
                    all_products.remove((layer_labels[i], layer_labels[i+1]))
                    new_labels.append(layer_labels[i+1]+1)
                    i += 2
                else:
                    new_layer.append("Id")
                    new_labels.append(layer_labels[i])
                    i += 1
            layer_labels = new_labels
            layers.append(new_layer)
        return layers


class RectSYT3lines():
    """
    A class modeling the set of all rectangular 3 lines standard Young
    tableau of a given number of colunms.

    EXAMPLES:

    >>> S = RectSYT3lines(3)
    >>> S.cardinality()
    42
    """
    def __init__(self, n):
        """
        TESTS:

        >>> S = RectSYT3lines(4)
        """
        self._size = n
        self._list = None

    def __repr__(self):
        """
        TESTS:

        >>> RectSYT3lines(5)
        Rectangular Standard Young Tableaux of size (3, 5)
        """
        return "Rectangular Standard Young Tableaux of size (3, %d)"%(self._size)

    def cardinality(self):
        """
        Returns the cardinality of `self`

        EXAMPLES:

        >>> [RectSYT3lines(i).cardinality() for i in range(10)]
        [1, 1, 5, 42, 462, 6006, 87516, 1385670, 23371634, 414315330]
        """
        n = self._size
        return (2*factorial(3*n)) // (factorial(n)*factorial(n+1)*factorial(n+2))
    
    def __set_list(self):
        """
        Sets the list of all elements of `self`.

        EXAMPLES:

        >>> for t in RectSYT3lines(2):
        ...     print(t)
        ...
        ---------
        | 3 | 6 |
        ---------
        | 2 | 5 |
        ---------
        | 1 | 4 |
        ---------
        ---------
        | 4 | 6 |
        ---------
        | 2 | 5 |
        ---------
        | 1 | 3 |
        ---------
        ---------
        | 5 | 6 |
        ---------
        | 2 | 4 |
        ---------
        | 1 | 3 |
        ---------
        ---------
        | 4 | 6 |
        ---------
        | 3 | 5 |
        ---------
        | 1 | 2 |
        ---------
        ---------
        | 5 | 6 |
        ---------
        | 3 | 4 |
        ---------
        | 1 | 2 |
        ---------
        """
        if self._list is not None:
            return
        n = self._size
        content = [[0]*n for i in range(3)]
        val = 1
        last = 3*n
        tableaux = [content]
        for val in range(1, last+1):
            new_tableaux = []
            for t in tableaux:
                for i in range(n):
                    for j in range(3):
                        if t[j][i] == 0:
                            if i == 0 or t[j][i-1] != 0:
                                if j==2 or t[j+1][i] != 0:
                                    t[j][i] = val
                                    new_tableaux.append(deepcopy(t))
                                    t[j][i] = 0
            tableaux = new_tableaux
        self._list = [SYT3lines(x, check=False) for x in tableaux]

    def __list__(self):
        """
        TESTS:

        >>> R = RectSYT3lines(1)
        >>> list(R)
        [-----
        | 3 |
        -----
        | 2 |
        -----
        | 1 |
        -----]
        """
        self.__set_list()
        return self._list

    def __iter__(self):
        """
        TESTS:

        >>> sum([1 for t in RectSYT3lines(3)])
        42
        """
        self.__set_list()
        for t in self._list:
            yield t

    def __contains__(self, elt):
        """
        TESTS:

        >>> R = RectSYT3lines(3)
        >>> [[7, 8, 9], [4, 5, 6], [1, 2, 3]] in R
        True
        >>> [[7, 8, 6], [4, 5, 9], [1, 2, 3]] in R
        False
        >>> T = SYT3lines([[7, 8, 9], [4, 5, 6], [1, 2, 3]])
        >>> T in R
        True
        >>> T = SYT3lines([[7, 8, 6], [4, 5, 9], [1, 2, 3]], check=False)
        >>> T in R
        False
        """
        if isinstance(elt, (list, tuple)):
            if elt:
                if elt[0]:
                    if len(elt[0]) == self._size:
                        return is_SYT3line(elt, verbose=False)
            return False
        elif isinstance(elt, (SYT3lines,)):
            L = elt._content
            if L:
                if L[0]:
                    if len(L[0]) == self._size:
                        return is_SYT3line(L, verbose=False)
        return False

    def random_element(self):
        """
        Return a random element of `self`.

        EXAMPLES:

        >>> R = RectSYT3lines(10)
        >>> R.random_element() in R
        True
        """
        n = self._size
        t = [[0]*n for i in range(3)]
        last = 3*n
        for val in range(1, last+1):
            found = False
            while not found:
                j = randint(0,2)
                i = 0
                while t[j][i] != 0 and i < n-1:
                    i += 1
                if t[j][i] == 0:
                    if i == 0 or t[j][i-1] != 0:
                        if j==2 or t[j+1][i] != 0:
                            found = True
                            t[j][i] = val
        return SYT3lines(t, check=False)

    def max_element(self):
        """
        Return the maximal element of `self`.

        EXAMPLES:

        >>> RectSYT3lines(2).max_element()
        ---------
        | 4 | 6 |
        ---------
        | 2 | 5 |
        ---------
        | 1 | 3 |
        ---------
        >>> RectSYT3lines(12).max_element()
        -------------------------------------------------------------
        |  4 |  7 | 10 | 13 | 16 | 19 | 22 | 25 | 28 | 31 | 34 | 36 |
        -------------------------------------------------------------
        |  2 |  5 |  8 | 11 | 14 | 17 | 20 | 23 | 26 | 29 | 32 | 35 |
        -------------------------------------------------------------
        |  1 |  3 |  6 |  9 | 12 | 15 | 18 | 21 | 24 | 27 | 30 | 33 |
        -------------------------------------------------------------
        """
        n = self._size
        val = [[], [2], [1, 3]]
        pos = 0
        for i in range(4, 3*n):
            val[pos].append(i)
            pos = (pos + 1) % 3
        val[0].append(3*n)
        return SYT3lines(val, check=False)
    
    def min_element(self):
        """
        Return the minimal element of `self`.

        EXAMPLES:

        >>> RectSYT3lines(2).min_element()
        ---------
        | 5 | 6 |
        ---------
        | 3 | 4 |
        ---------
        | 1 | 2 |
        ---------
        >>> RectSYT3lines(12).min_element()
        -------------------------------------------------------------
        | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 | 36 |
        -------------------------------------------------------------
        | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
        -------------------------------------------------------------
        |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 |
        -------------------------------------------------------------
        """
        n = self._size
        val = [list(range(2*n+1, 3*n+1)), list(range(n+1, 2*n+1)), list(range(1, n+1))]
        return SYT3lines(val, check=False)

    def intervals(self):
        """
        Compute the list of all intervals classified by top element.

        EXAMPLES:

        >>> I = RectSYT3lines(1).intervals()
        >>> [len(I[top]) for top in I]
        [1]
        >>> I = RectSYT3lines(2).intervals()
        >>> [len(I[top]) for top in I]
        [5, 2, 2, 2, 1]
        >>> I = RectSYT3lines(3).intervals()
        >>> [len(I[top]) for top in I]
        [42, 17, 14, 27, 27, 14, 17, 13, 9, 18, 12, 5, 5, 4, 12, 18, 13, 5, 5, 9, 4, 4, 4, 9, 2, 2, 6, 6, 5, 6, 3, 2, 2, 3, 3, 6, 5, 3, 2, 1, 4, 2]
        >>> # I = RectSYT3lines(4).intervals()
        >>> # [len(I[top]) for top in I]
        # [462, 203, 145, 347, 299, 118, 299, 347, 145, 203, 174, 144, 203, 245, 286, 76, 154, 57, 41, 101, 154, 51, 77, 39, 94, 28, 50, 103, 94, 186, 222, 144, 221, 136, 136, 221, 186, 101, 51, 41, 57, 174, 76, 245, 203, 103, 50, 28, 28, 94, 28, 66, 21, 67, 47, 140, 10, 14, 10, 66, 14, 14, 42, 42, 35, 128, 33, 39, 10, 10, 10, 31, 18, 70, 70, 18, 31, 80, 48, 160, 166, 60, 67, 21, 38, 119, 103, 53, 38, 48, 21, 39, 67, 110, 157, 147, 119, 131, 128, 131, 147, 157, 110, 80, 106, 36, 73, 88, 36, 42, 42, 14, 14, 10, 10, 14, 35, 24, 49, 10, 10, 34, 60, 166, 160, 80, 21, 24, 73, 106, 80, 108, 33, 24, 10, 10, 33, 33, 108, 88, 67, 53, 103, 14, 10, 25, 82, 8, 8, 140, 253, 47, 18, 8, 8, 25, 82, 49, 34, 24, 18, 26, 17, 14, 12, 4, 6, 5, 4, 6, 43, 18, 83, 16, 6, 4, 127, 119, 119, 127, 6, 5, 4, 12, 14, 17, 26, 4, 4, 14, 18, 20, 12, 6, 7, 9, 38, 58, 82, 22, 30, 54, 12, 22, 50, 57, 94, 68, 43, 16, 65, 68, 94, 57, 50, 22, 12, 35, 34, 9, 26, 18, 57, 40, 6, 4, 5, 6, 26, 40, 57, 9, 12, 6, 88, 39, 12, 12, 12, 10, 5, 7, 10, 12, 12, 22, 5, 24, 59, 22, 30, 22, 38, 82, 58, 55, 26, 6, 18, 80, 10, 12, 51, 9, 9, 12, 12, 28, 27, 43, 6, 4, 34, 35, 14, 14, 12, 10, 51, 65, 45, 20, 14, 7, 10, 6, 56, 77, 5, 39, 77, 56, 27, 24, 6, 58, 38, 14, 7, 9, 43, 14, 38, 28, 31, 88, 31, 80, 12, 55, 26, 6, 8, 9, 40, 12, 20, 20, 27, 21, 6, 8, 21, 7, 72, 4, 6, 72, 27, 7, 4, 16, 13, 13, 5, 8, 8, 8, 25, 21, 21, 21, 43, 4, 3, 43, 4, 4, 11, 15, 25, 25, 54, 5, 10, 8, 29, 12, 41, 41, 3, 2, 30, 4, 11, 17, 20, 37, 6, 6, 4, 4, 3, 3, 2, 8, 12, 12, 4, 12, 40, 21, 20, 8, 54, 3, 2, 12, 8, 11, 30, 7, 4, 10, 3, 9, 46, 17, 7, 4, 19, 7, 7, 16, 21, 11, 4, 15, 14, 37, 29, 46, 21, 2, 7, 8, 19, 2, 7, 6, 14, 12, 7, 11, 2, 12, 10, 34, 15, 15, 34, 18, 18, 5, 2, 6, 4, 4, 3, 3, 11, 7, 10, 5, 15, 5, 5, 15, 2, 1, 8, 6, 4, 6, 5, 9, 29, 2, 6, 8, 13, 8]
        """
        max_elt = self.max_element()
        intervals = {max_elt : set([max_elt])}
        from copy import deepcopy
        new = True
        while new:
            new = False
            new_intervals = deepcopy(intervals)
            for top in intervals:
                for e in intervals[top]:
                    for child in e.lower_elements():
                        if child not in new_intervals:
                            new_intervals[child] = set([child])
                            new = True
                        if child not in new_intervals[top]:
                            new_intervals[top].add(child)
                            new = True
            intervals = new_intervals
        return intervals

                
        

#***********************************************************************
#   EXPERIMENTATIONS
#***********************************************************************

def global_height():
    """
    EXPERIENCE : look at the height of the prograph (number of layers)
    according the size of the prograph.

    There are a lot of result of the average height of a random binary
    tree. So what is the height of a random PC prograph ? What is the
    good experience to proceeed ?

    TESTS:

    >>> 1+1
    2
    """
    # This current experience try to compute an average rate of
    # height/size for large random prograph.  It seems to converge to
    # zero but very very slowly. Even for random prograph of size
    # 1000...
    size = 1
    rates = []
    while True:
        size += randint(0,1)
        if len(rates) > size // 4:
            rates.pop(0)
        print("SIZE : "+str(size))
        R = RectSYT3lines(size)
        S = R.random_element()
        rate = len(S.to_bialgebra_layers()) / size
        rates.append(rate)
        print(sum(rates) / len(rates))
