# -*- coding: utf-8 -*-
"""Copy of Copy of Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15ef5xj58IT0bJYizGRz-h6mfzGtAVp0r

### Importing the files:

Run the following code, restart the runtime and re-run the code.

# Project:
"""

from google.colab import drive
drive.mount('/content/drive')

# Necessary imports.
import numpy as np
import cv2
from google.colab.patches import cv2_imshow
import matplotlib.pyplot as plt
from google.colab import drive
from pathlib import Path
from PIL import Image
import os
!pip uninstall imgaug && pip uninstall albumentations && pip install git+https://github.com/aleju/imgaug.git
!sudo apt install tesseract-ocr
!pip install pytesseract
import pytesseract
from pytesseract import image_to_string
import string
if not (os.path.isdir('/content/drive/MyDrive/')):
  drive.mount('/content/drive')
try:
  os.mkdir('/content/drive/MyDrive/Project/Output')
except:
   pass
try:
  os.mkdir('/content/drive/MyDrive/Project/Output/Images_With_Background')
except:
   pass
try:
  os.mkdir('/content/drive/MyDrive/Project/Output/Rotated_Images_With_Background')
except:
   pass
try:
  os.mkdir('/content/drive/MyDrive/Project/Output/Greyscaled_Images')
except:
   pass
try:
  os.mkdir('/content/drive/MyDrive/Project/Output/Thresholding_Images')
except:
   pass
try:
  os.mkdir('/content/drive/MyDrive/Project/Output/Cropped_Images')
except:
   pass
try:
  os.mkdir('/content/drive/MyDrive/Project/Output/Sliced_Images')
except:
   pass

"""### Adding a background:"""

def paste_image(path1,path2):
  large_img = cv2.imread(path1)
  small_img = cv2.imread(path2)
  #small_img = cv2.resize(small_img,(580,370)) #To make them look similar.
  large_img = cv2.resize(large_img,(small_img.shape[1]*2,small_img.shape[0]*2))
  x_offset = round(small_img.shape[1]/2)
  y_offset = round(small_img.shape[0]/2)
  x_end = x_offset + small_img.shape[1]
  y_end = y_offset + small_img.shape[0]
  large_img[y_offset:y_end,x_offset:x_end] = small_img
  large_img = cv2.resize(large_img,(round(large_img.shape[1]/2),round(large_img.shape[0]/2)))
  return large_img
def add_background(background):
  locationinput='/content/drive/MyDrive/Project/Input/Data/'
  locationoutput='/content/drive/MyDrive/Project/Output/Images_With_Background/'
  for f in os.listdir(locationinput):
      foreground=os.path.join(locationinput,f)
      op = paste_image(background,foreground)
      backfile = background[background.find('round/')+6:background.find('.')]
      #cv2_imshow(op)
      cv2.imwrite(locationoutput+backfile+"_"+f, op) 
location='/content/drive/MyDrive/Project/Output/Images_With_Background/'
for f in os.listdir(location):
  os.remove(os.path.join(location,f))
add_background('/content/drive/MyDrive/Project/Input/Background/bedsheet.jpg')
add_background('/content/drive/MyDrive/Project/Input/Background/sky.jpg')

"""###Grey scaling the image:"""

def greyscaleImages():
  locationinput='/content/drive/MyDrive/Project/Input/Data/'
  locationoutput='/content/drive/MyDrive/Project/Output/Greyscaled_Images/'
  for f in os.listdir(locationinput):
    img = Image.open(os.path.join(locationinput,f))
    #cv2_imshow(img)
    img.convert("L").save(locationoutput+'greyscale_'+f)
location='/content/drive/MyDrive/Project/Output/Greyscaled_Images/'
for f in os.listdir(location):
  os.remove(os.path.join(location,f))
greyscaleImages()

"""###Thresholding the image:"""

def thresholdingImages():
  locationinput='/content/drive/MyDrive/Project/Output/Greyscaled_Images/'
  locationoutput='/content/drive/MyDrive/Project/Output/Thresholding_Images/'
  for f in os.listdir(locationinput):
    gray = cv2.imread(os.path.join(locationinput,f))
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    retval, thr = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
    thr = cv2.resize(thr,(1160,740)) #To make them look similar.
    #cv2_imshow(thr)
    cv2.imwrite(locationoutput+'threshold'+"_"+f,thr)
location='/content/drive/MyDrive/Project/Output/Thresholding_Images/'
for f in os.listdir(location):
  os.remove(os.path.join(location,f))
thresholdingImages()

"""###Cropping the image:"""

def croppingImages():
  locationinput='/content/drive/MyDrive/Project/Output/Thresholding_Images/'
  locationoutput='/content/drive/MyDrive/Project/Output/Cropped_Images/'
  for f in os.listdir(locationinput):
    img = cv2.imread(os.path.join(locationinput,f))  
    x=1
    y=round(img.shape[0]*0.235)
    y1=img.shape[0]
    x1=round(0.7*img.shape[1])
    crop_img = img[y:y1, x:x1]
    #cv2_imshow(crop_img)
    cv2.imwrite(locationoutput+'cropped'+"_"+f,crop_img)
location='/content/drive/MyDrive/Project/Output/Cropped_Images/'
for f in os.listdir(location):
  os.remove(os.path.join(location,f))
croppingImages()

"""###Extracting the number and cropping the image further."""

def slicingImages():
  locationinput='/content/drive/MyDrive/Project/Output/Cropped_Images/'
  locationoutput='/content/drive/MyDrive/Project/Output/Sliced_Images/'
  for f in os.listdir(locationinput):
    img = cv2.imread(os.path.join(locationinput,f))
    x_max=img.shape[1]
    y_max=img.shape[0]
    ycut=round(0.1*y_max)
    ii=1
    while ii<y_max-ycut-100:
      crop_img = img[ii:ii+ycut, 1:x_max]
      ii=ii+10
      extract = image_to_string(crop_img)
      op=extract.split('\n')
      ctr=1
      no=''
      for i in extract:
        if i=='0' and ctr<=5:
          i='O'
        if i=='O' and ctr<=10 and ctr>=6:
          i='0'
        if i in string.ascii_uppercase and ctr<=5:
          ctr=ctr+1
          no=no+i
        elif i in '0123456789' and ctr>=6 and ctr<=10:
          ctr=ctr+1
          no=no+i
        elif i in string.ascii_uppercase and ctr==10:
          no=no+i
          if ii>=round(y_max/2):
            yslice=ii
            fin_img = img[1:yslice, 1:round(x_max*0.9)]
          else:
            yslice=ii+ycut
            fin_img = img[yslice:y_max, 1:round(x_max*0.9)]
          #cv2_imshow(fin_img)
          cv2.imwrite(locationoutput+no+"_"+f,fin_img)
          ii=y_max
          break
        else:
          ctr=1
          no=''
location='/content/drive/MyDrive/Project/Output/Sliced_Images/'
for f in os.listdir(location):
  os.remove(os.path.join(location,f))
slicingImages()

"""###Data extraction:"""

import re
def countCaps(st):
  count=0
  for j in st:
    if j in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
      count=count+1
  return count
data=[]
def dataExtraction():
  locationinput='/content/drive/MyDrive/Project/Output/Sliced_Images/'
  for f in os.listdir(locationinput):
    img = cv2.imread(os.path.join(locationinput,f))
    filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img=cv2.filter2D(img,-1,filter)
    extract = image_to_string(img)
    op=extract.split('\n')
    #Date
    ctr=0
    for j in op:
      len=0
      for i in j:
        len=len+1
        if i=='/':
          ctr=0
          ctr=ctr+1 
        elif i in '0123456789' and ctr>=1 and ctr<=4:
          ctr=ctr+1
        else:
          ctr=0
        if ctr==5:
          date=j[0:len]
    #Name
    opn=[]
    for i in op:
      if 'Name' in i:
        pass
      elif 'Birth' in i:
        pass
      elif '/' in i:
        pass
      elif re.findall("[A-Z]", i):
        opn.append(i)
    op=opn
    vals=[]
    for i in op:
      count=0
      for j in i:
        if j in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
          count=count+1
      vals.append(count)
    vals.sort()
    names=[]
    for i in op:
      if 'Name' in i:
        pass
      elif 'Birth' in i:
        pass
      elif '/' in i:
        pass
      elif re.findall("[A-Z]", i) and countCaps(i)>=vals[-2]:
        names.append(i)
    data.append([f[0:10],date]+names)
  print(data)
dataExtraction()

"""###Check:"""

def drawHoughLines(image, lines, output):
    out = image.copy()
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 10000 * (-b))
        y1 = int(y0 + 10000 * (a))
        x2 = int(x0 - 10000 * (-b))
        y2 = int(y0 - 10000 * (a))
        cv2.line(out, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imwrite(output, out)

def cyclic_intersection_pts(pts):
    """
    Sorts 4 points in clockwise direction with the first point been closest to 0,0
    Assumption:
        There are exactly 4 points in the input and
        from a rectangle which is not very distorted
    """
    if pts.shape[0] != 4:
        return None

    # Calculate the center
    center = np.mean(pts, axis=0)

    # Sort the points in clockwise
    cyclic_pts = [
        # Top-left
        pts[np.where(np.logical_and(pts[:, 0] < center[0], pts[:, 1] < center[1]))[0][0], :],
        # Top-right
        pts[np.where(np.logical_and(pts[:, 0] > center[0], pts[:, 1] < center[1]))[0][0], :],
        # Bottom-Right
        pts[np.where(np.logical_and(pts[:, 0] > center[0], pts[:, 1] > center[1]))[0][0], :],
        # Bottom-Left
        pts[np.where(np.logical_and(pts[:, 0] < center[0], pts[:, 1] > center[1]))[0][0], :]
    ]

    return np.array(cyclic_pts)

# Read input
color = cv2.imread('/content/drive/MyDrive/Project/bedsheet_img_6.jpg', cv2.IMREAD_COLOR)
color = cv2.resize(color, (0, 0), fx=0.15, fy=0.15)
# RGB to gray
gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
#cv2.imwrite('output/gray.png', gray)
# cv2.imwrite('output/thresh.png', thresh)
# Edge detection
edges = cv2.Canny(gray, 100, 200, apertureSize=3)
# Save the edge detected image
#cv2.imwrite('output/edges.png', edges)
cv2_imshow(edges)

# Detect lines using hough transform
polar_lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)
drawHoughLines(color, polar_lines, 'output/houghlines.png')
# Detect the intersection points
intersect_pts = lq.hough_lines_intersection(polar_lines, gray.shape)
# Sort the points in cyclic order
intersect_pts = cyclic_intersection_pts(intersect_pts)
# Draw intersection points and save
out = color.copy()
for pts in intersect_pts:
    cv2.rectangle(out, (pts[0] - 1, pts[1] - 1), (pts[0] + 1, pts[1] + 1), (0, 0, 255), 2)
cv2.imwrite('output/intersect_points.png', out)

# Find contours
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Fit a rotated rect
rotatedRect = cv2.minAreaRect(contours[0])
# Get rotated rect dimensions
(x, y), (width, height), angle = rotatedRect
# Get the 4 corners of the rotated rect
rotatedRectPts = cv2.boxPoints(rotatedRect)
rotatedRectPts = np.int0(rotatedRectPts)
# Draw the rotated rect on the image
out = color.copy()
cv2.drawContours(out, [rotatedRectPts], 0, (0, 255, 0), 2)
cv2.imwrite('output/minRect.png', out)


# List the output points in the same order as input
# Top-left, top-right, bottom-right, bottom-left
dstPts = [[0, 0], [width, 0], [width, height], [0, height]]
# Get the transform
m = cv2.getPerspectiveTransform(np.float32(intersect_pts), np.float32(dstPts))
# Transform the image
out = cv2.warpPerspective(color, m, (int(width), int(height)))
# Save the output
cv2.imwrite('output/page.png', out)

"""# Rotating Images"""

n=1
# get the path/directory
folder_dir = '/content/drive/MyDrive/Project/Initial_Images'

# iterate over files in
# that directory
images = Path(folder_dir).glob('*.png')
for image in images:
    colorImage  = Image.open(image)

    # Rotate it by 45 degrees
    rotated     = colorImage.rotate(5, expand = True)

    # Rotate it by 90 degrees
    transposed  = colorImage.transpose(Image.ROTATE_90)

    # Display the Original Image
    colorImage.show()

    # Display the Image rotated by 45 degrees
    rotated.show()
    rotated.save('/content/drive/MyDrive/Project/All_img/rotated'+str(n)+'.png')
    

    # Display the Image rotated by 90 degrees
    transposed.show()
    transposed.save('/content/drive/MyDrive/Project/All_img/updated'+str(n)+'.png')
    n=n+1