import numpy as np
import matplotlib.pyplot as plt
import sys

def pathToRGB(path):
    return (plt.imread(path)/255)[:, :, 0:3]
def procImg(imgArr, colorArr):
    dotPosArr = []
    for i in range(len(imgArr)):
        for j in range(len(imgArr[i])):
            for k in range
