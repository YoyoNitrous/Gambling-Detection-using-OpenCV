import cv2
import numpy as np
import time
import os
import Cards
import VideoStream
import DetectingCurrency

IM_WIDTH = 1280
IM_HEIGHT = 720 
FRAME_RATE = 10

font = cv2.FONT_HERSHEY_SIMPLEX

videostream = VideoStream.VideoStream((IM_WIDTH,IM_HEIGHT),FRAME_RATE,2,0).start()
time.sleep(1) 
path = os.path.dirname(os.path.abspath(__file__))
train_ranks = Cards.load_ranks( path + '/Card_Imgs/')
train_suits = Cards.load_suits( path + '/Card_Imgs/')

cam_quit = 0 

while cam_quit == 0:

    image = videostream.read()  
    cardflag=0     
    currency=DetectingCurrency.isCurrencyPresent(image)
    pre_proc = Cards.preprocess_image(image)       
	
    cnts_sort, cnt_is_card = Cards.find_cards(pre_proc)    
    if len(cnts_sort) != 0:

        cards = []
        k = 0

        for i in range(len(cnts_sort)):
            if (cnt_is_card[i] == 1):
                cards.append(Cards.preprocess_card(cnts_sort[i],image))5

                cards[k].best_rank_match,cards[k].best_suit_match,cards[k].rank_diff,cards[k].suit_diff = Cards.match_card(cards[k],train_ranks,train_suits)

                image = Cards.draw_results(image, cards[k])
                k = k + 1
        if (len(cards) != 0):
            cardflag=1
            temp_cnts = []
            for i in range(len(cards)):
                temp_cnts.append(cards[i].contour)
            cv2.drawContours(image,temp_cnts, -1, (255,0,0), 2)
    

    if(cardflag==1 and currency==1):
        print("Gambling Detected")
        cv2.putText(image,"Gambling Detected",(10,26),font,0.7,(255,0,255),2,cv2.LINE_AA)
    else: 
        print("Gambling not detected")
        cv2.putText(image,"Gambling Not Detected",(10,26),font,0.7,(255,0,255),2,cv2.LINE_AA)    

    cv2.imshow("Card Detector",image)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cam_quit = 1
        

cv2.destroyAllWindows()
videostream.stop()

