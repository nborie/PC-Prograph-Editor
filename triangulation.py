"""
This module implement triangulations of the sphere build by hand.
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

from enum import Enum
from math import sqrt

class Paw(Enum):
    """
    A class whose instances model the different types of half-edge.
    """
    IN_LEFT_PROD = 1
    IN_RIGHT_PROD = 2
    OUT_PROD = 3
    IN_COPROD = 4
    OUT_LEFT_COPROD = 5
    OUT_RIGHT_COPROD = 6

class Operator(Enum):
    """
    A class whose instances model the two types of triangle.
    """
    PROD = 1
    COPROD = 2

def determinant2(v1, v2):
    """
    Returns the determinant of the two vectors `v1` and `v2` of 
    dimension `2`.

    EXAMPLES::
    >>> determinant2((0, 0), (13, 23))
    0
    >>> determinant2((1, 2), (3, 4))
    -2
    >>> determinant2((1, 2), (2, 4))
    0
    >>> determinant2((1, 2), (-7, -14))
    0
    >>> determinant2((2, 3), (5, 8))
    1
    """
    return v1[0]*v2[1] - v2[0]*v1[1]

def is_point_in_triangle(A, B, C, P):
    """
    Returns `True` if point `P` in inside triangle `ABC`. Returns `False`
    otherwise.

    EXAMPLES::
    >>> is_point_in_triangle((0, 0), (0, 3), (3, 0), (1, 1))
    True
    >>> is_point_in_triangle((0, 0), (0, 3), (1, 1), (3, 0))
    False
    >>> is_point_in_triangle((0, 0), (1, 1), (3, 0), (0, 3))
    False
    >>> is_point_in_triangle((1, 1), (0, 3), (3, 0), (0, 0))
    False
    """
    PA = (A[0] - P[0], A[1] - P[1])
    PB = (B[0] - P[0], B[1] - P[1])
    PC = (C[0] - P[0], C[1] - P[1])
    a = determinant2(PB, PC)
    b = determinant2(PC, PA)
    c = determinant2(PA, PB)
    if (a >= 0) and (b >= 0) and (c >= 0):
        return True
    if (a <= 0) and (b <= 0) and (c <= 0):
        return True
    return False

def combinaison_lineaire(A,B,u,v):
    return [A[0]*u+B[0]*v,A[1]*u+B[1]*v]

def interpolation_lineaire(A,B,t):
    return combinaison_lineaire(A,B,t,1-t)

def point_bezier_3(points_control,t):
    x=(1-t)**2
    y=t*t
    A = combinaison_lineaire(points_control[0],points_control[1],(1-t)*x,3*t*x)
    B = combinaison_lineaire(points_control[2],points_control[3],3*y*(1-t),y*t)
    return [A[0]+B[0],A[1]+B[1]]

def draw_bezier(canvas, p, width, fill, arrow=None, iteration=50):
    """
    Draw a Bezier curve from a list `p` of four points. The curve start
    at the point `p[0]` and end at the point `p[3]`. The curve has 
    for tangents the line `(p[0], p[1])` and line `(p[2], p[3])`.
    """
    # Start x and y coordinates, when t = 0
    x_start = p[0][0]
    y_start = p[0][1]
    # loops through
    for i in range(iteration+1):
        t = i / iteration
        x = (p[0][0] * (1-t)**3 + p[1][0] * 3 * t * (1-t)**2 + p[2][0] * 3 * t**2 * (1-t) + p[3][0] * t**3)
        y = (p[0][1] * (1-t)**3 + p[1][1] * 3 * t * (1-t)**2 + p[2][1] * 3 * t**2 * (1-t) + p[3][1] * t**3)
        if i == (iteration // 2) and arrow == 'last':
            canvas.create_line(x, y, x_start, y_start, width=width, fill=fill, arrow='first', arrowshape=(10,12,4))
        else:
            canvas.create_line(x, y, x_start, y_start, width=width, fill=fill)
        # updates initial values
        x_start = x
        y_start = y


class Triangulation():
    """
    A class modeling an embedded triangulation on the ball.


    """
    def __init__(self, size_x, size_y):
        """
        Initialise `self` to the smallest triangulation of the sphere.
        """
        self.size = (size_x, size_y)
        self.diam_circle = min([size_x - 60, size_y - 60])
        self.from_left = (size_x // 2) - (self.diam_circle // 2) + 20
        self.points = [[size_x//2, size_y//2], 
                       [self.from_left , size_y//2], 
                       [size_x-self.from_left, size_y//2]]
        self.triangles = [[[1, 0, 1], [0, 2, 2], [1, 2, 3]], 
                          [[1, 2, 4], [1, 0, 5], [0, 2, 6]]]
        self.from_top = (size_y // 2) - (self.diam_circle // 2) + 20
        self.dual_points = [[size_x//2, self.from_top, 1], 
                            [size_x//2, size_y-self.from_top, 2]]

    def number_of_triangles(self):
        """
        Returns the number of triangles inside the triangulation `self`.
        """
        return len(self.triangles)

    def draw_all(self, canvas):
        """
        Draw all elements of the triangulation inside a tkinter 
        given canvas
        """
        self.draw_fixed_part(canvas)
        self.draw_triangles(canvas)
        self.draw_edges(canvas)
        self.draw_edges_orientation(canvas)
        self.draw_points(canvas)

    def draw_points(self, canvas):
        """
        Draw the points (vertices of triangles) appearing in the 
        triangulation `self`
        """
        diam = 8
        color = 'black'
        for (a, b) in self.points:
            A=(a-(diam//2), b-(diam//2))
            B=(a+(diam//2), b+(diam//2))
            canvas.create_oval(A, B, fill=color, outline=color, width=3)

    def draw_triangles(self, canvas):
        """
        Draw the normal non infinte triangles inside `self`.
        """
        pts = self.points
        size_x, size_y = self.size
        if pts[self.triangles[0][0][1]][1] > (size_y // 2):
            A = pts[1]
            B = pts[2]
            C = pts[self.triangles[0][0][1]]
            canvas.create_polygon(A[0], A[1], B[0], B[1], C[0], C[1], fill='lightsalmon1')
        if pts[self.triangles[1][1][1]][1] < (size_y // 2):
            A = pts[1]
            B = pts[2]
            C = pts[self.triangles[1][1][1]]
            canvas.create_polygon(A[0], A[1]+1, B[0], B[1]+1, C[0], C[1], fill='light blue')
        for i in range(2, self.number_of_triangles()):
            inda = -1
            indb = -1
            indc = -1
            (s1, s2, _) = self.triangles[i]
            inda = s1[0]
            indb = s1[1]
            if s2[0] not in [inda, indb]:
                indc = s2[0]
            else:
                indc = s2[1]
            A = pts[inda]
            B = pts[indb]
            C = pts[indc]
            if s1[2] in [1, 2, 3]:
                canvas.create_polygon(A[0], A[1], B[0], B[1], C[0], C[1], fill='lightsalmon1')
            else:
                canvas.create_polygon(A[0], A[1], B[0], B[1], C[0], C[1], fill='light blue')

    def draw_common_fixed_part(self, canvas):
        """
        Draw an adapted circle representing the sphere and the four cardinate
        """
        size_x, size_y = self.size
        # draw the visible part of the sphere
        diam = self.diam_circle
        A = (size_x//2 - (diam//2) , size_y//2 - (diam//2))
        B = (size_x//2 + (diam//2) , size_y//2 + (diam//2))
        canvas.create_oval(A, B, outline='gray30', width=1, fill='white')
        # draw the four cardinate direction
        canvas.create_text(size_x//2+20, 16, text="N", fill="black", font="Times 16 bold")
        canvas.create_text(size_x//2+20, size_y-10, text="S", fill="black", font="Times 16 bold")
        canvas.create_text(16, size_y//2-15, text="W", fill="black", font="Times 16 bold")
        canvas.create_text(size_x-16, size_y//2-15, text="E", fill="black", font="Times 16 bold")

    def draw_fixed_part(self, canvas):
        """
        Draw the fixed part of the triangulation `self`.
        * the two unmovable points close West and East.
        * the infinite edge passing the dark side of the sphere.
        * the color area for product and coproduct joinning at infinity.
        * The four direction N, S, W, and E.
        """
        self.draw_common_fixed_part(canvas)
        size_x, size_y = self.size
        diam = self.diam_circle
        A = (size_x//2 - (diam//2) , size_y//2 - (diam//2))
        B = (size_x//2 + (diam//2) , size_y//2 + (diam//2))
        canvas.create_arc(A, B, outline="gray30", extent=180, start=180, fill="light blue",  width=1)
        canvas.create_arc(A, B, outline="gray30", extent=180, start=0, fill="lightsalmon1",  width=1)
        
        # draw the splitted edge at infinity
        canvas.create_line(self.from_left, size_y//2, self.from_left-30, size_y//2, width=2, fill='black')
        canvas.create_line(size_x - self.from_left, size_y//2, size_x - (self.from_left-30), size_y//2, width=2, fill='black')
        abs = self.from_left-32
        for i in range(5):
            canvas.create_line(abs, size_y//2, abs-2, size_y//2, width=2, fill='black')
            canvas.create_line(size_x - abs, size_y//2, size_x - (abs-2), size_y//2, width=2, fill='black')
            abs -=4

    def draw_edges_orientation(self, canvas):
        """
        """
        for tri in self.triangles:
            for orig, end, _ in tri:
                if [orig, end] == [1, 2] or [orig, end] == [2, 1]:
                    continue
                A = self.points[orig]
                B = self.points[end]
                x = (2*A[0] + B[0]) / 3
                y = (2*A[1] + B[1]) / 3
                norm = sqrt( (B[0]-A[0])**2 + (B[1]-A[1])**2 )
                nx = (B[0] - A[0]) / norm
                ny = (B[1] - A[1]) / norm
                ox = ny
                oy = -nx
                size = 10
                canvas.create_line((x-size*ox, y-size*oy), (x+1.5*size*ox, y+1.5*size*oy), fill="black", width=3, arrow="last")

    def get_edge_type(self, orig, end):
        """
        Return a tuple `(type_of_output, type_of_input)` fully describing 
        the type of the edge going from `orig` to `end`.
        """
        t_out = -1
        t_in = -1
        for tri in self.triangles:
            for o, e, t in tri:
                if o == orig and e == end:
                    if t in [3, 5, 6]:  # output
                        t_out = t
                    else: # t is thus an input
                        t_in = t
        return (t_out, t_in)

    def is_flipable_down(self, orig, end):
        """
        Return `True` if the edge going from`orig` to `end` is flipable down
        inside the triangulation `self`.
        """
        return self.get_edge_type(orig, end) in [(3, 1), (6, 4), (5, 2), (3, 4)]

    def is_flipable_up(self, orig, end):
        """
        Return `True` if the edge going from`orig` to `end` is flipable up 
        inside the triangulation `self`.
        """
        return self.get_edge_type(orig, end) in [(3, 2), (5, 4), (3, 4), (6, 1)]

    def flip_down(self, orig, end):
        """
        Flip down the edge inside the triangulation `self`.
        """
        out = -1
        input = -1 # type de demi arrête
        tout = -1
        tinp = -1 # indices des triangles
        indout = -1
        indinp = -1 # indices des troisièmes points
        for i in range(len(self.triangles)):
            tri = self.triangles[i]
            for o, e, t in tri:
                if o == orig and e == end:
                    if t in [3, 5, 6]:  # output
                        out = t
                        tout = i
                    else: # t is thus an input
                        input = t
                        tinp = i
        # recherche des indices des troisièmes points
        tri = self.triangles[tout]
        for o, e, _ in tri:
            if o != orig and o != end:
                indout = o
            if e != orig and e != end:
                indout = e
        # recherche des indices des troisièmes points
        tri = self.triangles[tinp]
        for o, e, _ in tri:
            if o != orig and o != end:
                indinp = o
            if e != orig and e != end:
                indinp = e
        # Change (orig, end) into the other 
        if (out, input) in [(3, 1)]:
            print("flip down !")
            tri_down = self.triangles[tout]
            tri_up = self.triangles[tinp]
            for i in range(3):
                _, _, t = tri_down[i]
                if t == 3:
                    tri_down[i] = [indout, indinp, 3]
                # echange two edges between bottom and top
                if t == 1:
                    for j in range(3):
                        _, _, tb = tri_up[j]
                        if tb == 2:
                            swap_edge = tri_up[j]
                            tri_up[j] = tri_down[i]
                            tri_down[i] = swap_edge
            for i in range(3):
                o, e, _ = tri_up[i]
                if o == orig and e == end:
                    tri_up[i] = [indout, indinp, 2]


    def flip_up(self, orig, end):
        """
        Flip up the edge inside the triangulation `self`.
        """
        pass

    def draw_edges(self, canvas):
        """
        Draw edges appearing inside the triangulation `self`.
        """
        flip_up_color = 'yellow'
        flip_down_color = 'sea green'
        for tri in self.triangles:
            for orig, end, _ in tri:
                if [orig, end] == [1, 2] or [orig, end] == [2, 1] :
                    continue
                A = self.points[orig]
                B = self.points[end]
                if self.is_flipable_down(orig, end):
                    if self.is_flipable_up(orig, end):
                        canvas.create_line(A[0], A[1], B[0], B[1], width=6, fill=flip_down_color)
                        canvas.create_line(A[0], A[1], B[0], B[1], width=6, fill=flip_up_color, dash=(8, 8))
                    else:
                        canvas.create_line(A[0], A[1], B[0], B[1], width=6, fill=flip_down_color)
                else:
                    if self.is_flipable_up(orig, end):
                        canvas.create_line(A[0], A[1], B[0], B[1], width=6, fill=flip_up_color)
                    else:
                        canvas.create_line(A[0], A[1], B[0], B[1], width=1, fill='black')

    def update_dual_points(self):
        """
        Update all coordinates of dual points
        """
        pts = self.points
        size_x, size_y = self.size
        for i in range(2, self.number_of_triangles()):
            inda = -1
            indb = -1
            indc = -1
            (s1, s2, _) = self.triangles[i]
            inda = s1[0]
            indb = s1[1]
            t = s1[2]
            if s2[0] not in [inda, indb]:
                indc = s2[0]
            else:
                indc = s2[1]
            A = pts[inda]
            B = pts[indb]
            C = pts[indc]
            dual_p = [ (A[0] + B[0] + C[0]) // 3, (A[1] + B[1] + C[1]) // 3 ]
            # dilatation from middle
            # if dual_p[1] < (size_y // 2):
            #     diff = (size_y // 2) - dual_p[1]
            #     dual_p[1] -= diff
            # elif dual_p[1] > (size_y // 2):
            #     diff = dual_p[1] - (size_y // 2)
            #     dual_p[1] += diff
            # correction prod or coprod
            if t in [1, 2, 3]:
                dual_p[1] -= 10
            else:
                dual_p[1] += 10
            if s1[2] in [1, 2, 3]:
                dual_p.append(1)
            else:
                dual_p.append(2)
            if len(self.dual_points) > i:
                self.dual_points[i] = dual_p
            else:
                self.dual_points.append(dual_p)

    def draw_all_dual(self, canvas):
        """
        Draw all elements in the dual side : the PC prograph associated 
        the triangulation.
        """
        self.draw_fixed_part_dual(canvas)
        self.draw_edge_dual(canvas)
        self.draw_operators(canvas)

    def draw_fixed_part_dual(self, canvas):
        """
        """
        self.draw_common_fixed_part(canvas)

    def draw_operators(self, canvas):
        """
        Draw products and coproducts inside the PC prograph associated to `self`.
        """
        for (x, y, t) in self.dual_points:
            if t == 1:
                canvas.create_polygon(x, y-10, x-9, y+8, x+9, y+8, fill='red3')
            else:
                canvas.create_polygon(x+9, y-8, x-9, y-8, x, y+10, fill='blue')

    def draw_half_edge_dual(self, canvas, i, j, t, x, y):
        """
        """
        p = []
        pts = self.points
        end = ( (pts[i][0] + pts[j][0]) // 2, (pts[i][1] + pts[j][1]) // 2 )
        side = ( pts[i][0] - pts[j][0], pts[i][1] - pts[j][1] )
        norm = sqrt(side[0]**2 + side[1]**2)
        ortho = ( side[1] / norm, -side[0] / norm) 
        start = ( x, y )
        p.append(start)
        coef_tangent = 15 # adjust the impact of tangents for Bézier curves.
        if t == 1:
            start = ( x-6, y+5 )
            p.append( ( x-6-coef_tangent, y+5+coef_tangent ) )
            arrow=None
        elif t == 2:
            start = ( x+6, y+5 )
            p.append( ( x+6+coef_tangent, y+5+coef_tangent ) )
            arrow=None
        elif t == 3:
            start = ( x, y-7 )
            p.append( ( x, y-7-((14*coef_tangent) // 10) ) )
            arrow='last'
        elif t == 4:
            start = ( x, y+7 )
            p.append( ( x, y+7+((14*coef_tangent) // 10) ) )
            arrow=None
        elif t == 5:
            start = ( x-6, y-5 )
            p.append( ( x-6-coef_tangent, y-5-coef_tangent ) )
            arrow='last'
        elif t == 6:
            start = ( x+6, y-5 )
            p.append( ( x+6+coef_tangent, y-5-coef_tangent ) )
            arrow='last'
        if arrow == 'last':
            p.append( (end[0]+int(ortho[0]*coef_tangent), end[1]+int(ortho[1]*coef_tangent)) )
        else:
            p.append( (end[0]-int(ortho[0]*coef_tangent), end[1]-int(ortho[1]*coef_tangent)) )
        p.append(end)
        p.append(end)
        draw_bezier(canvas, p, width=3, fill='violet red', arrow=arrow, iteration=50)
        # canvas.create_line(start[0], start[1], end[0], end[1], width=2, fill='violet red')

    def draw_edge_dual(self, canvas):
        """
        """
        (s1, s2, s3) = self.triangles[0]
        x, y, _ = self.dual_points[0]
        self.draw_half_edge_dual(canvas, s1[0], s1[1], s1[2], x, y)
        self.draw_half_edge_dual(canvas, s2[0], s2[1], s2[2], x, y)
        canvas.create_line(x, y-7, x, y-27, width=2, fill='violet red')
        for i in range(5):
            canvas.create_line(x, y-29, x, y-31, width=2, fill='violet red')
            y -= 4
        (s1, s2, s3) = self.triangles[1]
        x, y, _ = self.dual_points[1]
        self.draw_half_edge_dual(canvas, s2[0], s2[1], s2[2], x, y)
        self.draw_half_edge_dual(canvas, s3[0], s3[1], s3[2], x, y)
        canvas.create_line(x, y+7, x, y+27, width=2, fill='violet red')
        for i in range(5):
            canvas.create_line(x, y+29, x, y+31, width=2, fill='violet red')
            y += 4
        for i in range(2, self.number_of_triangles()):
            (s1, s2, s3) = self.triangles[i]
            x, y, _ = self.dual_points[i]
            self.draw_half_edge_dual(canvas, s1[0], s1[1], s1[2], x, y)
            self.draw_half_edge_dual(canvas, s2[0], s2[1], s2[2], x, y)
            self.draw_half_edge_dual(canvas, s3[0], s3[1], s3[2], x, y)

    def find_triangle(self, x, y):
        """
        Return the index of the triangle in inside the trangulation `self`
        in which the point lives.
        """
        pts = self.points
        for i in range(2, self.number_of_triangles()):
            inda = -1
            indb = -1
            indc = -1
            (s1, s2, _) = self.triangles[i]
            inda = s1[0]
            indb = s1[1]
            if s2[0] not in [inda, indb]:
                indc = s2[0]
            else:
                indc = s2[1]
            A = pts[inda]
            B = pts[indb]
            C = pts[indc]
            if is_point_in_triangle(A, B, C, (x, y) ):
                return i
        if y <= (self.size[1] // 2):
            return 0
        return 1

    def find_closest_point(self, x, y):
        """
        """
        pts = self.points
        size_x, size_y = self.size
        dist_min = size_x**2 + size_y**2
        ind_min = -1
        for i in range(len(pts)):
            a, b = pts[i]
            dist = (a-x)**2 + (b-y)**2
            if dist < dist_min:
                dist_min = dist
                ind_min = i        
        return ind_min

    def find_closest_edge(self, x, y):
        """
        return the closest edge to the point `(x, y)`.
        """
        size_x, size_y = self.size
        dist_min = size_x**2 + size_y**2
        orig = -1
        end = -1
        for i in range(self.number_of_triangles()):
            for (o, e, _) in self.triangles[i]:
                if o == 1 and e == 2:
                    continue
                A = self.points[o]
                B = self.points[e]
                dist = (x-A[0])**2 + (y-A[1])**2 + (x-B[0])**2 + (y-B[1])**2
                dist /= (A[0]-B[0])**2 + (A[1]-B[1])**2
                if dist < dist_min:
                    orig = o
                    end = e
                    dist_min = dist
        return (orig, end)

    def draw_selected_point(self, index, canvas):
        """
        Emphase selected point by the user.
        """
        diam = 14
        color = 'violet red'
        a, b = self.points[index]
        A=(a-(diam//2), b-(diam//2))
        B=(a+(diam//2), b+(diam//2))
        canvas.create_oval(A, B, fill='violet red', outline=color, width=2)
        diam = 22
        A=(a-(diam//2), b-(diam//2))
        B=(a+(diam//2), b+(diam//2))
        canvas.create_oval(A, B, outline=color, width=2)

    def draw_middle_edge(self, canvas):
        """
        Emphase the middle of each edge to help the user selecting them.
        """
        for tri in self.triangles:
            for orig, end, _ in tri:
                if [orig, end] == [1, 2]:
                    continue
                A = self.points[orig]
                B = self.points[end]
                M = ((A[0]+B[0]) // 2, (A[1]+B[1]) // 2)
                canvas.create_oval(M, M, width=14, outline='violet red')

    def draw_selected_edge(self, orig, end, canvas):
        """
        Emphase selected edge.
        """
        A = self.points[orig]
        B = self.points[end]
        canvas.create_line(A[0], A[1], B[0], B[1], width=12, fill='violet red')

    def add_point(self, x, y, canvas):
        """
        add the point at coordinate `(x, y)` inside the 
        triangulation `self`.
        """
        ind_new_point = len(self.points)
        self.points.append( [x, y] )
        ind_triangle = self.find_triangle( x, y )
        s1 = self.triangles[ind_triangle][0].copy()
        s2 = self.triangles[ind_triangle][1].copy()
        s3 = self.triangles[ind_triangle][2].copy()

        # first case : upper infinite triangle
        if ind_triangle == 0:
            p3 = [self.triangles[0][0][1], ind_new_point]
            self.triangles[0][0][1] = ind_new_point
            self.triangles[0][1][0] = ind_new_point
            p1 = self.triangles[0][0]
            p2 = self.triangles[0][1]

            self.triangles.append( [[s1[0], s1[1], 1], [p1[0], p1[1], 3], [p3[0], p3[1], 2]] )
            self.triangles.append( [[p2[0], p2[1], 6], [s2[0], s2[1], 4], [p3[0], p3[1], 5]] )
        # first case : lower infinite triangle
        elif ind_triangle == 1:
            p1 = [ind_new_point, self.triangles[1][1][1]]
            self.triangles[1][1][1] = ind_new_point
            self.triangles[1][2][0] = ind_new_point
            p2 = self.triangles[1][1]
            p3 = self.triangles[1][2]

            self.triangles.append( [[s3[0], s3[1], 6], [p3[0], p3[1], 4], [p1[0], p1[1], 5]] )
            self.triangles.append( [[p2[0], p2[1], 1], [s2[0], s2[1], 3], [p1[0], p1[1], 2]] )

        # Now begin general case : but coprod or prod
        # first : COPROD case
        elif s1[2] in [4, 5, 6]:
            # Be sure s1 is old input of coproduct
            if self.triangles[ind_triangle][0][2] == 4:
                s1 = self.triangles[ind_triangle][0].copy()
            elif self.triangles[ind_triangle][1][2] == 4:
                s1 = self.triangles[ind_triangle][1].copy()
            else:
                s1 = self.triangles[ind_triangle][2].copy()

            # Be sure s2 is old left output of coproduct
            if self.triangles[ind_triangle][0][2] == 5:
                s2 = self.triangles[ind_triangle][0].copy()
            elif self.triangles[ind_triangle][1][2] == 5:
                s2 = self.triangles[ind_triangle][1].copy()
            else:
                s2 = self.triangles[ind_triangle][2].copy()

            # Be sure s3 is old right output of coproduct 
            if self.triangles[ind_triangle][0][2] == 6:
                s3 = self.triangles[ind_triangle][0].copy()
            elif self.triangles[ind_triangle][1][2] == 6:
                s3 = self.triangles[ind_triangle][1].copy()
            else:
                s3 = self.triangles[ind_triangle][2].copy()

            p1 = [ind_new_point, s2[1]]
            p2 = [ind_new_point, s1[1]]
            p3 = [s1[0], ind_new_point]

            self.triangles[ind_triangle] = [[s1[0], s1[1], 4], [p3[0], p3[1], 5], [p2[0], p2[1], 6]]
            self.triangles.append( [[p2[0], p2[1], 4], [p1[0], p1[1], 5], [s3[0], s3[1], 6]] )
            self.triangles.append( [[p3[0], p3[1], 1], [p1[0], p1[1], 2], [s2[0], s2[1], 3]] )

        # last case : PROD case
        else:
            # Be sure s1 is old left input of product
            if self.triangles[ind_triangle][0][2] == 1:
                s1 = self.triangles[ind_triangle][0].copy()
            elif self.triangles[ind_triangle][1][2] == 1:
                s1 = self.triangles[ind_triangle][1].copy()
            else:
                s1 = self.triangles[ind_triangle][2].copy()
            # Be sure s2 is old right input of coproduct
            if self.triangles[ind_triangle][0][2] == 2:
                s2 = self.triangles[ind_triangle][0].copy()
            elif self.triangles[ind_triangle][1][2] == 2:
                s2 = self.triangles[ind_triangle][1].copy()
            else:
                s2 = self.triangles[ind_triangle][2].copy()
            # Be sure s3 is old output of coproduct
            if self.triangles[ind_triangle][0][2] == 3:
                s3 = self.triangles[ind_triangle][0].copy()
            elif self.triangles[ind_triangle][1][2] == 3:
                s3 = self.triangles[ind_triangle][1].copy()
            else:
                s3 = self.triangles[ind_triangle][2].copy()

            p1 = [ind_new_point, s2[1]]
            p2 = [s1[0], ind_new_point]
            p3 = [s1[1], ind_new_point]

            self.triangles[ind_triangle] = [[s1[0], s1[1], 1], [p3[0], p3[1], 2], [p2[0], p2[1], 3]]
            self.triangles.append( [[s2[0], s2[1], 4], [p3[0], p3[1], 5], [p1[0], p1[1], 6]] )
            self.triangles.append( [[p2[0], p2[1], 1], [p1[0], p1[1], 2], [s3[0], s3[1], 3]] )

        self.draw_all(canvas)
        self.update_dual_points()

    def has_edge(self, ind_tri, orig, end):
        """
        Return the demi-edge type of `(orig, end)` if its bellong to
        triangle indexed by `ind_tri` inside the triangulation `self`.
        Return `-1` otherwise.
        """
        edges = self.triangles[ind_tri]
        for o, e, t in edges:
            if orig == o and end == e:
                return t
        return -1

    def get_edge_of_type(self, ind_tri, t):
        """
        Return the edge of type `t` inside triangle indexed by `ind_tri`
        inside the triangulation `self`. The user is responsible and
        should give valid argument to this method.
        """
        edges = self.triangles[ind_tri]
        for e in edges:
            if e[2] == t:
                return e
        return None

    def to_standard_young_tableau(self):
        """
        """
        ans = [[], [], [1]] 
        endding_edge = self.triangles[0][1]
        current_edge = self.triangles[1][1]
        stack_coprod = [1]
        current_triangle = 1
        current_index = 2
        while len(ans[0]) < (self.number_of_triangles() // 2):
            for i in range(self.number_of_triangles()):
                t = self.has_edge(i, current_edge[0], current_edge[1])
                if t != -1 and i != current_triangle:
                    if t == 1: # left input of product
                        ans[1].append(current_index)
                        current_index += 1
                        current_triangle = stack_coprod.pop(-1)
                        # Next edge : right output of last visited coproduct
                        current_edge = self.get_edge_of_type(current_triangle, 6)
                        break
                    elif t == 2: # right input of product
                        ans[0].append(current_index)
                        current_index += 1
                        current_triangle = i
                        # Next edge : the only output of the product on which we are
                        current_edge = self.get_edge_of_type(current_triangle, 3) 
                        break
                    elif t == 4: # t MUST BE 4 : input of coproduct
                        ans[2].append(current_index)
                        current_index += 1
                        current_triangle = i
                        stack_coprod.append(i)
                        # Next edge : the left output of the coproduct on which we are
                        current_edge = self.get_edge_of_type(current_triangle, 5) 
                        break
        return ans
        
    def schutzenberger_involution(self):
        """
        Apply the Schützenberger involution on `self`.
        """
        # We flip all point but we do not touch [1] and [2]
        size_x, size_y = self.size
        for i in range(len(self.points)):
            self.points[i][0] = size_x - self.points[i][0]
            self.points[i][1] = size_y - self.points[i][1]
        # we reverse coordinate of [1] and [2]
        self.triangles[0], self.triangles[1] = list(reversed(self.triangles[1])), list(reversed(self.triangles[0]))
        for i in range(len(self.triangles)):
            for seg in self.triangles[i]:
                seg[0], seg[1] = seg[1], seg[0]
                if seg[2] == 1:
                    seg[2] = 6
                elif seg[2] == 2:
                    seg[2] = 5
                elif seg[2] == 3:
                    seg[2] = 4
                elif seg[2] == 4:
                    seg[2] = 3
                elif seg[2] == 5:
                    seg[2] = 2
                elif seg[2] == 6:
                    seg[2] = 1
        self.update_dual_points()