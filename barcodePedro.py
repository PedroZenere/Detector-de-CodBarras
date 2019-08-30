from __future__ import print_function
from cv2 import *
import numpy as np
import pyzbar.pyzbar as pyzbar


def decode(im) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)
  #print("Entrou")
 
  # Print results
  for obj in decodedObjects:
    print('Type : ', obj.type)
    print('Data : ', obj.data,'\n')
     
  return decodedObjects
 
 
# Display barcode and QR code location  
def display(im, decodedObjects):
 
  # Loop over all decoded objects
  for decodedObject in decodedObjects: 
    points = decodedObject.polygon
 
    # If the points do not form a quad, find convex hull
    if len(points) > 4 : 
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else : 
      hull = points;
     
    # Number of points in the convex hull
    n = len(hull)
 
    # Draw the convext hull
    for j in range(0,n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)
 
  # Display results 
  cv2.imshow("Results", im);
  #cv2.waitKey(0);


def main():
	W_NAME_FRM = 'Frame'
	W_NAME_ROI = 'ROI'
	W_NAME_ORI = 'ORIGINAL'
	
	vidcap = VideoCapture(0)
	success,image = vidcap.read()
	count = 0
	success = True
	while success:
	  success,image = vidcap.read()
	  #print("frame%d" % count)
	  #if (count%100 == 0):
	  ROI_HP = (image.shape[0]/2)+40;
	  ROI_HN = (image.shape[0]/2)-40;
	  ROI_W = image.shape[1]
	  
	  #imshow(W_NAME_ORI, image)
	  
	  aux = (50/255.0)*image
	  aux = np.uint8(aux)
	  imgROI = image[int(ROI_HN):int(ROI_HP), 0:int(ROI_W)].copy()
	  image = aux
	  
	  image[int(ROI_HN):int(ROI_HP), 0:int(ROI_W)] = imgROI
	  imshow(W_NAME_FRM, image)
	  
	  decodedObjects = decode(imgROI)
	  display(imgROI, decodedObjects)
	  #imshow(W_NAME_ROI, imgROI)
	  if cv2.waitKey(10) == 27: # exit if Escape
		  break
	  count += 1


if __name__ == "__main__":
	main()
