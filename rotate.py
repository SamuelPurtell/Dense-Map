

f = open('wifi.txt', 'r')
lines = f.readlines()
f.close()

theta = input("\nAngle of rotation (degrees) > ")
theta = theta * 3.141592654 / 180
import math

newlines = [];
for i in range(len(lines)):
    ########################




    xs = 2;
    xf = lines[i].find('|')

    ys = lines[i].find('y:') + 2;
    yf = lines[i].find('|', ys)

    zs = lines[i].find('z:');

    x = eval(lines[i][xs:xf])
    y = eval(lines[i][ys:yf])


##        ##########################
##    xs = 3;
##    xf = lines[i].find(',')
##
##    ys = lines[i].find('y:\t') + 3;
##    yf = lines[i].find(',', ys)
##
##    zs = lines[i].find('z:\t');
##
##    x = eval(lines[i][xs:xf])
##    y = eval(lines[i][ys:yf])

    

    xnew = x*math.cos(theta) - y*math.sin(theta);
    ynew = y*math.cos(theta) + x*math.sin(theta);

    line = 'x:'+ ("%.6f"%xnew) +'||y:\t'+ ("%.6f"%ynew) +'||'+lines[i][zs:len(lines[i])]
    newlines.append(line)
    #print( str(x) +'\t' + str(y) )

ff = open('rotatedWifi.txt', 'w')
for j in range(len(newlines)):
    ff.write( str(newlines[j]) )
ff.close()


def wifiLocations(filename):
    
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    locations = numpy.zeros((len(lines),2), float)

    newlines = [];
    for i in range(len(lines)):
        xs = 2;
        xf = lines[i].find('|')

        ys = lines[i].find('y:') + 2;
        yf = lines[i].find('|', ys)

        zs = lines[i].find('z:');

        x = eval(lines[i][xs:xf])
        y = eval(lines[i][ys:yf])

        locations[i][0] = x
        locations[i][1] = y
    return locations
