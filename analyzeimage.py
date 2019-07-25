import cv2
import numpy as np
from PIL import Image

def analyzeimage(old_image_file):

        old_image = Image.open(old_image_file)

        old_image_arr = np.array(old_image)

        nir_img = np.array[2]

        green_img = np.array[1] - nir_img

        built_up_index = (green_img-2*nir_img)/(green_img+2*nir_img)

        built_up_image = cv2.fromarray(built_up_index)

        cv2.imwrite('static/temp.jpg', built_up_image)
        
	# analyze the image 'old_image' here
	# save the analyzed image to 'static/temp.jpg'
	# return the path of the new image file
	return "static/temp.jpg"
from sklearn import cluster

def ndvi(nir, red):
  nir = nir.astype('f8')
  red = red.astype('f8')
  return ((nir-red)/(nir+red))

def ndwi(nir, green):
  nir = nir.astype('f8')
  green = red.astype('f8')
  return ((green-nir)/(green+nir))

def ndbi(nir, swir):
  nir = nir.astype('f8')
  swir = swir.astype('f8')
  return ((nir-swir)/(nir+swir))

def norm(band):
    band_min, band_max = band.min(), band.max()
    return ((band - band_min)/(band_max - band_min))

with rasterio.open(filepath) as src:
    profile = src.profile
    oviews = src.overviews(1) # list of overviews from biggest to smallest
    oview = 1  # Use second-highest resolution overview
    print('Decimation factor= {}'.format(oview))
    nir = src.read(1, window=window, out_shape=(1, 1000, 1000))

with rasterio.open(filepath2) as src:
    profile = src.profile
    oviews = src.overviews(1) # list of overviews from biggest to smallest
    oview = 1 # Use second-highest resolution overview
    print('Decimation factor= {}'.format(oview))
    red = src.read(1, window=window, out_shape=(1, 1000, 1000))
    
with rasterio.open(filepath3) as src:
    profile = src.profile
    oviews = src.overviews(1) # list of overviews from biggest to smallest
    oview = 1 # Use second-highest resolution overview
    print('Decimation factor= {}'.format(oview))
    green = src.read(1, window=window, out_shape=(1, 1000, 1000))

with rasterio.open(filepath4) as src:
    profile = src.profile
    oviews = src.overviews(1) # list of overviews from biggest to smallest
    oview = 1 # Use second-highest resolution overview
    print('Decimation factor= {}'.format(oview))
    swir = src.read(1, window=window, out_shape=(1, 1000, 1000))

filepath = 'http://landsat-pds.s3.amazonaws.com/c1/L8/013/032/LC08_L1TP_013032_20190713_20190719_01_T1/LC08_L1TP_013032_20190713_20190719_01_T1_B5.TIF'
filepath2 = 'http://landsat-pds.s3.amazonaws.com/c1/L8/013/032/LC08_L1TP_013032_20190713_20190719_01_T1/LC08_L1TP_013032_20190713_20190719_01_T1_B4.TIF'
filepath3 = 'http://landsat-pds.s3.amazonaws.com/c1/L8/013/032/LC08_L1TP_013032_20190713_20190719_01_T1/LC08_L1TP_013032_20190713_20190719_01_T1_B3.TIF'
filepath4 = 'http://landsat-pds.s3.amazonaws.com/c1/L8/013/032/LC08_L1TP_013032_20190713_20190719_01_T1/LC08_L1TP_013032_20190713_20190719_01_T1_B6.TIF'
    
to_delete = set()

NDWI_THRESH = -0.1
NDVI_THRESH = 0.5

ndwi = ndwi(nir, green)

for i in range(1000):
  for j in range(1000):
    if ndwi[i,j] > NDWI_THRESH:
      to_delete.add((i, j))

ndvi = ndvi(nir, red)

for i in range(1000):
  for j in range(1000):
    if ndvi[i,j] > NDVI_THRESH:
      to_delete.add((i, j))

ndvi2 = ndvi.copy()

lstdel = list(to_delete)

for i,j in lstdel:
  ndvi2[i, j] = np.nan

plt.imshow(ndvi2)
#lt.colorbar()

ndbi = ndbi(nir, swir)
plt.imshow(ndbi)

if __name__ == '__main__':
        filepath = ""
        analyze_image(old_image_file)
