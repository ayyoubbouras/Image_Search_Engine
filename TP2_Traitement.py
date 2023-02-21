from tkinter import *
import tkinter as tk  
from tkinter import ttk
from tkinter import filedialog, Text
import os
from ttkthemes import ThemedTk, THEMES
import PIL.Image
import PIL.ImageTk
from resizeimage import resizeimage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import imageio
from skimage import feature
from tkinter import font as tkFont
import searcher,searcherHu
import argparse
import cv2
import time
import Descriptors
from scrollbarImage import ScrollableImage



global var_methode,weightc,weightt,weightf,poid

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def image_title(img,distance):
    black = [0,0,0]     
    constant=cv2.copyMakeBorder(img,3,3,3,3,cv2.BORDER_CONSTANT,value=black )
    blue= np.zeros((30, constant.shape[1], 3), np.uint8)
    blue[:] = (237, 221, 191) 
    vcat = cv2.vconcat((blue, constant))
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(vcat,distance,(75,25), font, 1,(0,0,0), 3, 0)
    return vcat

def affichage_Hu():
    hd = Descriptors.HuMoments()
    query = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
    queryFeatures = hd.hu_moments(query)
    s1 = searcher.SearcherHu("Indexes/indexHuMoments.csv")
    results = s1.search(queryFeatures)
    T=[]
    i,j=0,0
    for (score, resultID) in results:
        src= "dataset/" + resultID
        score=score*10000
        score="{0:.7f}".format(score)
        liste=(src,score)
        T.insert(i,liste)
        if (j%4==0 and j!=0):
            Horizontal=[]
            img0=cv2.imread(T[0][0]) 
            im0=image_title(img0,T[0][1])
            im0 = image_resize(im0,200, 200)

            img1=cv2.imread(T[1][0])
            im1=image_title(img1,T[1][1])
            im1 = image_resize(im1, 200, 200)
            
            img2=cv2.imread(T[2][0])
            im2=image_title(img2,T[2][1])
            im2 = image_resize(im2, 200, 200)

            img3=cv2.imread(T[3][0])
            im3=image_title(img3,T[3][1])
            im3 = image_resize(im3, 200, 200)

            Hori = np.concatenate((im3,im2,im1,im0), axis=1)
            if i==1:
                final=np.concatenate((H,Hori), axis=0)
                H=final
            else:
                H=Hori
            T=[]
            i=1    
        if j==40:
            break
        j=j+1  
    
    top = Toplevel(root)  
    top.title("Resultat")
    imageRGB = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    im = PIL.Image.fromarray(imageRGB)
    im.save("scroll1.png")
    #time.sleep(3)
    img = tk.PhotoImage(file="scroll1.png") 
    image_window = ScrollableImage(top, image=img, scrollbarwidth=15,width=800, height=800)
    image_window.pack()
    top.mainloop()

def affichage_Zernike():
    zr = Descriptors.ZernikeMoments(10)
    query = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
    queryFeatures = zr.describe(query)
    s1 = searcher.Searcher("Indexes/indexzernike.csv")
    results = s1.search(queryFeatures)
    T=[]
    i,j=0,0
    for (score, resultID) in results:
        src= "dataset/" + resultID
        score=score*10
        score="{0:.7f}".format(score)
        liste=(src,score)
        T.insert(i,liste)
        if (j%4==0 and j!=0):
            Horizontal=[]
            img0=cv2.imread(T[0][0]) 
            im0=image_title(img0,T[0][1])
            im0 = cv2.resize(im0, (200, 200))

            img1=cv2.imread(T[1][0])
            im1=image_title(img1,T[1][1])
            im1 = cv2.resize(im1, (200, 200))
            
            img2=cv2.imread(T[2][0])
            im2=image_title(img2,T[2][1])
            im2 = cv2.resize(im2, (200, 200))

            img3=cv2.imread(T[3][0])
            im3=image_title(img3,T[3][1])
            im3 = cv2.resize(im3, (200, 200))

            Hori = np.concatenate((im3,im2,im1,im0), axis=1)
            if i==1:
                final=np.concatenate((H,Hori), axis=0)
                H=final
            else:
                H=Hori
            T=[]
            i=1    
        if j==40:
            break
        j=j+1  
    
    top = Toplevel(root)  
    top.title("Resultat")
    imageRGB = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    im = PIL.Image.fromarray(imageRGB)
    im.save("scroll1.png")
    #time.sleep(3)
    img = tk.PhotoImage(file="scroll1.png") 
    image_window = ScrollableImage(top, image=img, scrollbarwidth=15,width=800, height=800)
    image_window.pack()
    top.mainloop()





def affichage_Matrice_Coccurrence():
    cmd = Descriptors.GLCM()
    query = cv2.imread(filename)
    gray = cv2.cvtColor(query, cv2.COLOR_BGR2GRAY)
    queryFeatures = cmd.extract_features(gray)
    s1 = searcher.Searcher("Indexes/index_cmd.csv")
    results = s1.search(queryFeatures)
    T=[]
    i,j=0,0
    for (score, resultID) in results:
        src= "dataset/" + resultID
        score=score*10000
        score="{0:.7f}".format(score)
        liste=(src,score)
        T.insert(i,liste)
        if (j%4==0 and j!=0):
            Horizontal=[]
            img0=cv2.imread(T[0][0]) 
            im0=image_title(img0,T[0][1])
            im0 = cv2.resize(im0, (200, 200))

            img1=cv2.imread(T[1][0])
            im1=image_title(img1,T[1][1])
            im1 = cv2.resize(im1, (200, 200))
            
            img2=cv2.imread(T[2][0])
            im2=image_title(img2,T[2][1])
            im2 = cv2.resize(im2, (200, 200))

            img3=cv2.imread(T[3][0])
            im3=image_title(img3,T[3][1])
            im3 = cv2.resize(im3, (200, 200))

            Hori = np.concatenate((im3,im2,im1,im0), axis=1)
            if i==1:
                final=np.concatenate((H,Hori), axis=0)
                H=final
            else:
                H=Hori
            T=[]
            i=1
        if j==40:
            break
        j=j+1    

    top = Toplevel(root)  
    top.title("Resultat")
    imageRGB = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    im = PIL.Image.fromarray(imageRGB)
    im.save("scroll1.png")
    #time.sleep(3)
    img = tk.PhotoImage(file="scroll1.png") 
    image_window = ScrollableImage(top, image=img, scrollbarwidth=15,width=800, height=800)
    image_window.pack()
    top.mainloop()
  
def affichage_lbp():
    ld = Descriptors.lbp(1,8)
    query = cv2.imread(filename)
    queryFeatures = ld.lbp_features(query)
    s1 = searcher.Searcher("Indexes/indexlbp.csv")
    results = s1.search(queryFeatures)
    T=[]
    i,j=0,0
    for (score, resultID) in results:
        src= "dataset/" + resultID
        score=score*10000
        score="{0:.7f}".format(score)
        liste=(src,score)
        T.insert(i,liste)
        if (j%4==0 and j!=0):
            Horizontal=[]
            img0=cv2.imread(T[0][0]) 
            im0=image_title(img0,T[0][1])
            im0 = cv2.resize(im0, (200, 200))

            img1=cv2.imread(T[1][0])
            im1=image_title(img1,T[1][1])
            im1 = cv2.resize(im1, (200, 200))
            
            img2=cv2.imread(T[2][0])
            im2=image_title(img2,T[2][1])
            im2 = cv2.resize(im2, (200, 200))

            img3=cv2.imread(T[3][0])
            im3=image_title(img3,T[3][1])
            im3 = cv2.resize(im3, (200, 200))

            Hori = np.concatenate((im3,im2,im1,im0), axis=1)
            if i==1:
                final=np.concatenate((H,Hori), axis=0)
                H=final
            else:
                H=Hori
            T=[]
            i=1    
        if j==40:
            break
        j=j+1    

    top = Toplevel(root)  
    top.title("Resultat")
    imageRGB = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    im = PIL.Image.fromarray(imageRGB)
    im.save("scroll1.png")
    #time.sleep(3)
    img = tk.PhotoImage(file="scroll1.png") 
    image_window = ScrollableImage(top, image=img, scrollbarwidth=15,width=800, height=800)
    image_window.pack()
    top.mainloop()


def affichage_colorHSV():
    cd = Descriptors.ColorDescriptor((8,12,3))
    query = cv2.imread(filename)
    queryFeatures = cd.describe(query)
    s1 = searcher.Searcher("Indexes/indexcolor.csv")
    results = s1.search(queryFeatures)
    T=[]
    i,j=0,0
    for (score, resultID) in results:
        src= "dataset/" + resultID
        score=score*10
        score="{0:.7f}".format(score)
        liste=(src,score)
        T.insert(i,liste)
        if (j%4==0 and j!=0):
            Horizontal=[]
            img0=cv2.imread(T[0][0]) 
            im0=image_title(img0,T[0][1])
            im0 = cv2.resize(im0, (200, 200))

            img1=cv2.imread(T[1][0])
            im1=image_title(img1,T[1][1])
            im1 = cv2.resize(im1, (200, 200))
            
            img2=cv2.imread(T[2][0])
            im2=image_title(img2,T[2][1])
            im2 = cv2.resize(im2, (200, 200))

            img3=cv2.imread(T[3][0])
            im3=image_title(img3,T[3][1])
            im3 = cv2.resize(im3, (200, 200))

            Hori = np.concatenate((im3,im2,im1,im0), axis=1)
            if i==1:
                final=np.concatenate((H,Hori), axis=0)
                H=final
            else:
                H=Hori
            T=[]
            i=1
        if j==40:
            break
        j=j+1    

    top = Toplevel(root)  
    top.title("Resultat")
    imageRGB = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    im = PIL.Image.fromarray(imageRGB)
    im.save("scroll1.png")
    #time.sleep(3)
    img = tk.PhotoImage(file="scroll1.png") 
    image_window = ScrollableImage(top, image=img, scrollbarwidth=15,width=800, height=800)
    image_window.pack()
    top.mainloop()

def affichage_colorRGB():
    cd = Descriptors.ColorDescriptor((8,12,3))
    query = cv2.imread(filename)
    queryFeatures = cd.RGB_hist(query)
    s1 = searcher.Searcher("Indexes/indexRGB.csv")
    results = s1.search(queryFeatures)
    T=[]
    i,j=0,0
    for (score, resultID) in results:
        src= "dataset/" + resultID
        score="{0:.7f}".format(score)
        liste=(src,score)
        T.insert(i,liste)
        if (j%4==0 and j!=0):
            Horizontal=[]
            img0=cv2.imread(T[0][0]) 
            im0=image_title(img0,T[0][1])
            im0 = cv2.resize(im0, (200, 200))

            img1=cv2.imread(T[1][0])
            im1=image_title(img1,T[1][1])
            im1 = cv2.resize(im1, (200, 200))
            
            img2=cv2.imread(T[2][0])
            im2=image_title(img2,T[2][1])
            im2 = cv2.resize(im2, (200, 200))

            img3=cv2.imread(T[3][0])
            im3=image_title(img3,T[3][1])
            im3 = cv2.resize(im3, (200, 200))

            Hori = np.concatenate((im3,im2,im1,im0), axis=1)
            if i==1:
                final=np.concatenate((H,Hori), axis=0)
                H=final
            else:
                H=Hori
            T=[]
            i=1
        if j==40:
            break
        j=j+1    

    top = Toplevel(root)  
    top.title("Resultat")
    imageRGB = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    im = PIL.Image.fromarray(imageRGB)
    im.save("scroll1.png")
    #time.sleep(3)
    img = tk.PhotoImage(file="scroll1.png") 
    image_window = ScrollableImage(top, image=img, scrollbarwidth=15,width=800, height=800)
    image_window.pack()
    top.mainloop()



def affichage_color_texture(w1,w2):
    cd = Descriptors.ColorDescriptor((8,12,3))
    ld = Descriptors.lbp(1,8)
    query = cv2.imread(filename)
    queryFeatures1 = cd.describe(query)
    queryFeatures2= ld.lbp_features(query)
    s1 = searcher.SearcherCombo("Indexes/indexcolor.csv","Indexes/indexlbp.csv",w1,w2)
    results = s1.search(queryFeatures1,queryFeatures2)
    T=[]
    i,j=0,0
    for (score, resultID) in results:
        src= "dataset/" + resultID
        score=score*10000
        score="{0:.7f}".format(score)
        liste=(src,score)
        T.insert(i,liste)
        if (j%4==0 and j!=0):
            Horizontal=[]
            img0=cv2.imread(T[0][0]) 
            im0=image_title(img0,T[0][1])
            im0 = cv2.resize(im0, (200, 200))

            img1=cv2.imread(T[1][0])
            im1=image_title(img1,T[1][1])
            im1 = cv2.resize(im1, (200, 200))
            
            img2=cv2.imread(T[2][0])
            im2=image_title(img2,T[2][1])
            im2 = cv2.resize(im2, (200, 200))

            img3=cv2.imread(T[3][0])
            im3=image_title(img3,T[3][1])
            im3 = cv2.resize(im3, (200, 200))

            Hori = np.concatenate((im3,im2,im1,im0), axis=1)
            if i==1:
                final=np.concatenate((H,Hori), axis=0)
                H=final
            else:
                H=Hori
            T=[]
            i=1
        if j==40:
            break
        j=j+1    

    top = Toplevel(root)  
    top.title("Resultat")
    imageRGB = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    im = PIL.Image.fromarray(imageRGB)
    im.save("scroll1.png")
    #time.sleep(3)
    img = tk.PhotoImage(file="scroll1.png") 
    image_window = ScrollableImage(top, image=img, scrollbarwidth=15,width=800, height=800)
    image_window.pack()
    top.mainloop()

def affichage_forme_texture(w1,w2):
    hd = Descriptors.HuMoments()
    ld = Descriptors.lbp(1,8)
    query = cv2.imread(filename)
    query1 = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
    queryFeatures1 = hd.hu_moments(query1)
    queryFeatures2= ld.lbp_features(query)
    s1 = searcher.SearcherCombo1("Indexes/indexHuMoments.csv","Indexes/indexlbp.csv",w1,w2)
    results = s1.search(queryFeatures1,queryFeatures2)
    T=[]
    i,j=0,0
    for (score, resultID) in results:
        src= "dataset/" + resultID
        score=score*10000
        score="{0:.7f}".format(score)
        liste=(src,score)
        T.insert(i,liste)
        if (j%4==0 and j!=0):
            Horizontal=[]
            img0=cv2.imread(T[0][0]) 
            im0=image_title(img0,T[0][1])
            im0 = cv2.resize(im0, (200, 200))

            img1=cv2.imread(T[1][0])
            im1=image_title(img1,T[1][1])
            im1 = cv2.resize(im1, (200, 200))
            
            img2=cv2.imread(T[2][0])
            im2=image_title(img2,T[2][1])
            im2 = cv2.resize(im2, (200, 200))

            img3=cv2.imread(T[3][0])
            im3=image_title(img3,T[3][1])
            im3 = cv2.resize(im3, (200, 200))

            Hori = np.concatenate((im3,im2,im1,im0), axis=1)
            if i==1:
                final=np.concatenate((H,Hori), axis=0)
                H=final
            else:
                H=Hori
            T=[]
            i=1
        if j==40:
            break
        j=j+1    

    top = Toplevel(root)  
    top.title("Resultat")
    imageRGB = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    im = PIL.Image.fromarray(imageRGB)
    im.save("scroll1.png")
    #time.sleep(3)
    img = tk.PhotoImage(file="scroll1.png") 
    image_window = ScrollableImage(top, image=img, scrollbarwidth=15,width=800, height=800)
    image_window.pack()
    top.mainloop()

def affichage_forme_couleur(w1,w2):
    cd = Descriptors.ColorDescriptor((8,12,3))
    hd = Descriptors.HuMoments()
    query = cv2.imread(filename)
    query1 = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
    queryFeatures1 = hd.hu_moments(query1)
    queryFeatures2= cd.describe(query)
    s1 = searcher.SearcherCombo1("Indexes/indexHuMoments.csv","Indexes/indexcolor.csv",w1,w2)
    results = s1.search(queryFeatures1,queryFeatures2)
    T=[]
    i,j=0,0
    for (score, resultID) in results:
        src= "dataset/" + resultID
        score=score*10000
        score="{0:.7f}".format(score)
        liste=(src,score)
        T.insert(i,liste)
        if (j%4==0 and j!=0):
            Horizontal=[]
            img0=cv2.imread(T[0][0]) 
            im0=image_title(img0,T[0][1])
            im0 = cv2.resize(im0, (200, 200))

            img1=cv2.imread(T[1][0])
            im1=image_title(img1,T[1][1])
            im1 = cv2.resize(im1, (200, 200))
            
            img2=cv2.imread(T[2][0])
            im2=image_title(img2,T[2][1])
            im2 = cv2.resize(im2, (200, 200))

            img3=cv2.imread(T[3][0])
            im3=image_title(img3,T[3][1])
            im3 = cv2.resize(im3, (200, 200))

            Hori = np.concatenate((im3,im2,im1,im0), axis=1)
            if i==1:
                final=np.concatenate((H,Hori), axis=0)
                H=final
            else:
                H=Hori
            T=[]
            i=1
        if j==40:
            break
        j=j+1    

    top = Toplevel(root)  
    top.title("Resultat")
    imageRGB = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    im = PIL.Image.fromarray(imageRGB)
    im.save("scroll1.png")
    #time.sleep(3)
    img = tk.PhotoImage(file="scroll1.png") 
    image_window = ScrollableImage(top, image=img, scrollbarwidth=15,width=800, height=800)
    image_window.pack()
    top.mainloop()

def affichage_trois(w1,w2,w3):
    cd = Descriptors.ColorDescriptor((8,12,3))
    ld = Descriptors.lbp(1,8)
    hd = Descriptors.HuMoments()
    query = cv2.imread(filename)
    query1 = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
    queryFeatures1 = hd.hu_moments(query1)
    queryFeatures2= cd.describe(query)
    queryFeatures3= ld.lbp_features(query)
    s1 = searcher.SearcherComboTrois("Indexes/indexHuMoments.csv","Indexes/indexcolor.csv","Indexes/indexlbp.csv",w1,w2,w3)
    results = s1.search(queryFeatures1,queryFeatures2,queryFeatures3)
    T=[]
    i,j=0,0
    for (score, resultID) in results:
        src= "dataset/" + resultID
        score=score*10000
        score="{0:.7f}".format(score)
        liste=(src,score)
        T.insert(i,liste)
        if (j%4==0 and j!=0):
            Horizontal=[]
            img0=cv2.imread(T[0][0]) 
            im0=image_title(img0,T[0][1])
            im0 = cv2.resize(im0, (200, 200))

            img1=cv2.imread(T[1][0])
            im1=image_title(img1,T[1][1])
            im1 = cv2.resize(im1, (200, 200))
            
            img2=cv2.imread(T[2][0])
            im2=image_title(img2,T[2][1])
            im2 = cv2.resize(im2, (200, 200))

            img3=cv2.imread(T[3][0])
            im3=image_title(img3,T[3][1])
            im3 = cv2.resize(im3, (200, 200))

            Hori = np.concatenate((im3,im2,im1,im0), axis=1)
            if i==1:
                final=np.concatenate((H,Hori), axis=0)
                H=final
            else:
                H=Hori
            T=[]
            i=1
        if j==20:
            break
        j=j+1    

    top = Toplevel(root)  
    top.title("Resultat")
    imageRGB = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    im = PIL.Image.fromarray(imageRGB)
    im.save("scroll1.png")
    #time.sleep(3)
    img = tk.PhotoImage(file="scroll1.png") 
    image_window = ScrollableImage(top, image=img, scrollbarwidth=15,width=800, height=800)
    image_window.pack()
    top.mainloop()


def Matrice_Coccurrence():
    global var_methode,poid
    var_methode="Matrice_Coccurrence"
    widget_list=all_children(root)
    for item in widget_list:
        if (type(item)== ttk.Label or type(item)==ttk.Entry) :
            item.destroy()
    if poid.winfo_exists():
        poid.destroy()
    ttk.Label(FrameMaster, text = "La Recherche En Utilisant Le Descripteur de La Matrice Co-occurrence",).grid(row = 0, column = 1, sticky = W,padx=230, pady = 25)


def couleur_descripteurHSV():
    global var_methode,poid
    var_methode="colorHSV"
    widget_list=all_children(root)
    for item in widget_list:
        if (type(item)==ttk.Label or type(item)==ttk.Entry) :
            item.destroy()
    if poid.winfo_exists():
        poid.destroy()
    ttk.Label(FrameMaster, text = "La Recherche En Utilisant Le Descripteur Couleur HSV").grid(row = 0, column = 1, sticky = W,padx=310, pady = 25)


def couleur_descripteurRGB():
    global var_methode,poid
    var_methode="colorRGB"
    widget_list=all_children(root)
    for item in widget_list:
        if (type(item)== ttk.Label or type(item)==ttk.Entry) :
            item.destroy()
    if poid.winfo_exists():
        poid.destroy()
    ttk.Label(FrameMaster, text = "La Recherche En Utilisant Le Descripteur Couleur RGB").grid(row = 0, column = 1, sticky = W,padx=310, pady = 25)

def LBP():
    global var_methode,poid
    var_methode="lbp"
    widget_list=all_children(root)
    for item in widget_list:
        if (type(item)== ttk.Label or type(item)==ttk.Entry) :
            item.destroy()
    if poid.winfo_exists():
        poid.destroy()        
    ttk.Label(FrameMaster, text = "La Recherche En Utilisant Le Descripteur LBP").grid(row = 0, column = 1, sticky = W,padx=320, pady = 25)

def humoments():
    global var_methode,poid
    var_methode="HuMoments"
    widget_list=all_children(root)
    for item in widget_list:
        if (type(item)== ttk.Label or type(item)==ttk.Entry) :
            item.destroy()
    if poid.winfo_exists():
        poid.destroy()
    ttk.Label(FrameMaster, text = "La Recherche En Utilisant \n Le Descripteur HuMoments").grid(row = 0, column = 0, sticky = W,padx=320, pady = 25)

def zernikemoments():
    global var_methode,poid
    var_methode="ZrMoments"
    widget_list=all_children(root)
    for item in widget_list:
        if (type(item)== ttk.Label or type(item)==ttk.Entry) :
            item.destroy()
    if poid.winfo_exists():
        poid.destroy()
    ttk.Label(FrameMaster, text = "La Recherche En Utilisant \n Le Descripteur Zernike Moments").grid(row = 0, column = 0, sticky = W,padx=320, pady = 25)



def ChoisirImage():
    global filename
    for widget in frameDroit.winfo_children():  
        widget.destroy()
    filename = filedialog.askopenfilename(initialdir="/home/ubuntu/Desktop/master ENSIAS ETUDE/Homework/Traitement des Images",title= "Choisissez Une Image:")
    
    if filename != "":
        with open(filename, 'rb') as file:
            image = PIL.Image.open(file)
            resized_image = resizeimage.resize_cover(image, [500, 500],validate=False)
            resized_image.save('resized_image.png', image.format)
        photo = PIL.ImageTk.PhotoImage(file='resized_image.png')
        Artwork = Label(frameDroit, image=photo)
        Artwork.photo = photo
        Artwork.pack()
    
        
    
def Appliquer():
    if var_methode=="colorHSV":
        affichage_colorHSV() 
    if var_methode=="colorRGB":
        affichage_colorRGB()     
    if var_methode=="lbp":
        affichage_lbp()
    if var_methode=="Matrice_Coccurrence":
        affichage_Matrice_Coccurrence()
    if var_methode=="HuMoments":
        affichage_Hu()
    if var_methode=="color&texture":
        affichage_color_texture(weightc,weightt)
    if var_methode=="forme&couleur":
        affichage_forme_couleur(weightf,weightc)
    if var_methode=="forme&texture":
        affichage_forme_texture(weightf,weightt)
    if var_methode=="trois":
        affichage_trois(weightf,weightc,weightt)    
    else:
        affichage_Zernike()
         
       
            
def all_children(root):
    _list=root.winfo_children()
    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())
    return _list  
global poid
def TextureCouleur():
    global var_methode,weightt,weightc,poid
    weightt,weightc=0.5,0.5
    var_methode="color&texture"
    widget_list=all_children(root)
    for item in widget_list:
        if (type(item)== ttk.Label or type(item)==ttk.Entry) :
            item.destroy() 
    if poid.winfo_exists():
        poid.destroy()
    ttk.Label(FrameMaster, text = "Descripteur Couleur et Texture\n").grid(row = 0, column = 2, sticky = W)
    ttk.Label(FrameMaster, text = "Poids de La Couleur :  ").grid(row = 1 ,sticky = W)
    ttk.Label(FrameMaster, text = "Poids de La Texture : ").grid(row = 2, sticky = W) 
    C=ttk.Entry(FrameMaster)
    C.grid(row = 1, column = 1)
    T=ttk.Entry(FrameMaster)
    T.grid(row = 2, column = 1) 
    def poids():
        global weightt,weightc
        weightc=float(C.get())
        weightt=float(T.get())  
        if (weightt+weightc==1):
            enregistre=ttk.Label(FrameMaster, text = "C'est Enregiste")
            enregistre.grid(row = 4 ,sticky = W) 
            FrameMaster.after(5000, enregistre.destroy)  
        else:
            erreur=ttk.Label(FrameMaster, text = "La somme des poids doit etre = 1")
            erreur.grid(row = 4 ,sticky = W) 
            FrameMaster.after(3000, erreur.destroy)   
    poid = ttk.Button(FrameMaster,text='Enregister les poids',command=poids) 
    poid.grid(row=3,column=0)
    

def TextureForme():
    global var_methode,weightt,weightf,poid
    weightt,weightf=0.5,0.5
    var_methode="forme&texture"
    widget_list=all_children(root)
    for item in widget_list:
        if (type(item)== ttk.Label or type(item)==ttk.Entry) :
            item.destroy() 
    if poid.winfo_exists():
        poid.destroy()
    ttk.Label(FrameMaster, text = "Descripteur Forme et Texture").grid(row = 0, column = 2, sticky = W)
    ttk.Label(FrameMaster, text = "Poids de La Texture :  ").grid(row = 1 ,sticky = W)
    ttk.Label(FrameMaster, text = "Poids de La Forme : ").grid(row = 2, sticky = W) 
    T=ttk.Entry(FrameMaster)
    T.grid(row = 1, column = 1)
    F=ttk.Entry(FrameMaster)
    F.grid(row = 2, column = 1) 
    def poids():
        global weightf,weightc
        weightt=float(T.get())
        weightf=float(F.get())  
        if (weightf+weightt==1):
            enregistre=ttk.Label(FrameMaster, text = "C'est Enregiste")
            enregistre.grid(row = 4 ,sticky = W) 
            FrameMaster.after(5000, enregistre.destroy)  
        else:
            erreur=ttk.Label(FrameMaster, text = "La somme des poids doit etre = 1")
            erreur.grid(row = 4 ,sticky = W) 
            FrameMaster.after(3000, erreur.destroy) 
    poid = ttk.Button(FrameMaster,text='Enregister les poids',command=poids) 
    poid.grid(row=3,column=0)
      

def FormeCouleur():
    global var_methode,weightc,weightf,poid
    weightc,weightf=0.5,0.5
    var_methode="forme&couleur"
    widget_list=all_children(root)
    for item in widget_list:
        if (type(item)== ttk.Label or type(item)==ttk.Entry) :
            item.destroy()
    if poid.winfo_exists():
        poid.destroy() 
    ttk.Label(FrameMaster, text = "Descripteur Forme et Couleur").grid(row = 0, column = 2, sticky = W)
    ttk.Label(FrameMaster, text = "Poids de La Forme :  ").grid(row = 1 ,sticky = W)
    ttk.Label(FrameMaster, text = "Poids de La Couleur : ").grid(row = 2, sticky = W) 
    F=ttk.Entry(FrameMaster)
    F.grid(row = 1, column = 1)
    C=ttk.Entry(FrameMaster)
    C.grid(row = 2, column = 1) 
    def poids():
        global weightf,weightc
        weightf=float(F.get())
        weightc=float(C.get()) 
        if (weightf+weightc==1):
            enregistre=ttk.Label(FrameMaster, text = "C'est Enregiste")
            enregistre.grid(row = 4 ,sticky = W) 
            FrameMaster.after(5000, enregistre.destroy)  
        else:
            erreur=ttk.Label(FrameMaster, text = "La somme des poids doit etre = 1")
            erreur.grid(row =4 ,sticky = W) 
            FrameMaster.after(3000, erreur.destroy) 
    poid = ttk.Button(FrameMaster,text='Enregister les poids',command=poids) 
    poid.grid(row=3,column=0)
       
      
    
def TroisDescripteurs():
    global var_methode,weightc,weightf,weightt,poid
    weightc,weightf,weightt=0.3,0.3,0.4
    var_methode="trois"
    widget_list=all_children(root)
    for item in widget_list:
        if (type(item)== ttk.Label or type(item)==ttk.Entry) :
            item.destroy() 
    if poid.winfo_exists():
        poid.destroy()
    ttk.Label(FrameMaster, text = "La Recherche En Utilisant La combinaison des Trois Descripteurs \n").grid(row = 0, column = 2, sticky = W)
    ttk.Label(FrameMaster, text = "Poids de La Forme :  ").grid(row = 1 ,sticky = W)
    ttk.Label(FrameMaster, text = "Poids de La Couleur : ").grid(row = 2, sticky = W) 
    ttk.Label(FrameMaster, text = "Poids de La Texture : ").grid(row = 3, sticky = W)
    F=ttk.Entry(FrameMaster)
    F.grid(row = 1, column = 1)
    C=ttk.Entry(FrameMaster)
    C.grid(row = 2, column = 1) 
    T=ttk.Entry(FrameMaster)
    T.grid(row = 3, column = 1)
    def poids():
        global weightf,weightc,weightt
        weightf=float(F.get())
        weightc=float(C.get()) 
        weightt=float(T.get())
        if (weightf+weightc+weightt==1):
            enregistre=ttk.Label(FrameMaster, text = "C'est Enregiste")
            enregistre.grid(row = 4 ,sticky = W) 
            FrameMaster.after(5000, enregistre.destroy)  
        else:
            erreur=ttk.Label(FrameMaster, text = "La somme des poids doit etre = 1")
            erreur.grid(row = 4 ,sticky = W) 
            FrameMaster.after(3000, erreur.destroy)
           
    poid = ttk.Button(FrameMaster,text='Enregister les poids',command=poids) 
    poid.grid(row=4,column=0)
        
    

root = ThemedTk(theme='ubuntu')
root.title("IMAGE SEARCH ENGINE")



# Set the theme with the theme_use method


FrameMaster = ttk.Frame(root, height=600, width=1000)  
FrameMaster.pack(expand=YES, fill=BOTH)
FrameMaster.grid_propagate(0)

s = ttk.Style()
s.configure('font1', font=('Helvetica', 14))

poid = ttk.Button(FrameMaster,text='Enregister les poids')
poid.destroy()

frameDroit = ttk.Frame(FrameMaster)
frameDroit.place(relwidth=0.6, relheight=0.8, relx=0.24, rely=0.2)



menubar = Menu(root,tearoff=False,background='#FBFCF8', foreground='black',activebackground='#ED7117', activeforeground='black',font=("Helvetica", 14))

helpmenu = Menu(menubar,tearoff=False,background='#FBFCF8', foreground='black',activebackground='#ED7117', activeforeground='black')

nested_menu1 = Menu(helpmenu,tearoff=False,background='#FBFCF8', foreground='black',activebackground='#ED7117', activeforeground='black')
nested_menu1.add_command(label='Texture & Couleur',command = TextureCouleur,font=("Helvetica", 14))
nested_menu1.add_command(label='Forme & Couleur',font=("Helvetica", 14),command = FormeCouleur)
nested_menu1.add_command(label='Forme & Texture',font=("Helvetica", 14),command = TextureForme)

nested_menu2 = Menu(helpmenu,tearoff=False,background='#FBFCF8', foreground='black',activebackground='#ED7117', activeforeground='black')

menu2_nested = Menu(nested_menu2,tearoff=False,background='#FBFCF8', foreground='black',activebackground='#ED7117', activeforeground='black')
menu2_nested.add_command(label='HuMoments',font=("Helvetica", 14),command = humoments)
menu2_nested.add_command(label='ZernikeMoments',font=("Helvetica", 14),command = zernikemoments)
nested_menu2.add_cascade(label='Forme', menu=menu2_nested,font=("Helvetica", 14))

menu3_nested = Menu(nested_menu2,background='#FBFCF8', foreground='black',activebackground='#ED7117', activeforeground='black',tearoff=False)

menu3_nested.add_command(label='Hist HSV',font=("Helvetica", 14),command = couleur_descripteurHSV)
menu3_nested.add_command(label='Hist RGB',font=("Helvetica", 14),command = couleur_descripteurRGB)
nested_menu2.add_cascade(label='Couleur', menu=menu3_nested,font=("Helvetica", 14))

menu4_nested = Menu(nested_menu2,tearoff=False,background='#FBFCF8', foreground='black',activebackground='#ED7117', activeforeground='black')
menu4_nested.add_command(label='LBP',font=("Helvetica", 14),command = LBP)
menu4_nested.add_command(label='Matrice Co-occurrence',font=("Helvetica", 14),command =Matrice_Coccurrence)
nested_menu2.add_cascade(label='Texture', menu=menu4_nested,font=("Helvetica", 14))

nested_menu3 = Menu(helpmenu,tearoff=False,background='#FBFCF8', foreground='black',activebackground='#ED7117', activeforeground='black')
nested_menu3.add_command(label='les Poids',font=("Helvetica", 14),command =TroisDescripteurs)


helpmenu.add_cascade(label='Deux Descripteurs', menu=nested_menu1,font=("Helvetica", 14))
helpmenu.add_cascade(label='Un Seul Descripteur', menu=nested_menu2,font=("Helvetica", 14))
helpmenu.add_cascade(label='Les Trois Descripteurs', menu=nested_menu3,font=("Helvetica", 14))

menubar.add_cascade(label="Choisir Une Methode De Recherche", menu=helpmenu)
menubar.config( font=("Helvetica", 14))
root.config(menu=menubar)

choisirImg = ttk.Button(root,text='Choisir Une Image',command=ChoisirImage) 
choisirImg.pack(fill=X)

LBPbutton= ttk.Button(root,text='Appliquer',command=Appliquer)  
LBPbutton.pack(fill=X)

root.mainloop()

