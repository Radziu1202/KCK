from skimage import data, io, feature, color, filters, morphology, measure, transform, draw
import statistics
import numpy as np
import cv2
class Contour:
    def __init__(self, contour):
        self.c = contour
        self.is_o = None
        self.centre = None
        self.is_winner=False
        self.length = len(contour)


def process(img):
    s = np.uint8(color.rgb2gray(img)*255)
   # print(type(s))        
    
    #s = filters.gaussian(s, 0.7)

   
    #\s_cut = s[:, 79:559]
   # print(s)
    #thresh = filters.threshold_local(s, 85,offset=5)
    #print(thresh)
    #s = s > thresh
    #s= morphology.erosion(s);

 




    s = filters.gaussian(s, 0.1)

    # obciecie zdjecia by skupic sie na planszy i znalezc dokladniej threshold
    

    s_cut = s[:, 79:559]
    thresh = filters.threshold_yen(s_cut)
    s = s > thresh
    #print(thresh)

    # znajdz kontury
    
    contours = [Contour(c) for c in measure.find_contours(s, thresh)]
    #odsiej za małe kontury(szum)
    contours = [contour for contour in
        contours if contour.length > 100 ]


    if len(contours) > 0:
        #znajdz wspolrzedne planszy
        #minx,maxx, miny, maxy
        contours.sort(key=lambda c: c.length)   
        plansza = find_board(contours)

        #znajdź źrodki konturów
        
        for contour in contours:
            contour.centre = find_centre(contour.c)
        #usuń kontury znajdujące się poza planszą
        contours = delete_outside_contours(contours, plansza)
        if len(contours) > 0:
            #usuń za duże(np. plansza) i za małe(szum) kontury
            median = statistics.median([c.length for c in contours])
            contours = [contour for contour in contours if 0.3 * median < contour.length <  1.9*  median]
       
            if len(contours) > 0:
                
                    #sprawdz czy kontur jest kółkiem czy krzyżykiem
                for contour in contours:
                    contour.is_o = is_circle(contour.centre, s)
                    #    print(contour.centre)

                    #usuń wewnętrzne strony kółek
                contours = delete_double_circles(contours)
                contours=delete_srodek(contours)
    return contours



def find_board(contours):
    c = contours[-1].c
    minx, maxx, miny, maxy = 1000, -1, 1000, -1
    for i in c:
        if i[1] > maxx:
            maxx = i[1]
        elif i[1] < minx:
            minx = i[1]
        if i[0] > maxy:
            maxy = i[0]
        elif i[0] < miny:
            miny = i[0]
    return [minx, maxx, miny, maxy]

def delete_srodek(contours):
    for index in range(len(contours)):
        for index2 in range(index+1,len(contours)):
                if contours[index]!=None and contours[index2]!=None and  abs(contours[index].centre[0] - contours[index2].centre[0])<30 and abs(contours[index].centre[1] - contours[index2].centre[1]) <30:
                    if contours[index].length > contours[index2].length:
                        contours[index]=None
                    else:
                        contours[index2]=None
    return [contour for contour in contours if contour is not None]

def in_rectangle(rect, point):
    y, x = point
    minx, maxx, miny, maxy = rect
    return  minx < x and x < maxx and miny < y and y < maxy


def find_centre(c):
    moments = measure.moments_coords(c)
    m0 = int(moments[1, 0] / moments[0, 0])
    m1 = int(moments[0, 1] / moments[0, 0])
    return (m0, m1)


def delete_outside_contours(contours, plansza):
    for i in range(len(contours)):
        if not in_rectangle(plansza, contours[i].centre):
            #contours.pop(i)
            contours[i] = None
    return [contour for contour in contours if contour is not None]


def is_circle(centre, gray):
    r = 2
    m0, m1 = centre
    for i in range(m0 - r, m0+r+1):
        for j in range(m1 - r, m1 + r + 1):
            if gray[i, j] == 0:
                return False
    return True


def delete_double_circles(contours):
    for i in range(len(contours)):
        if contours[i] is not None and contours[i].is_o:
            r = contours[i].length/21
            for j in range(i+1, len(contours)):
                if contours[j] is not None and contours[j].is_o:
                    x1, y1 = contours[i].centre
                    x2, y2 = contours[j].centre
                    if ((x1-x2)**2 + (y1 - y2)**2)**0.5 <= r:
                        small = j
                        if contours[i].length < contours[j].length:
                            small = i
                        contours[small] = None
                        break
    return [contour for contour in contours if contour is not None]