from skimage import data, io, feature, color, filters, morphology, measure, transform, draw
import numpy as np
import matplotlib.pyplot as plt
import proc
import cv2 as cv
import time
import statistics

cap = cv.VideoCapture(0)




def main():
    start = time.time()
    #for i in range(1, 16):
    #    frame = cv.imread('/home/radziu/Desktop/KCK/projekt/obrazy' + str(i) + '.png')
     #   contours = proc.process(frame)
      #  contour_img(frame, contours)
       # cv.imwrite('/home/radziu/Desktop/KCK/projekt/przerobione/obrazy' + str(i) + '.png', frame)
    for i in range (1,22):
        if i!=11:
            frame = cv.imread('/home/radziu/Desktop/KCK/projekt/plikiDoPrzerobienia/test'+str(i)+'.jpg')
            contours = proc.process(frame)
            choose_winner(contours);
            contour_img(frame, contours)
            cv.imwrite('/home/radziu/Desktop/KCK/projekt/przerobione/test'+str(i)+'.jpg', frame)
            print(time.time() - start)

def contour_img(img, contours):
    for contour in contours:
        minx, maxx, miny, maxy = 1000, -1, 1000, -1
        for i in contour.c:
            if i[1] > maxx: maxx = i[1]
            elif i[1] < minx: minx = i[1]
            if i[0] > maxy: maxy = i[0]
            elif i[0] < miny: miny = i[0]
           # img[int(i[0]),int(i[1])] = np.array([0,255,255])
            #cv.imshow('kontur',img)
           # flag = cv.waitKey(10) & 0xFF
           # if flag == ord('q'):
            #    break
        minx, maxx, miny, maxy = int(minx) - 5, int(maxx) + 5, int(miny) - 5, int(maxy) + 5
        clr = (255, 0, 0)
        if contour.is_o:
            clr = (0,0,255)
        if contour.is_winner:
            clr=(0,255,0)
        cv.rectangle(img, (maxx, maxy), (minx,miny), clr, 2)

def same_shape(contour1,contour2,contour3):
    if (contour1.is_o==contour2.is_o==contour3.is_o):
        return True
    return False
def skos(contour1,contour2,contour3):
     #skos od lewo dol do prawo gora
    tabela=[contour1,contour2,contour3]
   
    tabelax=[contour1.centre[0],contour2.centre[0],contour3.centre[0]]
    tabelay=[contour1.centre[1],contour2.centre[1],contour3.centre[1]]
    tabelax.sort()
    tabelay.sort()
    najmniejszy_x=contour1.centre[0]
    najmniejszy_y=contour1.centre[1]        #to wszystko zeby potem okreslic czy jest jakis X albo O w lewym dolnym albo prawym gornym rogu
    najwiekszy_x=contour1.centre[0]
    najwiekszy_y=contour1.centre[1]
    for i in tabela:
        if i.centre[0] < najmniejszy_x:
            najmniejszy_x=i.centre[0]
        if i.centre[1] < najmniejszy_y:
             najmniejszy_y=i.centre[1]
        if i.centre[0]>najwiekszy_x:
            najwiekszy_x=i.centre[0]
        if i.centre[1]>najwiekszy_y:
            najwiekszy_y=i.centre[1]
    for j in tabela:
        if najmniejszy_x == j.centre[0] and najmniejszy_y == j.centre[1]: #czy jest jakis X albo O co jest w lewym dolnym
            for l in tabela:
                if najwiekszy_x == l.centre[0] and najwiekszy_y == l.centre[1]:
                    if najmniejszy_x + 50 < statistics.median(tabelax) and najmniejszy_y + 50 < statistics.median(tabelay):
                        print(najmniejszy_y,najmniejszy_x,najwiekszy_y,najwiekszy_x)
                        if statistics.median(tabelax) + 50 < najwiekszy_x  and statistics.median(tabelay)+50<najwiekszy_y:
                            print("skos1")
                            return True
        #skos od lewo gora do prawo dol
    for l in tabela:
        if najmniejszy_x == l.centre[0] and najwiekszy_y == l.centre[1]: # jak wyzej tylko lewy gorny
            for j in tabela:
                if najwiekszy_x == j.centre[0] and najmniejszy_y == j.centre[1]:
                    if najmniejszy_x + 50 < statistics.median(tabelax) and statistics.median(tabelax) + 50 < najwiekszy_x:
                        if najmniejszy_y + 50 < statistics.median(tabelay) and statistics.median(tabelay)+50<najwiekszy_y:
                            print("skos2")
                            return True
    return False


def winning_position(contour1,contour2,contour3):
    if  skos(contour1,contour2,contour3): 
        return True
    elif abs(contour1.centre[0]-contour2.centre[0]) < 30 and  abs(contour2.centre[0]-contour3.centre[0]) <30 and abs(contour1.centre[0]-contour3.centre[0]) <30:
        return True
    elif abs(contour1.centre[1]-contour2.centre[1]) < 30 and  abs(contour2.centre[1]-contour3.centre[1]) <30 and abs(contour1.centre[1]-contour3.centre[1]) <30:
        return True
    return False

def choose_winner(contours):
    if len(contours)>=5:
        for first in range( len(contours)):
            for second in range (first+1,len(contours)):
                for third in range(second+1,len(contours)):
                        if same_shape(contours[first],contours[second],contours[third]) and winning_position(contours[first],contours[second],contours[third]):
                            contours[first].is_winner=True
                            contours[second].is_winner=True
                            contours[third].is_winner=True
                            return
                        contours[first].is_winner=False
                        contours[second].is_winner=False
                        contours[third].is_winner=False



main()
