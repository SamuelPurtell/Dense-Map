# -*- coding: utf-8 -*-
import re
import array
import numpy
import math

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

def getResolution(filename):
    if filename.find('.yaml') < 0:
        t = filename.find('.')
        newname = filename[0:t]
        newname = newname + ".yaml"
        filename = newname
        
    f = open(filename, 'r')
    data = f.read()
    f.close()

    t1 = data.find('resolution')
    t2 = data.find(':', t1)
    t3 = data.find('\n', t2)

    resolution =  eval(data[t2+1:t3]);
    return resolution

def wifiReadings(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    data = [];

    for i in range(len(lines)):
        oneline = []
        line = lines[i]

        t1 = line.find('MAC: ')
        t2 = line.find(', Str')
        t3 = line.find(']')
        
        while(t1 != -1):
            oneline.append([line[t1+5:t2], eval(line[t2+5:t3])])
   
            t1 = line.find('MAC: ', t2)
            t2 = line.find(', Str', t1)
            t3 = line.find(']', t2)
            
        data.append(oneline)
        del oneline
    return(data)

def oneLineWifi(line):
    oneline = []

    t1 = line.find('MAC: ')
    t2 = line.find(', Str')
    t3 = line.find(']', t2)
    
    while(t1 != -1):
        print ( line[t1:t2])
        print ( line[t2+3: t3])
        
        t1 = line.find('MAC: ', t2)
        t2 = line.find(', Str', t1)
        t3 = line.find(']', t2)
        

##def getAllMacs(filename):
##    f = open(filename, 'r')
##    data = f.read()
##    f.close()
##
##    macs = []
##    
##    t1 = 0; t2 = 0;
##    while(t1 > -1):
##        t1 = data.find('MAC: ', t2)
##        t2 = data.find(', Str', t1)
##        macs.append(data[t1:t2])
##
##    return macs
        
def getMacs(wifiData):
    macList = [];
    for i in range(len(wifiData)):
        for j in range(len(wifiData[i])):
            if wifiData[i][j][0] not in macList:
                macList.append(wifiData[i][j][0]);
    return(macList)
    
def pixelToWifi(wifiData, pixelCount, xCount):
    pixelCount = float(pixelCount);
    
    xcoor = (wifiData[:,0] * xCount/pixelCount) - xCount/2.0;
    ##ycoor = ( xCount/2.0 - wifiData[:,1] ) * xCount/pixelCount;
    ycoor = xCount/2.0 - (wifiData[:,1] * xCount/pixelCount)

    pixelData = numpy.array(wifiData)  ## copy to get the shape
    pixelData[:,0] = xcoor;
    pixelData[:,1] = ycoor;

    return pixelData

def wifiToPixel(pixelData, pixelCount, xCount):
    
    xpixel  = ( pixelData[:,0] + xCount/2 ) * pixelCount/xCount;
    ypixel = pixelCount - ( pixelData[:,1] + xCount/2 ) * pixelCount/xCount;
    ##ypixel = ( pixelCount - pixelData[:,1] ) * xCount/pixelCount - xCount/2.0;
    #wifiData = numpy.array(pixelData, 'uint8')
    wifiData = numpy.array(pixelData)
    wifiData[:,0] = xpixel
    wifiData[:,1] = ypixel

    return wifiData

def read_pgm(filename, byteorder='>'):

    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    return numpy.frombuffer(buffer,
                            dtype='u1' if int(maxval) < 256 else byteorder+'u2',
                            count=int(width)*int(height),
                            offset=len(header)
                            ).reshape((int(height), int(width)))


def wifiToPGM(wifiData, pgmfileread):
    from matplotlib import pyplot
    ##blocksize = 10 # 10 pixels * 0.050 m/pixel = 0.5m
    resolution = getResolution(pgmfileread)  ## get resolution from .yaml file
    blocksize = int(0.5 / resolution) ## number of pixels = 0.5m / resoultion
    
    
    halfTile = 0.05 * blocksize * 0.5 ##### NOT RIGHT
    ##halfTile = 
    tileList = []

    pixelThreshold = 0.5 * blocksize * blocksize # 50% of pixels is a full block
    
    #image = read_pgm("rotated.pgm", byteorder='<')
    image = read_pgm(pgmfileread, byteorder='<')  
    height = len(image)
    width = len(image[0])

    for yblock in range(0, height, blocksize):
        for xblock in range(0, width, blocksize):
            block = image[yblock:yblock+blocksize][:,xblock:xblock+blocksize]
            booleanMat = (block==254)

            if numpy.sum(booleanMat) > pixelThreshold:
                ## make timile ##
                ##tileList.append([xblock + halfTile, yblock + halfTile])
                tileList.append([xblock, yblock]) ## this gives a 

    buff = 205 * numpy.ones((height, width), 'B')

    print('filling in visual markers')
    ## write in colored dots here
    for q in range(len(tileList)):
        ##buff[tileList[q][1]][tileList[q][0]] = 0 ## buff[y][x] = ...[x, y]
        for t in range(blocksize):
            buff[tileList[q][1]+t][tileList[q][0]] = 100;
            buff[tileList[q][1]][tileList[q][0]+t] = 100;
            buff[tileList[q][1]+blocksize-t][tileList[q][0]+blocksize] = 100;
            buff[tileList[q][1]+blocksize][tileList[q][0]+blocksize-t] = 100;

    # add the wifi readings here
    pix = wifiToPixel(wifiData, len(buff), len(buff)/10 )
    pixelized = numpy.array(pix, 'uint16')
    for m in range(len(pixelized)):
        ##buff[pixelized[m][1]][pixelized[m][0]] = 0;  ## another color

        buff[pixelized[m][1]][pixelized[m][0]] = 0;  ## another color
        buff[pixelized[m][1]][pixelized[m][0]-1] = 0;  ## another color
        buff[pixelized[m][1]][pixelized[m][0]+1] = 0;  ## another color
        
        buff[pixelized[m][1]+1][pixelized[m][0]] = 0;  ## another color
        buff[pixelized[m][1]+1][pixelized[m][0]-1] = 0;  ## another color
        buff[pixelized[m][1]+1][pixelized[m][0]+1] = 0;  ## another color

        buff[pixelized[m][1]-1][pixelized[m][0]] = 0;  ## another color
        buff[pixelized[m][1]-1][pixelized[m][0]-1] = 0;  ## another color
        buff[pixelized[m][1]-1][pixelized[m][0]+1] = 0;  ## another color
        
        
    # open file for writing 
    filename = 'tilewithwifi.pgm'
    try:
      fout=open(filename, 'wb')
    except IOError, er:
      print "Cannot open file ", filename, "Exiting … \n", er
      sys.exit()

    # define PGM Header
    pgmHeader = 'P5' + '\n' + str(width) + '  ' + str(height) + '  ' + str(255) + '\n'

    # write the header to the file
    fout.write(pgmHeader)

    # write the data to the file 
    buff.tofile(fout)

    # close the file
    fout.close()

def macInSingle(mac, oneReading):
    for i in range(len(oneReading)):
        if(mac==oneReading[i][0]):
           return(True)
    return(False)

def getMacStr(mac, oneReading):
    for i in range(len(oneReading)):
        if(mac==oneReading[i][0]):
            return(oneReading[i][1])

##def sumSampleFast(index, wifiData, tolerance, mac):
##    wifiSum = 0;
##    samples = 0;
##    for i in getOneNeighbors(blockList,

def getWifiNeighbors(blockList, wifiLoc, tolerance):
    ##2 Dimensional list
    # [ [wifiLoc[0] neighbors], [wifiLoc[1] neighbors] .... ]
    bigList = [];
    for eachBlock in blockList:
        oneNeighbors = [];
        x1 = eachBlock[0];
        y1 = eachBlock[1];
        for t in range(len(wifiLoc)):
            x2 = wifiLoc[t][0];
            y2 = wifiLoc[t][1];
            if((x1<=x2) and (y1<=y2)):  #check Lower bounds
                if((x2<x1+tolerance) and (y2<y1+tolerance)): # check upper bound
                    oneNeighbors.append(t)  ## add the the list
        bigList.append(oneNeighbors)
    return(bigList);

def countFull(wifiNeighbors):
    full = 0;
    for i in wifiNeighbors:
        if(len(i))>0:
            full += 1
    return(full)
                    
def fastSumSamples(blockList, index, wifiData, wifiNeighbors, mac):
    wifiSum = 0;
    samples = 0;
    neighbors = wifiNeighbors[index];  ## neighbors of blockList[index]
    for i in neighbors:
        if macInSingle(mac, wifiData[i] ):
            wifiSum += getMacStr(mac, wifiData[i]);
            samples +=1;
    return(wifiSum, samples)
    

##def getSumSamples(xcoor, ycoor, wifiData, tileSize, mac):
##    wifiSum = 0;
##    samples = 0;
##    for reading in wifiData:  ## for every reading
##        if macInSingle(mac, reading):  # is MACxx:xx:xx:xx in this reading
##            if( (xcoor < reading[0]) and (reading[0] < xcoor + tileSize) ):
##                if ( (ycoor < reading[1] ) and (reading[1] < ycoor + tileSize) ):
##                    wifiSum += getMacStr(mac, reading);
##                    samples += 1;
##    return(wifiSum, samples)

def getSumSamples(xcoor, ycoor, wifiData, tileSize, mac):
    wifiSum = 0;
    samples = 0;
    halftile = tileSize / 2;
    for reading in wifiData:  ## for every reading
        if macInSingle(mac, reading):  # is MACxx:xx:xx:xx in this reading
            if( abs(xcoor - reading[0]) < halftile):
                if( abs(ycoor - reading[1]) < halftile):
                    wifiSum += getMacStr(mac, reading);
                    samples += 1;
    return(wifiSum, samples)
    
def getOneNeighbors(blockList, index, tolerance): # returns all neighbor indexes
    x1 = blockList[index][0];
    y1 = blockList[index][1];
    neighbors = [];
    for i in range(len(blockList)):
        x2 = blockList[i][0];
        y2 = blockList[i][1];
        if( (x1<=x2) and (y1<=y2) ):  ## check lower limits
            if( (x2 <= x1 + tolerance) and (y2 <= y1 + tolerance) ):
                neighbors.append(i);
    return neighbors

def bigBoy(filename):
    wifiLoc = wifiLocations(filename)
    wifiData = wifiReadings(filename)
    macList = getMacs(wifiData)

    bigList = [];
    for z in range(len(wifiData)):
        bigList.append([])
    return bigList
    

    return(0)
    ##return(wifiLoc, wifiData, macList)

#loc = wifiLocations('wifi.txt')

#wifiToPGM(loc, '3rdFloor.pgm')

#f = open('wifi.txt', 'r')
#lines = f.readlines()
#f.close()


#######################################################
def getBlocks(pgmfileread):
    from matplotlib import pyplot
    ##blocksize = 10 # 10 pixels * 0.050 m/pixel = 0.5m
    resolution = getResolution(pgmfileread)  ## get resolution from .yaml file
    blocksize = int(0.5 / resolution) ## number of pixels = 0.5m / resoultion
    
    ##halfTile = 0.05 * blocksize * 0.5 ##### NOT RIGHT
    ##halfx = 0.5 / 2;
    tileList = []

    pixelThreshold = 0.5 * blocksize * blocksize # 50% of pixels is a full block
    
    image = read_pgm(pgmfileread, byteorder='<')  
    height = len(image)
    width = len(image[0])

    for yblock in range(0, height, blocksize):
        for xblock in range(0, width, blocksize):
            block = image[yblock:yblock+blocksize][:,xblock:xblock+blocksize]
            booleanMat = (block==254)

            if numpy.sum(booleanMat) > pixelThreshold:
                tileList.append([xblock, yblock]) ## this gives a list of tiles with x and y coordinates


    numpyPixel = numpy.array(tileList, float)
    goodList = pixelToWifi(numpyPixel, height, resolution*height)
    
##    before = numpy.array(tileList)
##    after = pixelToWifi(numpyPixel, height, resolution*height)
##    again = wifiToPixel(after, height, resolution*height)
##    return(before, after, again)
    
    
    return(goodList)


##blockList = getBlocks('map2.pgm');
#(before, after, again) = getBlocks('map2.pgm')

######################################################
######################################################

filename = 'rotatedWifi.txt'
pgmfile = 'rotated.pgm'


print('extracting wifi Locations')
wifiLoc = wifiLocations(filename)
print('--done')
print('extracting wifi Mac/Str data')
wifiData = wifiReadings(filename)
print('--done')
print('creating mac list')
macList = getMacs(wifiData)
macList.sort()
print('--done')

print('grabbing blocks from ' + pgmfile)
blockList = getBlocks(pgmfile)
print('--done')

###### NOTE -- Hardcoded value 
tileSize = 0.5 # 1/2 meter per grid

print('generating empty str list for one MAC')
oneMacStr = [];
for i in range(len(blockList)):
    oneMacStr.append([])
print('---done')

emptyOneMacStr = list(oneMacStr)  ## copy this later

npxwifi = wifiLoc[:,0]
npywifi = wifiLoc[:,1]
# maclist is the same
npxmap = blockList[:,0]
npymap = blockList[:,1]

xwifi = []; ywifi = []; xmap = []; ymap =[];
for i in range(len(npxwifi)):
    xwifi.append(npxwifi[i])
    ywifi.append(npywifi[i])

for i in range(len(npxmap)):
    xmap.append(npxmap[i])
    ymap.append(npymap[i])

macMatrix = [];
##dummy = [];
##for i in range(len(macList)):
##    dummy.append([]);

print('making mac address matrix')
for i in range(len(wifiData)): ## for each x/y vertical

    dummy = [];
    for j in range(len(macList)):
        dummy.append([]);
    
    for m in range(len(macList)):  # for each mac address
        if macInSingle(macList[m], wifiData[i]):
            dummy[m] = getMacStr(macList[m], wifiData[i]);
        else:
            dummy[m] = 0;
    macMatrix.append(dummy)
    if(i%200 ==  0):
        print( 'reading ' + str(i) + ' out of ' + str(len(wifiData)))
print('-- done')
    



print('determining adjacentcies')
wifiNeighbors1 = getWifiNeighbors(blockList, wifiLoc, 0.5)
print('--finished order 1')
wifiNeighbors2 = getWifiNeighbors(blockList, wifiLoc, 1.0)
print('--finished order 2')
wifiNeighbors3 = getWifiNeighbors(blockList, wifiLoc, 2.0)
print('--finished order 3')
wifiNeighbors4 = getWifiNeighbors(blockList, wifiLoc, 4.0)
print('--finished order 4')
wifiNeighbors5 = getWifiNeighbors(blockList, wifiLoc, 7.0)
print('--finished order 5')
wifiNeighbors6 = getWifiNeighbors(blockList, wifiLoc, 15.0)
print('--finished order 6')
print('--done')

for macNumber in range(len(macList)):
    eachMac = macList[macNumber];
    
    ###oneMacStr = list(emptyOneMacStr)

    print('filling MAC: ' + eachMac + '        ' + str(macNumber) + ' / ' + str(len(macList)))
    for b in range(len(blockList)):
        if (not macInSingle(eachMac, oneMacStr[b])):  ## only add if not in oneMacStr[] 
            (wifiSum, samples) = fastSumSamples(blockList, b, wifiData, wifiNeighbors1, eachMac)
            if(samples > 0):
                average = wifiSum / samples;
                oneMacStr[b].append([eachMac, average])

    for b in range(len(blockList)):
        if (not macInSingle(eachMac, oneMacStr[b])):  ## only add if not in oneMacStr[] 
            (wifiSum, samples) = fastSumSamples(blockList, b, wifiData, wifiNeighbors2, eachMac)
            if(samples > 0):
                average = wifiSum / samples;
                oneMacStr[b].append([eachMac, average])

    for b in range(len(blockList)):
        if (not macInSingle(eachMac, oneMacStr[b])):  ## only add if not in oneMacStr[] 
            (wifiSum, samples) = fastSumSamples(blockList, b, wifiData, wifiNeighbors3, eachMac)
            if(samples > 0):
                average = wifiSum / samples;
                oneMacStr[b].append([eachMac, average])

    for b in range(len(blockList)):
        if (not macInSingle(eachMac, oneMacStr[b])):  ## only add if not in oneMacStr[] 
            (wifiSum, samples) = fastSumSamples(blockList, b, wifiData, wifiNeighbors4, eachMac)
            if(samples > 0):
                average = wifiSum / samples;
                oneMacStr[b].append([eachMac, average])

    for b in range(len(blockList)):
        if (not macInSingle(eachMac, oneMacStr[b])):  ## only add if not in oneMacStr[] 
            (wifiSum, samples) = fastSumSamples(blockList, b, wifiData, wifiNeighbors5, eachMac)
            if(samples > 0):
                average = wifiSum / samples;
                oneMacStr[b].append([eachMac, average])

    for b in range(len(blockList)):
        if (not macInSingle(eachMac, oneMacStr[b])):  ## only add if not in oneMacStr[] 
            (wifiSum, samples) = fastSumSamples(blockList, b, wifiData, wifiNeighbors6, eachMac)
            if(samples > 0):
                average = wifiSum / samples;
                oneMacStr[b].append([eachMac, average])
                
    ##print('--done')
print('--all MAC filled')

print('saving denseMap')
savename = 'denseMap.txt'
save = open(savename, 'w')
for i in range(len(blockList)):
    line = "x:" + str(blockList[i][0]) + "||y:" + str(blockList[i][1]) + "||z:0.000000"
    for addStr in oneMacStr[i]:
        line = line + '||[MAC: ' + str(addStr[0]) + ' Str ' + str(addStr[1]) + ']'
    save.write(line)
    save.write('\n')
save.close()

           

