# PC-Prograph-Editor

A small application to illustrate some recent research results about Prographs and Triangulations of the sphere. With minimal interactions, the user can build rooted triangulations of the bipolar sphere. The application finely exploits the Hopf isomorphism between the triangulations of the sphere and the rectangular Young Standard tableaux with three lines. The calculations are largely carried out on the Young tableaux side.


## References

[Three-dimensional Catalan numbers and product-coproduct prographs](https://arxiv.org/abs/1704.00212) (N. B.)

[Product-Coproduct Prographs and Triangulations of the Sphere](https://arxiv.org/abs/2202.05757) (Justine Falque, N. B.)

## Documentation

This application has been writen in **Python3** langage with the **tkinther** librairy. Once downloaded, if your computer is Python3 and tkinter ready, you just need to launch the application by typing `./main.py` in a Unix console (or `python3 main.py` at the proper directory).

![écran de l'application](https://github.com/nborie/PC-Prograph-Editor/blob/main/IMG/screenshot1.png)

### Message and action buttons

North-west of the window present a message adapted the current state of the application and a set of buttons.

**Reset :** A clic will restart the triangulation at the simpliest one with only two triangles.   
**Add point :** After a clic on this button, you will have to clic on the triangulation to add a point.   
**Move point :** After a clic on this button, you will have to select an existing point in the triangulation then make another clic to set a new position for the selected point. This action is dangerous. You should not try to move the extremal left and right points (because triangulations are rooted to the edge joinning these two points). Also, you should try to produce a triangulation impossible to draw on the plane.   
**Overlay dual :** This will overlay the PC-prograph over the triangulation. Another clic on the button or any other action will disable the overlay drawn.   
**Schützenberger :** This will apply the Schützenberger involution on the triangulation, PC-prograph and Standard Young Tableau.   
**Select edge :** After a clic on this button, you will have to select an existing edge in the triangulation.   
**Flip up :** Once you have selected an edge, if this edge is flipable upper, clic here to apply the flip.    
**Flip down :** Once you have selected an edge, if this edge is flipable downer, clic here to apply the flip.   


### Bipolar triangulation

TODO

### Rectangular Young Standard Tableaux with three lines

TODO

### PC-prograph (dual side)

TODO

