# Dense-Map

In order to se this code, you must have numpy library installed:

sudo apt-get install python-numpy

The user must have present a wifi.txt, constaining wifi readings and a .pgm containing the point cloud data.  
In the attached code, it is called "3rdFloor.pgm", change it as needed.

The user will need a .yaml file for the .pgm, "3rdFloor.yaml" in or case.  We also need a .yaml file for the rotated image we are about to make.  Simply copy and resave "3rdFloor.yaml" as "rotated.yaml"


Start by rotating your .pgm file to align with your floor plan.  Do this by using gimp:

gimp 3rdFloor.pgm

rotate the image and RECORD the angle of rotation.  (just write it down so you don't forget)

save the file as "rotated.pgm"

Now the user must rotate the wifi data to match with the rotated image:

python rotate.py

The program will ask for the angle of rotation.  Given the angle found previously--You must MULTIPLY BY -1 if using gimp, as gimp has different axes then we are used to.

Now we process the image, find the floor, and fill the data:

python makeBlocks.py

this may take a few minutes.

The dense map, with evenly spaced x,y cooridnates will be saved to denseMap.txt

Note:  Every single location may not have data.  If Readings are too far away, they will not be considered. The best way to ensre readings at every point is to sample the area adequately.  

In our case 93% of 0.5m x 0.5m blocks have wifi data
