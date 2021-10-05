import numpy as np
import matplotlib.pyplot as plt
import sys

def pathToRGB(path):
    """
    INPUT: An image path
    RETURNS: A 2D rgb array, in floating point  if possible.
    """
    return (plt.imread(path)/255)[:, :, 0:3]

def map2D(arr, func):
    """
    INPUT: (2D array, mapping function) 
    RETURNS: 2D array, each element taking the value specificed by the function 
    Hopefully temporary as I think python has capabiility to do this. 
    """
    temp = arr.copy()
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            temp[i][j] = func(arr[i][j])
    return temp
def rgbToBW(rgbArr, thresh): 
    """
    INPUT: (A 2D rgb array, a threshold function that turns a pixel to B or W) 
    RETURNS: (A 2D array of B and W rgb pixels)
    """
    return map2D(rgbArr, thresh)

def rgbToBWAverage(arr, thresh, size):
    temp = arr.copy()
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            sSum = [0, 0, 0]
            num = 0
            for x in range(-int((size-1)/2), int((size-1)/2 + 1)):
                for y in range(-int((size-1)/2), int((size-1)/2 + 1)):
                    if (0 <= x + i < len(arr)) and (0 <= y + j < len(arr[i])):
                        for k in range(0, 3):
                            sSum[k] = sSum[k] + arr[i + x][j + y][k]
                        num = num + 1
            for k in range(0, 3):
                temp[i][j][k] = sSum[k]/num
            temp[i][j] = thresh(temp[i][j])
    return temp
    
def thresh1(pix):
    """
    INPUT: Pixel
    OUTPUT: Pixel with red thresholding
    """
    if (pix[0]<0.55 and pix[1]< 0.55 and pix[2]<0.55) or (pix[2] > 0.39 and pix[2]<0.58) : 
        return [0,0,0]
    else:
        return [1,1,1]

def thresh2(pix):

    if (pix[0]>0.5098 and pix[0]<0.647 and pix[1]<0.647 and pix[1]>0.549 and pix[2]>0.5686 and pix[2]<0.666):
        return [1, 1, 1]
    else:
        return [0, 0, 0] 
def thresh3(pix):
    if (pix[0]>0.4 and pix[0]<0.8 and pix[1]<0.8 and pix[1]>0.4 and pix[2]>0.5):
        return [1, 1, 1]
    else:
        return [0, 0, 0] 

def thresh4(pix):
    lim0 = 0.06
    lim1 = 0.02
    lim2 = 0.05
    mean = (pix[0] + pix[1] + pix[2])/3
    if(-lim0 < pix[0]-mean< lim0 and -lim1 < pix[1] - mean < lim1 and -lim2< pix[2] -mean < lim2 and pix[0]>(2/5)):
        return [1, 1, 1]
    else:
        return [0, 0, 0]

def createGrid(arr, gridtype, gridsize):
    """
    INPUT: (2D array, gridtype {'rect', 'polar'}, [gridx, gridy])
    RETURNS: 2D array of [n, s, w, e] coordinates, where that makes sense based on polar or rect
    NOTES: If the gridsize does not divide the pixel dimensions, this function will add an extra layer of smaller squares. 
            If the coordinates ever go [x, x], then there is 1 layer of pixel
    """
    #Use remainder to divy up grid.
    if(str.__eq__(gridtype, 'rect')):
        lx = len(arr)
        ly = len(arr[0])
        gx = gridsize[0]
        gy = gridsize[1]
        qx = int(len(arr)/gridsize[0])
        qy = int(len(arr[0])/gridsize[1])
        rx = len(arr)-qx*gx
        ry = len(arr[0])-qy*gy

        sx = 0
        sy = 0
        if(rx > 0):
            sx = 1
        if(ry > 0):
            sy = 1
        #create the mask that will end up being the returned array
        msk = np.zeros((gx+sx, gy+sy, 4), int)
        for i in range(gx +sx):
            for j in range(gy + sy):
                if(i == gx):
                    if(j == gy):
                        msk[i][j] = [j*qy, j*qy + ry-1, i*qx, i*qx + rx-1]
                    else:
                        msk[i][j] = [j*qy, (j+1)*qy -1, i*qx, i*qx + rx-1]
                elif(j == gy):
                    msk[i][j] = [j*qy, j*qy + ry-1, i*qx, (i+1)*qx -1]
                else:
                    msk[i][j] = [j*qy, (j+1)*qy -1, (i)*qx, (i+1)*qx - 1]

        return msk
    
def convert(arr, msk):
    copy = np.zeros((len(arr), len(arr[0]), 3))
    for i in range(len(msk)):
        for j in range(len(msk[0])): 
            cell = msk[i][j]
            for pixx in range(cell[2], cell[3]):
                for pixy in range(cell[0], cell[1]):
                    copy[pixx][pixy] = arr[pixx][pixy] 
    return copy  

def convertByMask(arr, msk, func):
    """
    INPUT: (2D array to be operated on, mask to analyze array, function that operates on each cell) 
    RETUNRS: 2D operated-on array
    """
    copy = arr.copy()


def createGridBeta(imgArr, gridx, gridy):
    width= imgArr.shape[0]
    height= imgArr.shape[1]
    gwidth= int(width/gridx)
    gheight=int(height/gridy)
    # print('width: ' + str(width)+"\n"+"gwidth: " + str(gwidth)+"\n"+'height: ' + str(height)+"\n"+'gheight: ' + str(gheight))
    damage_density=np.zeros((gridx,gridy),float)
    for gx in range(gridx):
        for gy in range(gridy):
            numwhite=0
            numblack=0
            for i in range(gx*gwidth, (gx+1)*gwidth):
                for j in range(gy*gheight, (gy+1)*gheight):
                    if(imgArr[i][j][0]==0):
                        numblack=numblack + 1
                    else: 
                        numwhite=numwhite +1 
            damage_density[gx][gy]=numblack/(numwhite+numblack)
    return damage_density         
    

def saveColorImage(imgs):
    fig, ax = plt.subplots(1,2,figsize=(30,15))
    ax[0].imshow(pImg)
    f = ax[1].imshow(damage_density,cmap='magma_r')
    eh = plt.colorbar(f)
    eh.ax.set_ylabel(r'% grid cell damaged')


