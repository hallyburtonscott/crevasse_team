from crevasseTools import  *

#plt.savefig('/Users/scotch/Desktop/CrevasseResearch/test.jpg', dpi=250)

print('---------------------START------------------------')
try:
    path = sys.argv[1]
except:
    path = './'

try:
    dest = sys.argv[2]
except:
    dest = './temp_destination'    

print(pathToRGB(path)[:, :, 0:3])
rgb = pathToRGB(path)
pImg = rgbToBW(rgb, thresh4)
#     #print(map2D([[1,2,3], [4, 5, 6], [7, 8, 9]], lambda el: el+1))
#     #sys.exit([1])
# plt.imshow(pImg)


damage_density = createGridBeta(pImg, 50, 50)
#test = createGrid([[1, 2, 3, 4, 5, 5, 1, 3, 24, 1], [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]], 'rect', [2, 2])
#test = convert(pImg, grid)
fig, ax = plt.subplots(1,2,figsize=(30,15))
ax[0].imshow(pImg)
f = ax[1].imshow(damage_density,cmap='magma_r')
eh = plt.colorbar(f)
eh.ax.set_ylabel(r'% grid cell damaged')

plt.savefig(dest, dpi=250)

