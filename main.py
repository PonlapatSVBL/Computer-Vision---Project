import os
import cv2
import numpy as np
import tkinter.messagebox
import imutils
from tkinter import *
from tkinter import filedialog
from matplotlib import pyplot as plt

from numpy.lib.npyio import fromregex
#from PIL import Image, ImageTk

new_window1 = ''
new_window2 = ''
new_window3 = ''
new_window4 = ''
new_window5 = ''
new_window6 = ''
new_window7 = ''
new_window8 = ''
new_window9 = ''
new_window10 = ''
val = 0
r_val = 0
g_val = 0
b_val = 0
h_val = 0       # 0-179
s_val = 0       # 0-255
v_val = 0       # 0-255

#________________________________________Event________________________________________#

def clickPosition(event, x, y, flags, param):
    global xMouse, yMouse
    xMouse = x
    yMouse = y

    if event == cv2.EVENT_LBUTTONDOWN:
        func_add_substract_cont()

def clickPosition_masking(event, x, y, flags, param):
    global xMouse, yMouse
    xMouse = x
    yMouse = y

    if event == cv2.EVENT_LBUTTONDOWN:
        func_masking_cont()

#________________________________________Function________________________________________#

def showImage():
    fileOpen = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("JPG File", "*.jpg"), ("PNG file", "*.png"), ("All Files", "*.*")))
    global img
    global edited_img

    img = cv2.imread(fileOpen)
    edited_img = img.copy()
    cv2.imshow("Original", img)

def chooseImage():
    fileOpen = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("JPG File", "*.jpg"), ("PNG file", "*.png"), ("All Files", "*.*")))
    global img2
    img2 = cv2.imread(fileOpen)

def chooseImage_mask():
    fileOpen = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("JPG File", "*.jpg"), ("PNG file", "*.png"), ("All Files", "*.*")))
    global img_mask
    img_mask = cv2.imread(fileOpen)

    func_masking()

def saveImage():
    global edited_img
    fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Image", filetypes=(("JPG File", "*.jpg"), ("PNG file", "*.png"), ("All Files", "*.*")))
    cv2.imwrite(str(fln)+'.jpg', edited_img)
    tkinter.messagebox.showinfo("Image Saved", "Image has been saved to "+os.path.basename(fln)+" successfully.")

def previewImage():
    global edited_img
    cv2.imshow('Edited Image', edited_img)

def undoImage():
    global edited_img
    edited_img = img.copy()

def showHistogram():
    ch = cv2.split(edited_img)
    colors = ("b", "g", "r")

    plt.figure()
    plt.title("Color Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of pixels")

    for (chan, color) in zip(ch, colors):
        hist = cv2.calcHist([chan], [0], None, [256], [0,256])
        plt.plot(hist, color=color)
        plt.xlim([0,256])
    plt.show()

def exitProgram():
    confirm = tkinter.messagebox.askquestion("ยืนยัน", "คุณต้องการปิดโปรแกรมหรือไม่ ?")
    if confirm == "yes":
        root.destroy()

def slideVal(value):
    global val
    val = float(value)

def slide_R(value):
    global r_val
    r_val = int(value)

def slide_G(value):
    global g_val
    g_val = int(value)

def slide_B(value):
    global b_val
    b_val = int(value)

def slide_H(value):
    global h_val
    h_val = int(value)

def slide_S(value):
    global s_val
    s_val = int(value)

def slide_V(value):
    global v_val
    v_val = int(value)

def menu(root):
    menuBar = Menu()
    root.config(menu=menuBar)

    menuItem1 = Menu()
    menuItem1.add_command(label="Open", command=showImage)
    menuItem1.add_command(label="Save As...", command=saveImage)
    menuItem1.add_command(label="Exit", command=exitProgram)

    menuItem2 = Menu()
    menuItem2.add_cascade(label="Box filter", command=window_boxFilter)
    menuItem2.add_cascade(label="Gaussian filter", command=window_gaussianFilter)
    menuItem2.add_cascade(label="Median filter", command=window_medianFilter)
    menuItem2.add_cascade(label="Sharpen", command=window_sharpen)
    menuItem2.add_cascade(label="Edge detection", command=window_edgeDetection)

    menuItem3 = Menu()
    menuItem3.add_cascade(label="Add / Subtract", command=window_add_substract)

    menuItem4 = Menu()
    menuItem4.add_cascade(label="Auto White Balance", command=func_whiteBalance)
    menuItem4.add_cascade(label="RGB", command=window_RGB)
    menuItem4.add_cascade(label="HSV", command=window_HSV)

    menuItem5 = Menu()
    menuItem5.add_cascade(label="Masking", command=chooseImage_mask)

    menuItem6 = Menu()
    menuItem6.add_cascade(label="Show width/height", command=window_dimension)
    menuItem6.add_cascade(label="Show histogram (RGB)", command=showHistogram)

    menuBar.add_cascade(label="File", menu=menuItem1)
    menuBar.add_cascade(label="Filter", menu=menuItem2)
    menuBar.add_cascade(label="Image", menu=menuItem3)
    menuBar.add_cascade(label="Color", menu=menuItem4)
    menuBar.add_cascade(label="Selection", menu=menuItem5)
    menuBar.add_cascade(label="Info", menu=menuItem6)

#________________________________________New Window________________________________________#

def window_pixel():
    global new_window1
    new_window1 = Toplevel(root)
    new_window1.geometry("1120x900+400+50")
    new_window1.title("Pixel Transformation")
    new_window1.resizable(False, False)
    new_window1.config(bg="#292929")

    menu(new_window1)

    global alpha_C, beta_B, salt_prob, pepper_prob, mean, sigma
    alpha_C = DoubleVar()       #Contrast   1.0-3.0
    beta_B = IntVar()           #Brightness 0-100
    salt_prob = IntVar()        #salt n pepper
    pepper_prob = IntVar()      #salt n pepper
    mean = IntVar()             #Gaussian noise
    sigma = IntVar()            #Gaussian noise

    alpha_C.set(1.0)

    wrapper2 = LabelFrame(new_window1, text="Pixel Transformation", font=('TH Sarabun New', 20, 'bold'), bg="#393939", fg="white")
    wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)

    wrapper21 = LabelFrame(wrapper2, text="Gray scale", font=('TH Sarabun New', 15), bg="#393939", fg="white")
    wrapper21.pack(fill="both", expand="yes", padx=10, pady=10)

    wrapper22 = LabelFrame(wrapper2, text="Brightness/Contrast", font=('TH Sarabun New', 15), bg="#393939", fg="white")
    wrapper22.pack(fill="both", expand="yes", padx=10, pady=10)

    wrapper23 = LabelFrame(wrapper2, text="Invert", font=('TH Sarabun New', 15), bg="#393939", fg="white")
    wrapper23.pack(fill="both", expand="yes", padx=10, pady=10)

    wrapper24 = LabelFrame(wrapper2, text="Histogram Equalization", font=('TH Sarabun New', 15), bg="#393939", fg="white")
    wrapper24.pack(fill="both", expand="yes", padx=10, pady=10)

    wrapper25 = LabelFrame(wrapper2, text="Salt and Pepper noise", font=('TH Sarabun New', 15), bg="#393939", fg="white")
    wrapper25.pack(fill="both", expand="yes", padx=10, pady=10)

    wrapper26 = LabelFrame(wrapper2, text="Gaussian noise", font=('TH Sarabun New', 15), bg="#393939", fg="white")
    wrapper26.pack(fill="both", expand="yes", padx=10, pady=10)

    btn21 = Button(wrapper21, text="Gray scale",width=20, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=func_grayscale)
    btn21.pack(side=tkinter.LEFT, padx=20, pady=10)

    lbl21 = Label(wrapper22, text="Brightness", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl21.pack(side=tkinter.LEFT, padx=20, pady=20)

    ent21 = Entry(wrapper22, textvariable=beta_B)
    ent21.pack(side=tkinter.LEFT, padx=5, pady=5)

    lbl22 = Label(wrapper22, text="Contrast", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl22.pack(side=tkinter.LEFT, padx=20, pady=20)

    ent22 = Entry(wrapper22, textvariable=alpha_C)
    ent22.pack(side=tkinter.LEFT, padx=5, pady=5)

    btn22 = Button(wrapper22, text="Apply",width=20, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=func_brightContrast)
    btn22.pack(side=tkinter.LEFT, padx=20, pady=10)

    btn23 = Button(wrapper23, text="Invert",width=20, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=func_invert)
    btn23.pack(side=tkinter.LEFT, padx=20, pady=10)

    btn24 = Button(wrapper24, text="Histogram Equalization (RGB)",width=25, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=func_histogramEqualization)
    btn24.pack(side=tkinter.LEFT, padx=20, pady=10)

    btn24_1 = Button(wrapper24, text="Histogram Equalization (Gray)",width=25, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=func_histogramEqualizationGray)
    btn24_1.pack(side=tkinter.LEFT, padx=20, pady=10)

    lbl23 = Label(wrapper25, text="Salt (%)", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl23.pack(side=tkinter.LEFT, padx=20, pady=20)

    ent23 = Entry(wrapper25, textvariable=salt_prob)
    ent23.pack(side=tkinter.LEFT, padx=5, pady=5)

    lbl24 = Label(wrapper25, text="Pepper (%)", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl24.pack(side=tkinter.LEFT, padx=20, pady=20)

    ent24 = Entry(wrapper25, textvariable=pepper_prob)
    ent24.pack(side=tkinter.LEFT, padx=5, pady=5)

    btn25 = Button(wrapper25, text="Apply",width=20, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=func_snp)
    btn25.pack(side=tkinter.LEFT, padx=20, pady=10)

    lbl24 = Label(wrapper26, text="Mean", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl24.pack(side=tkinter.LEFT, padx=20, pady=20)

    ent24 = Entry(wrapper26, textvariable=mean)
    ent24.pack(side=tkinter.LEFT, padx=5, pady=5)

    lbl25 = Label(wrapper26, text="Sigma", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl25.pack(side=tkinter.LEFT, padx=20, pady=20)

    ent25 = Entry(wrapper26, textvariable=sigma)
    ent25.pack(side=tkinter.LEFT, padx=5, pady=5)

    btn26 = Button(wrapper26, text="Apply",width=20, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=func_gaussianNoise)
    btn26.pack(side=tkinter.LEFT, padx=20, pady=10)

    btn27 = Button(new_window1, text="Close",width=20, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=lambda:new_window1.destroy())
    btn27.pack(side=tkinter.RIGHT, padx=20, pady=10)

    btn28 = Button(new_window1, text="Preview",width=20, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=previewImage)
    btn28.pack(side=tkinter.RIGHT, padx=20, pady=10)

    btn29 = Button(new_window1, text="Undo",width=20, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=undoImage)
    btn29.pack(side=tkinter.RIGHT, padx=20, pady=10)

def window_boxFilter():
    global new_window2, k_boxfilter
    k_boxfilter = IntVar()      #Box Filter

    new_window2 = Toplevel(root)
    new_window2.geometry("300x200+450+150")
    new_window2.title("Box Filter")
    new_window2.resizable(False, False)
    new_window2.config(bg="#292929")

    wrapper3 = LabelFrame(new_window2, text="Box filter", font=('TH Sarabun New', 20, 'bold'), bg="#393939", fg="white")
    wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

    lbl31 = Label(wrapper3, text="Kernel", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl31.pack(side=tkinter.LEFT, padx=20, pady=20)

    ent31 = Entry(wrapper3, textvariable=k_boxfilter)
    ent31.pack(side=tkinter.LEFT, padx=5, pady=5)

    btn31 = Button(new_window2, text="Apply",width=10, font=('TH Sarabun New', 12, 'bold'), bg="#393939", fg="white", command=func_boxFilter)
    btn31.pack(side=tkinter.RIGHT, padx=20, pady=10)

def window_gaussianFilter():
    global new_window3, k_gaussianfilter
    k_gaussianfilter = IntVar() #Gaussian Filter

    new_window3 = Toplevel(root)
    new_window3.geometry("300x200+450+150")
    new_window3.title("Gaussian Filter")
    new_window3.resizable(False, False)
    new_window3.config(bg="#292929")

    wrapper4 = LabelFrame(new_window3, text="Gaussian filter", font=('TH Sarabun New', 20, 'bold'), bg="#393939", fg="white")
    wrapper4.pack(fill="both", expand="yes", padx=20, pady=10)

    lbl41 = Label(wrapper4, text="Kernel", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl41.pack(side=tkinter.LEFT, padx=20, pady=20)

    ent41 = Entry(wrapper4, textvariable=k_gaussianfilter)
    ent41.pack(side=tkinter.LEFT, padx=5, pady=5)

    btn41 = Button(new_window3, text="Apply",width=10, font=('TH Sarabun New', 12, 'bold'), bg="#393939", fg="white", command=func_gaussianFilter)
    btn41.pack(side=tkinter.RIGHT, padx=20, pady=10)

def window_medianFilter():
    global new_window4, k_medianfilter
    k_medianfilter = IntVar()   #Median Filter

    new_window4 = Toplevel(root)
    new_window4.geometry("300x200+450+150")
    new_window4.title("Median Filter")
    new_window4.resizable(False, False)
    new_window4.config(bg="#292929")

    wrapper5 = LabelFrame(new_window4, text="Median filter", font=('TH Sarabun New', 20, 'bold'), bg="#393939", fg="white")
    wrapper5.pack(fill="both", expand="yes", padx=20, pady=10)

    lbl51 = Label(wrapper5, text="Kernel", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl51.pack(side=tkinter.LEFT, padx=20, pady=20)

    ent51 = Entry(wrapper5, textvariable=k_medianfilter)
    ent51.pack(side=tkinter.LEFT, padx=5, pady=5)

    btn51 = Button(new_window4, text="Apply",width=10, font=('TH Sarabun New', 12, 'bold'), bg="#393939", fg="white", command=func_medianFilter)
    btn51.pack(side=tkinter.RIGHT, padx=20, pady=10)

def window_sharpen():
    global new_window5, a0, a1, a2, a3, a4, a5, a6, a7, a8

    a0 = IntVar()
    a0.set(-1)
    a1 = IntVar()
    a1.set(-1)
    a2 = IntVar()
    a2.set(-1)
    a3 = IntVar()
    a3.set(-1)
    a4 = IntVar()
    a4.set(9)
    a5 = IntVar()
    a5.set(-1)
    a6 = IntVar()
    a6.set(-1)
    a7 = IntVar()
    a7.set(-1)
    a8 = IntVar()
    a8.set(-1)

    new_window5 = Toplevel(root)
    new_window5.geometry("300x200+450+150")
    new_window5.title("Sharpen")
    new_window5.resizable(False, False)
    new_window5.config(bg="#292929")

    wrapper6 = LabelFrame(new_window5, text="Sharpen", font=('TH Sarabun New', 20, 'bold'), bg="#393939", fg="white")
    wrapper6.pack(fill="both", expand="yes", padx=20, pady=10)

    wrapper6.grid_columnconfigure(0, weight=1)
    wrapper6.grid_columnconfigure(1, weight=1)
    wrapper6.grid_columnconfigure(2, weight=1)

    wrapper6.grid_rowconfigure(0, weight=1)
    wrapper6.grid_rowconfigure(1, weight=1)
    wrapper6.grid_rowconfigure(2, weight=1)
    wrapper6.grid_rowconfigure(3, weight=1)

    ent61 = Entry(wrapper6, width=5 ,textvariable=a0)
    ent61.grid(row=0, column=0)
    ent62 = Entry(wrapper6, width=5, textvariable=a1)
    ent62.grid(row=0, column=1)
    ent63 = Entry(wrapper6, width=5, textvariable=a2)
    ent63.grid(row=0, column=2)
    ent64 = Entry(wrapper6, width=5, textvariable=a3)
    ent64.grid(row=1, column=0)
    ent65 = Entry(wrapper6, width=5, textvariable=a4)
    ent65.grid(row=1, column=1)
    ent66 = Entry(wrapper6, width=5, textvariable=a5)
    ent66.grid(row=1, column=2)
    ent67 = Entry(wrapper6, width=5, textvariable=a6)
    ent67.grid(row=2, column=0)
    ent68 = Entry(wrapper6, width=5, textvariable=a7)
    ent68.grid(row=2, column=1)
    ent69 = Entry(wrapper6, width=5, textvariable=a8)
    ent69.grid(row=2, column=2)

    btn61 = Button(wrapper6, text="Apply",width=10, font=('TH Sarabun New', 12, 'bold'), bg="#393939", fg="white", command=func_sharpen)
    btn61.grid(row=3, column=0, columnspan=3, padx=20, pady=10)

def window_edgeDetection():
    global new_window6, minval, maxval

    minval = IntVar()
    maxval = IntVar()
    minval.set(100)
    maxval.set(200)

    new_window6 = Toplevel(root)
    new_window6.geometry("300x200+450+150")
    new_window6.title("Edge Detection")
    new_window6.resizable(False, False)
    new_window6.config(bg="#292929")

    wrapper7 = LabelFrame(new_window6, text="Edge Detection", font=('TH Sarabun New', 20, 'bold'), bg="#393939", fg="white")
    wrapper7.pack(fill="both", expand="yes", padx=20, pady=10)

    lbl71 = Label(wrapper7, text="Min value :", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl71.pack(side=tkinter.LEFT, padx=5, pady=10)

    ent71 = Entry(wrapper7,width=5, textvariable=minval)
    ent71.pack(side=tkinter.LEFT, padx=5, pady=5)

    lbl72 = Label(wrapper7, text="Max value :", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl72.pack(side=tkinter.LEFT, padx=5, pady=10)

    ent72 = Entry(wrapper7,width=5, textvariable=maxval)
    ent72.pack(side=tkinter.LEFT, padx=5, pady=5)

    btn71 = Button(new_window6, text="Apply",width=10, font=('TH Sarabun New', 12, 'bold'), bg="#393939", fg="white", command=func_edgeDetection)
    btn71.pack(side=tkinter.RIGHT, padx=20, pady=10)

def window_add_substract():
    global new_window7

    new_window7 = Toplevel(root)
    new_window7.geometry("300x400+450+150")
    new_window7.title("Add / Subtract")
    new_window7.resizable(False, False)
    new_window7.config(bg="#292929")

    wrapper8 = LabelFrame(new_window7, text="Add/Subtract", font=('TH Sarabun New', 20, 'bold'), bg="#393939", fg="white")
    wrapper8.pack(fill="both", expand="yes", padx=20, pady=10)

    lbl81 = Label(wrapper8, text="Transparency (%)", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl81.pack(side=tkinter.LEFT, padx=20)

    vertical = Scale(wrapper8, from_=100, to=-100, font=('TH Sarabun New', 16, 'bold'), bg="#393939", fg="white", command=slideVal)
    vertical.pack(fill="y", expand="yes", pady=15)

    btn81 = Button(new_window7, text="Apply",width=10, font=('TH Sarabun New', 12, 'bold'), bg="#393939", fg="white", command=func_add_substract)
    btn81.pack(side=tkinter.RIGHT, padx=20, pady=10)

    btn82 = Button(new_window7, text="Choose Image",width=15, font=('TH Sarabun New', 12, 'bold'), bg="#393939", fg="white", command=chooseImage)
    btn82.pack(side=tkinter.LEFT, padx=20, pady=10)

def window_RGB():
    global new_window8

    new_window8 = Toplevel(root)
    new_window8.geometry("500x350+450+150")
    new_window8.title("RGB")
    new_window8.resizable(False, False)
    new_window8.config(bg="#292929")

    wrapper9 = LabelFrame(new_window8, text="RGB", font=('TH Sarabun New', 20, 'bold'), bg="#393939", fg="white")
    wrapper9.pack(fill="both", expand="yes", padx=20, pady=10)

    wrapper9.grid_columnconfigure(0, weight=1)
    wrapper9.grid_columnconfigure(1, weight=2)

    lbl91 = Label(wrapper9, text="R", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl91.grid(row=0, column=0, padx=10, pady=10)

    r_slide = Scale(wrapper9, from_=-100, to=100,orient=HORIZONTAL, font=('TH Sarabun New', 16), bg="#393939", fg="white", length=200, command=slide_R)
    r_slide.grid(row=0, column=1, padx=10, pady=10)

    lbl92 = Label(wrapper9, text="G", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl92.grid(row=1, column=0, padx=10, pady=10)

    g_slide = Scale(wrapper9, from_=-100, to=100,orient=HORIZONTAL, font=('TH Sarabun New', 16), bg="#393939", fg="white", length=200, command=slide_G)
    g_slide.grid(row=1, column=1, padx=10, pady=10)

    lbl93 = Label(wrapper9, text="B", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl93.grid(row=2, column=0, padx=10, pady=10)

    b_slide = Scale(wrapper9, from_=-100, to=100,orient=HORIZONTAL, font=('TH Sarabun New', 16), bg="#393939", fg="white", length=200, command=slide_B)
    b_slide.grid(row=2, column=1, padx=10, pady=10)

    btn91 = Button(new_window8, text="Apply",width=10, font=('TH Sarabun New', 12, 'bold'), bg="#393939", fg="white", command=func_rgb)
    btn91.pack(side=tkinter.RIGHT, padx=20, pady=10)

def window_HSV():
    global new_window9

    new_window9 = Toplevel(root)
    new_window9.geometry("500x350+450+150")
    new_window9.title("HSV")
    new_window9.resizable(False, False)
    new_window9.config(bg="#292929")

    wrapper10 = LabelFrame(new_window9, text="HSV", font=('TH Sarabun New', 20, 'bold'), bg="#393939", fg="white")
    wrapper10.pack(fill="both", expand="yes", padx=20, pady=10)

    wrapper10.grid_columnconfigure(0, weight=1)
    wrapper10.grid_columnconfigure(1, weight=2)

    lbl101 = Label(wrapper10, text="H", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl101.grid(row=0, column=0, padx=10, pady=10)

    h_slide = Scale(wrapper10, from_=-100, to=100,orient=HORIZONTAL, font=('TH Sarabun New', 16), bg="#393939", fg="white", length=200, command=slide_H)
    h_slide.grid(row=0, column=1, padx=10, pady=10)

    lbl102 = Label(wrapper10, text="S", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl102.grid(row=1, column=0, padx=10, pady=10)

    s_slide = Scale(wrapper10, from_=-100, to=100,orient=HORIZONTAL, font=('TH Sarabun New', 16), bg="#393939", fg="white", length=200, command=slide_S)
    s_slide.grid(row=1, column=1, padx=10, pady=10)

    lbl103 = Label(wrapper10, text="V", font=('TH Sarabun New', 14), bg="#393939", fg="white")
    lbl103.grid(row=2, column=0, padx=10, pady=10)

    v_slide = Scale(wrapper10, from_=-100, to=100,orient=HORIZONTAL, font=('TH Sarabun New', 16), bg="#393939", fg="white", length=200, command=slide_V)
    v_slide.grid(row=2, column=1, padx=10, pady=10)

    btn101 = Button(new_window9, text="Apply",width=10, font=('TH Sarabun New', 12, 'bold'), bg="#393939", fg="white", command=func_hsv)
    btn101.pack(side=tkinter.RIGHT, padx=20, pady=10)

def window_dimension():
    global new_window10

    new_window10 = Toplevel(root)
    new_window10.geometry("300x200+450+150")
    new_window10.title("Dimension")
    new_window10.resizable(False, False)
    new_window10.config(bg="#292929")

    h,w = edited_img.shape[:2]
    txt = str(w)+'x'+str(h)+' px'

    wrapper11 = LabelFrame(new_window10, text="Dimension", font=('TH Sarabun New', 20, 'bold'), bg="#393939", fg="white")
    wrapper11.pack(fill="both", expand="yes", padx=20, pady=10)

    lbl111 = Label(wrapper11, text=txt, font=('TH Sarabun New', 20), bg="#393939", fg="white")
    lbl111.pack(pady=35)

#________________________________________Function Manage Image________________________________________#

def func_resizeImage():
    global edited_img
    edited_img = cv2.resize(edited_img, (int(w.get()), int(h.get())) )
    cv2.imshow('Resize image', edited_img)

def func_flipVertical():
    global edited_img
    edited_img = cv2.flip(edited_img, 0)
    cv2.imshow('Flip Vertical Image', edited_img)

def func_flipHorizontal():
    global edited_img
    edited_img = cv2.flip(edited_img, 1)
    cv2.imshow('Flip Horizontal Image', edited_img)

def func_rotateCW():
    global edited_img
    edited_img = cv2.rotate(edited_img, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow('Rotated CW Image', edited_img)

def func_rotateCCW():
    global edited_img
    edited_img = cv2.rotate(edited_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imshow('Rotated CCW Image', edited_img)

def func_rotateAngle():
    global edited_img
    #แบบที่ 1 ไม่ตัดขอบภาพ
    edited_img = imutils.rotate_bound(edited_img, angle.get())

    #แบบที่ 2 ตัดขอบภาพที่เกินออก
    #h,w,c = edited_img.shape
    #center = (h//2, w//2)
    #matrix = cv2.getRotationMatrix2D(center, 45, 1.0)
    #edited_img = cv2.warpAffine(edited_img, matrix, (w,h))
    cv2.imshow('Rotate Angle Image', edited_img)

def func_crop():
    global edited_img
    roi = cv2.selectROI(edited_img)
    edited_img = edited_img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    cv2.imshow('Crop Image', edited_img)

def func_grayscale():
    global edited_img
    edited_img = cv2.cvtColor(edited_img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grayscale Image', edited_img)

def func_brightContrast():
    global edited_img
    global alpha_C, beta_B
    edited_img = cv2.convertScaleAbs(edited_img, alpha=alpha_C.get(), beta=beta_B.get())
    cv2.imshow('Brightness/Contrast Image', edited_img)

def func_invert():
    global edited_img
    edited_img = cv2.bitwise_not(edited_img)
    cv2.imshow('Invert Image', edited_img)

def func_histogramEqualization():
    #RGB
    global edited_img
    b,g,r = cv2.split(edited_img)

    hb = cv2.equalizeHist(b)
    hg = cv2.equalizeHist(g)
    hr = cv2.equalizeHist(r)
    
    edited_img = cv2.merge([hb,hg,hr])
    cv2.imshow('Histogram Equalization Image', edited_img)

def func_histogramEqualizationGray():
    global edited_img
    edited_img = cv2.cvtColor(edited_img, cv2.COLOR_BGR2GRAY)
    edited_img = cv2.equalizeHist(edited_img)
    cv2.imshow('Histogram Equalization (Gray) Image', edited_img)

def func_snp():
    global edited_img
    row,col,ch = edited_img.shape
    num_salt = int(np.ceil(salt_prob.get()*row*col/100))
    num_pepper = int(np.ceil(pepper_prob.get()*row*col/100))

    coords = [np.random.randint(0,row,num_salt), np.random.randint(0,col,num_salt)]
    edited_img[coords] = 255

    coords = [np.random.randint(0,row,num_pepper), np.random.randint(0,col,num_pepper)]
    edited_img[coords] = 0
    cv2.imshow('Salt & Pepper noise Image', edited_img)

def func_gaussianNoise():
    global edited_img
    image = edited_img.astype(np.float64)
    row,col,ch = image.shape
    gauss = np.random.normal(mean.get(), sigma.get(), (row,col,ch))
    edited_img = image+gauss
    edited_img = np.clip(edited_img, 0, 255)
    edited_img = edited_img.astype(np.uint8)
    cv2.imshow('Gaussian noise Image', edited_img)

def func_boxFilter():
    global edited_img
    edited_img = cv2.blur(edited_img, (k_boxfilter.get(), k_boxfilter.get()))
    cv2.imshow('Box Filter Image', edited_img)
    new_window2.destroy()

def func_gaussianFilter():
    global edited_img
    edited_img = cv2.GaussianBlur(edited_img, (k_gaussianfilter.get(), k_gaussianfilter.get()), 0)
    cv2.imshow('Gaussian Filter Image', edited_img)
    new_window3.destroy()

def func_medianFilter():
    global edited_img
    edited_img = cv2.medianBlur(edited_img, k_medianfilter.get())
    cv2.imshow('Median Filter Image', edited_img)
    new_window4.destroy()

def func_sharpen():
    global edited_img
    sharpening_filter = np.array([[a0.get(), a1.get(), a2.get()],
                                [a3.get(), a4.get(), a5.get()],
                                [a6.get(), a7.get(), a8.get()]])
    edited_img = cv2.filter2D(edited_img, -1, sharpening_filter)
    cv2.imshow('Sharpen Image', edited_img)
    new_window5.destroy()

def func_edgeDetection():
    global edited_img
    edited_img = cv2.Canny(edited_img, minval.get(), maxval.get())
    cv2.imshow('Edge Detection Image', edited_img)
    new_window6.destroy()

def func_add_substract():
    cv2.imshow('Add/Substract image', edited_img)
    cv2.setMouseCallback('Add/Substract image', clickPosition)
    new_window7.destroy()

def func_add_substract_cont():
    global edited_img, img2, val
    h1,w1 = img.shape[:2]
    h2,w2 = img2.shape[:2]

    if val > 0:
        weight1 = 1-val/100
    else:
        weight1 = 1+val/100

    foreground = np.zeros((h1,w1,3), dtype="uint8")
    #mask = np.zeros((h1,w1), dtype="uint8")

    for y in range(yMouse, h2+yMouse-1):
        if y >= h1:
            continue
        for x in range(xMouse, w2+xMouse-1):
            if x >= w1:
                continue
            else:
                #mask[y][x] = 255
                foreground[y][x] = img2[y-yMouse][x-xMouse]
    img2 = foreground
    edited_img = cv2.addWeighted(edited_img, weight1, img2, val, 0)
    val = 0

    cv2.imshow('Add/Substract image', edited_img)

def func_whiteBalance():
    global edited_img
    b,g,r = cv2.split(edited_img)
    r_avg = cv2.mean(r)[0]
    g_avg = cv2.mean(g)[0]
    b_avg = cv2.mean(b)[0]
 
    k = (r_avg + g_avg + b_avg) / 3
    kr = k / r_avg
    kg = k / g_avg
    kb = k / b_avg

    r = cv2.addWeighted(r, kr, 0, 0, 0)
    g = cv2.addWeighted(g, kg, 0, 0, 0)
    b = cv2.addWeighted(b, kb, 0, 0, 0)

    edited_img = cv2.merge([b, g, r])
    cv2.imshow('White Balance Image', edited_img)

def func_rgb():
    global edited_img, r_val, g_val, b_val

    b,g,r = cv2.split(edited_img)

    r = cv2.addWeighted(r, 1, 0, 0, r_val)
    g = cv2.addWeighted(g, 1, 0, 0, g_val)
    b = cv2.addWeighted(b, 1, 0, 0, b_val)

    edited_img = cv2.merge([b,g,r])
    r_val = 0
    g_val = 0
    b_val = 0

    cv2.imshow('RGB Color', edited_img)
    new_window8.destroy()

def func_hsv():
    global edited_img, h_val, s_val, v_val

    hsv_img = cv2.cvtColor(edited_img, cv2.COLOR_BGR2HSV)
    hsv_img = hsv_img.astype("uint16")

    h,s,v = cv2.split(hsv_img)
    h = cv2.add(h, h_val)
    s = cv2.add(s, s_val)
    v = cv2.add(v, v_val)

    h = np.clip(h, 0, 179)
    s = np.clip(s, 0, 255)
    v = np.clip(v, 0, 255)

    hsv_new_img = cv2.merge([h,s,v])

    hsv_new_img = hsv_new_img.astype("uint8")

    edited_img = cv2.cvtColor(hsv_new_img, cv2.COLOR_HSV2BGR)
    h_val = 0
    s_val = 0
    v_val = 0

    cv2.imshow('HSV Color', edited_img)
    new_window9.destroy()

def func_masking():
    cv2.imshow('Masking', edited_img)
    cv2.setMouseCallback('Masking', clickPosition_masking)

def func_masking_cont():
    global edited_img
    h1,w1 = edited_img.shape[:2]
    h2,w2 = img_mask.shape[:2]

    x_bottom_left = xMouse + w2
    y_bottom_left = yMouse + h2

    if x_bottom_left >= w1:
        x_bottom_left = w1 - 1
    if y_bottom_left >= h1:
        y_bottom_left = h1 - 1

    roi = edited_img[yMouse:y_bottom_left, xMouse:x_bottom_left]

    foreground = img_mask[0:y_bottom_left-yMouse, 0:x_bottom_left-xMouse]

    gray_img = cv2.cvtColor(foreground, cv2.COLOR_RGB2GRAY)
    ret, mask = cv2.threshold(gray_img, 150, 255, cv2.THRESH_BINARY)
    mask_invert = cv2.bitwise_not(mask)
    img_bg = cv2.bitwise_and(roi, roi, mask=mask)
    img_fg = cv2.bitwise_and(foreground, foreground, mask=mask_invert)
    added_img = cv2.add(img_bg, img_fg)

    edited_img[yMouse:y_bottom_left, xMouse:x_bottom_left] = added_img
    cv2.imshow('Masking', edited_img)

#____________________________________________________________Main Program____________________________________________________________#
root = Tk()
root.title("Mini Photoshop")
root.geometry("1120x880+400+50")
root.configure(bg="#292929")

w = StringVar()
h = StringVar()
angle = IntVar()

#สร้างเมนู
menu(root)

#หน้าต่าง user interface
wrapper1 = LabelFrame(root, text="Geometric Transformation", font=('TH Sarabun New', 20, 'bold'), bg="#393939", fg="white")
wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)

wrapper11 = LabelFrame(wrapper1, text="Resize", font=('TH Sarabun New', 15), bg="#393939", fg="white")
wrapper11.pack(fill="both", expand="yes", padx=10, pady=10)

wrapper12 = LabelFrame(wrapper1, text="Flip", font=('TH Sarabun New', 15), bg="#393939", fg="white")
wrapper12.pack(fill="both", expand="yes", padx=10, pady=10)

wrapper13 = LabelFrame(wrapper1, text="Rotate", font=('TH Sarabun New', 15), bg="#393939", fg="white")
wrapper13.pack(fill="both", expand="yes", padx=10, pady=10)

wrapper14 = LabelFrame(wrapper1, text="Crop", font=('TH Sarabun New', 15), bg="#393939", fg="white")
wrapper14.pack(fill="both", expand="yes", padx=10, pady=10)

lbl1 = Label(wrapper11, text="Width", font=('TH Sarabun New', 14), bg="#393939", fg="white")
lbl1.pack(side=tkinter.LEFT, padx=20, pady=20)

ent1 = Entry(wrapper11, textvariable=w)
ent1.pack(side=tkinter.LEFT, padx=5, pady=5)

lbl2 = Label(wrapper11, text="Height", font=('TH Sarabun New', 14), bg="#393939", fg="white")
lbl2.pack(side=tkinter.LEFT, padx=20, pady=20)

ent2 = Entry(wrapper11, textvariable=h)
ent2.pack(side=tkinter.LEFT, padx=5, pady=5)

btn1 = Button(wrapper11, text="Apply",width=15, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=func_resizeImage)
btn1.pack(side=tkinter.LEFT, padx=20, pady=10)

btn2 = Button(wrapper12, text="Flip Vertical",width=15, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=func_flipVertical)
btn2.pack(side=tkinter.LEFT, padx=20, pady=10)

btn3 = Button(wrapper12, text="Flip Horizontal",width=15, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=func_flipHorizontal)
btn3.pack(side=tkinter.LEFT, padx=20, pady=10)

btn4 = Button(wrapper13, text="หมุนตามเข็มนาฬิกา 90°",width=20, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=func_rotateCW)
btn4.pack(side=tkinter.LEFT, padx=20, pady=10)

btn5 = Button(wrapper13, text="หมุนทวนเข็มนาฬิกา 90°",width=20, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=func_rotateCCW)
btn5.pack(side=tkinter.LEFT, padx=20, pady=10)

lbl3 = Label(wrapper13, text="หมุนภาพ", font=('TH Sarabun New', 14), bg="#393939", fg="white")
lbl3.pack(side=tkinter.LEFT, padx=5, pady=5)

ent3 = Entry(wrapper13, textvariable=angle)
ent3.pack(side=tkinter.LEFT, padx=20, pady=10)

btn6 = Button(wrapper13, text="Apply",width=15, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=func_rotateAngle)
btn6.pack(side=tkinter.LEFT, padx=20, pady=10)

btn7 = Button(wrapper14, text="Crop",width=15, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=func_crop)
btn7.pack(side=tkinter.LEFT, padx=20, pady=10)

btn8 = Button(root, text="Pixel Transformation",width=20, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=window_pixel)
btn8.pack(side=tkinter.LEFT, padx=20, pady=10)

btn9 = Button(root, text="Preview",width=20, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=previewImage)
btn9.pack(side=tkinter.RIGHT, padx=20, pady=10)

btn10 = Button(root, text="Undo",width=20, font=('TH Sarabun New', 15, 'bold'), bg="#393939", fg="white", command=undoImage)
btn10.pack(side=tkinter.RIGHT, padx=20, pady=10)

root.mainloop()