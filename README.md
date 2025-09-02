# PC-Prograph-Editor

A small application to illustrate some recent research results about Prographs and Triangulations of the sphere. With minimal interactions, the user can build rooted triangulations of the bipolar sphere. The application finely exploits the Hopf isomorphism between the triangulations of the sphere and the rectangular Young Standard tableaux with three lines. The calculations are largely carried out on the Young tableaux side.


## References

[Three-dimensional Catalan numbers and product-coproduct prographs](https://arxiv.org/abs/1704.00212) (N. B.)

[Product-Coproduct Prographs and Triangulations of the Sphere](https://arxiv.org/abs/2202.05757) (Justine Falque, N. B.)

## Documentation

This application has been written in **Python3** language with the **tkinter** library. Once downloaded, if your computer is Python3 and tkinter ready, you just need to launch the application by typing `./main.py` in a Unix console (or `python3 main.py` at the proper directory).

![écran de l'application](https://github.com/nborie/PC-Prograph-Editor/blob/main/IMG/screenshot1.png)

### Message and action buttons

North-west of the window present a message adapted the current state of the application and a set of buttons.

**Reset :** A clic will restart the triangulation at the simplest one with only two triangles.   
**Add point :** After a clic on this button, you will have to clic on the triangulation to add a point.   
**Move point :** After a clic on this button, you will have to select an existing point in the triangulation then make another clic to set a new position for the selected point. This action is dangerous. You should not try to move the extremal left and right points (because triangulations are rooted to the edge joining these two points). Also, you should try to produce a triangulation impossible to draw on the plane.   
**Overlay dual :** This will overlay the PC-prograph over the triangulation. Another clic on the button or any other action will disable the overlay drawn.   
**Schützenberger :** This will apply the Schützenberger involution on the triangulation, PC-prograph and Standard Young Tableau.   
**Select edge :** After a clic on this button, you will have to select an existing edge in the triangulation.   
**Flip up :** Once you have selected an edge, if this edge is flippable upper, clic here to apply the flip.    
**Flip down :** Once you have selected an edge, if this edge is flippable downer, clic here to apply the flip.   


### Bipolar triangulation

The left canvas presents the triangulation of the bipolar sphere with two kind of pieces. Since edges of the triangulation are oriented, one could have red pieces with two inputs and one output (possibly at infinity for the upper red triangle which is drawn rounded) ; or the pieces are blue with a single input and two outputs (the input can come from infinity for the bottom blue triangle which is drawn rounded). This is not the usual way to draw triangulations. 

### Rectangular Young Standard Tableaux with three lines

At the upper right part of the screen, the 3 rows rectangular standard Young tableau is displayed. This last one is computed by a depth first search transversal of the PC-Prograph.

### PC-prograph (dual side)

The right canvas presents the dual graph of the triangulation which is, by the theory, a Product-Coproduct prograph. Operators coproduct and product are placed at the gravity center of each triangle. Thus, we use some Bezier curves to link each operator using the edges of the triangulation.
