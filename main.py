import threading
import time
import numpy as np
from queue import Queue
import cv2
import proc
import statistics

frames = Queue(1)

class ImageGrabber(threading.Thread):
    def __init__(self, m):
        threading.Thread.__init__(self)
        self.vidcap=cv2.VideoCapture('plikiDoPrzerobienia/videotest5.mp4')
        
        self.m = m
        self.counter = 0

    def run(self):
        global frames, counter
        while self.m.is_alive():
            ret,frame=self.vidcap.read()
            self.counter += 1
            if self.counter == 10: self.counter = 0
            frames.put((frame, self.counter))
            time.sleep(1/60)
        cv2.destroyAllWindows()
        self.vidcap.release()


class Main(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.contours = None
        self.out=cv2.VideoWriter('przerobione/videotest5_output.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (640,480))
        self.i = 1

    def run(self):
        global frames
        while True:
            if not frames.empty():
                self.curr_frame, count=frames.get()
                if count % 5 == 1:
                    self.contours = proc.process(self.curr_frame)
                choose_winner(self.contours)
                contour_img(self.curr_frame, self.contours)
                cv2.imshow('frame1', self.curr_frame)
                self.out.write(self.curr_frame)
                flag =  cv2.waitKey(10) & 0xFF
                if flag == ord('q'):
                    #print(self.i)
                    break
        self.out.release()
               




def contour_img(img, contours):
    for contour in contours:
        #print(type(contour))
        minx, maxx, miny, maxy = 1000, -1, 1000, -1
        for i in contour.c:
            if i[1] > maxx: maxx = i[1]
            elif i[1] < minx: minx = i[1]
            if i[0] > maxy: maxy = i[0]
            elif i[0] < miny: miny = i[0]
            #img[int(i[0]),int(i[1])] = np.array([0,255,255])

        minx, maxx, miny, maxy = int(minx) - 5, int(maxx) + 5, int(miny) - 5, int(maxy) + 5
        if contour.is_winner:
            clr=(0,255,0)
        elif contour.is_o:
            clr = (0,0,255)
        else:
            clr = (255, 0, 0)
        x=cv2.rectangle(img, (maxx, maxy), (minx,miny) , clr, 2)
        #cv2.imshow('frame',x)


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
    najmniejszy_x=tabelax[0]
    najmniejszy_y=tabelay[0]       #to wszystko zeby potem okreslic czy jest jakis X albo O w lewym dolnym albo prawym gornym rogu
    najwiekszy_x=tabelax[2]
    najwiekszy_y=tabelay[2]
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



main = Main()
grabber=ImageGrabber(main)



main.start()
grabber.start()

grabber.join()