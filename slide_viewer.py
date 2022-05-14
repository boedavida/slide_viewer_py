# slide_viewer.py. Created with Python version 3.9.7, Numpy version 1.21.4 by David Boe, (C) by David Boe
"""Computes which pixel on a slide to retrieve and display in a pixel in slide 
viewer after a rotation of the slide by a user. 

Sets up a coordinate system for both the viewer and slide. The x- and y-axes 
are what you think they would be. The x-axis is horizontal; the y-axis is 
vertical. Coordinates are expressed as (x,y). Initially , when the slide is 
loaded, the coordinate systems of the slide and the viewer are aligned.

The viewer pixel coordinate and the slide coordinate currently displayed in 
the viewer pixel are encapsulated together in a Display object. As the slide
is rotated with respect to the viewer, the coordinate of the slide displayed 
in the viewer pixel is updated.

Rotation is accomplished by matrix multiplication with a rotation matrix. For 
further information on rotation matrices: https://mathworld.wolfram.com/RotationMatrix.html.

Here the operation is applied to one display pixel, but to get all of the slide 
pixels to display, this same operation is applied to every pixel. This operation
is embarrassingly parallel and so is amenable to GPU impleementation."""

import numpy as np

class Display:
    def __init__(self, Vx0, Vy0, Sx0, Sy0):
        self._Vx = Vx0 # Viewer pixel x-coordinate
        self._Vy = Vy0 # Viewer pixel y-coordinate
        self._Sx = Sx0 # Slide pixel x-coordinate displayed in viewer pixel x-coordinate
        self._Sy = Sy0 # Slide pixel y-coordinate displayed in viewer pixel y-coordinate
    
    # Setter/getter for _Vx
    def Vx(self, a=None):
        if a: self._Vx = a
        return self._Vx

    # Setter/getter for _Vy
    def Vy(self, b=None):
        if b: self._Vy = b
        return self._Vy

    # Setter/getter for _Sx
    def Sx(self, c=None):
        if c: self._Sx = c
        return self._Sx

    # Setter/getter for _Sy
    def Sy(self, d=None):
        if d: self._Sy = d
        return self._Sy

    def get_viewer_coords(self):
        return np.array([self.Vx(), self.Vy()])

    def get_slide_coords(self):
        return np.array([self.Sx(), self.Sy()])

    def rotate_slide(self, theta):
        # Form rotation matrix
        R = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
        X = np.matmul(R, self.get_slide_coords())
        self._Sx = X[0]
        self._Sy = X[1]
        return self.get_slide_coords()
        

def main():
    # Instantiate a display pixel object
    V1 = Display(1.0, 0.0, 1.0, 0.0)

    # Output display on initial loading
    print("\nOn initially loading the silde into the viewer:")
    print(f"Viewer pixel ({V1.Vx():.2f}, {V1.Vy():.2f}) displays slide pixel ({V1.Sx():.2f}, {V1.Sy():.2f})") 

    # User rotation - counter-clockwise rotation of the slide around the center
    angle = 90 # [ degrees ]
    theta = angle*np.pi/180 # [ radians ]
    # update the slide coordinate to display in the viewer pixel after the rotation
    slide_pixel_rot_1 = V1.rotate_slide(theta)

    # Output the slide pixel to display in the viewer after a rotation
    print(f"\nAfter a {angle} degree rotation of the slide by the user:")
    print(f"Viewer pixel ({V1.Vx():.2f}, {V1.Vy():.2f}) displays slide pixel ({slide_pixel_rot_1[0]:.2f}, {slide_pixel_rot_1[1]:.2f})")

    # Rotate back again
    angle = -angle # [ degrees ] Negative rotation angle is a clockwise rotation 
    theta = -theta # [ radians ]
    slide_pixel_rot_2 = V1.rotate_slide(theta)

    # Output the slide pixel to display in the viewer after a rotation
    print(f"\nAfter a {angle} degree rotation of the slide by the user:")
    print(f"Viewer pixel ({V1.Vx():.2f}, {V1.Vy():.2f}) displays slide pixel ({slide_pixel_rot_2[0]:.2f}, {slide_pixel_rot_2[1]:.2f})\n")


if __name__ == "__main__":
    main()
    

