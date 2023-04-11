import cv2
import os
import numpy as np
from cv2 import *

#Defining required variables
folderPath=r"test\testImage.png"
threshold = 10
path = 'ImagesQuery' #Dataset
orb = cv2.ORB_create(nfeatures=1000) #Object to detect and describe 1000 features from the image

kernel = np.ones((5, 5), np.uint8) 
ClassNames = []
myList = os.listdir(path) #loading names of all images from dataset to myList

images = []
for cl in myList:
    imgCur = cv2.imread(f"{path}/{cl}", 0)
    images.append(imgCur)
    ClassNames.append(os.path.splitext(cl)[0]) #Appends the name of the class by excluding .jpg/.png
    

#finding the feature description of each image in the dataset
def findDes(images):
    #Finding key points and their descriptors for all the images in the dataset
    desList = []
    for img in images:
        kp, des = orb.detectAndCompute(img, None)
        desList.append(des)
    return desList

#Matching the input image against the images in the dataset
def findID(img, deslist):
    kp2, des2 = orb.detectAndCompute(img, None)
    bf = cv2.BFMatcher() #Brute force feature matching with the metric as distance
    #k=2 meaning 2 closest descriptors are found 
    matchlist = []
    finalvalue = -1
    try:
        #good matches are found between input image and each image in the dataset
        for des in deslist:
            matches = bf.knnMatch(des, des2, k=2)
            good = []
            for m, n in matches:
                
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            matchlist.append(len(good)) #how many good descriptors for each class of currency
    except:
        pass
    if len(matchlist) != 0:
        if max(matchlist) > threshold:
            finalvalue = matchlist.index(max(matchlist))
    #print(matchlist)
    return finalvalue 
        
#getting the contour details of the objects in the image
def get_contours(img,imgOriginal):
    img_blur = cv2.GaussianBlur(img, (7, 7), 1)
    img_edges = cv2.Canny(img_blur, 30, 30)
    img_dialation = cv2.dilate(img_edges, kernel, iterations=1) 
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    for cnt in contours:
        area = cv2.contourArea(cnt) 
        if area > 5000: 
            peri = cv2.arcLength(cnt, True) 
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True) 
            x, y, w, h = cv2.boundingRect(approx) 
            final_img = imgOriginal[y: y + h, x: x + w] 
            return final_img 
        else:
            return img
        
#Main function
def isCurrencyPresent(img2):
    imgOriginal = img2.copy()
    desList = findDes(images)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    final_img = get_contours(img2,imgOriginal) 
    X = findID(final_img, desList)
    if X!=-1:
        # cv2.putText(imgOriginal, ClassNames[X], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3)
        # cv2.imshow("img2", imgOriginal)
        # cv2.waitKey(0)
        return True
    return False

# ans=isCurrencyPresent()
# if(ans):
#     print("Yes, currency detected")
# else:
#     print("Currency not detected")