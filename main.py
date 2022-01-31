##.............Sketch Imagier............##
##-------------------Required Libraries-------------------------##

from tkinter import *
import cv2
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image,ImageTk

my_font=('Comic Sans MS',40,'bold')       
bt_font=('Calibre',20,'bold')
label_font=('Calibre',15,'italic')
img_title=('Calibre',10,'italic')

##-------------------------------Global variables used in functions as switch------------------##

uploaded=False
exp=False

##--------------------------------Defined Functions--------------------------##

def cartoonf():
    if uploaded==True:
        global panelA, panelB
        numDownSamples = 1
        numBilateralFilters = 50 
        img_color = imag
        for _ in range(numDownSamples): 
            img_color = cv2.pyrDown(img_color) 
        
        for _ in range(numBilateralFilters): 
            img_color = cv2.bilateralFilter(img_color, 9, 9, 7) 
        
        for _ in range(numDownSamples): 
            img_color = cv2.pyrUp(img_color) 
            
        img_gray = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY) 
        img_blur = cv2.medianBlur(img_gray, 3) 
        
        img_edge = cv2.adaptiveThreshold(img_blur, 255,cv2.ADAPTIVE_THRESH_MEAN_C,
                                                   cv2.THRESH_BINARY, 9, 2) 
    
        (x,y,z) = img_color.shape 
        img_edge = cv2.resize(img_edge,(y,x)) 
        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB) 
        converted=cv2.bitwise_and(img_color, img_edge)
        converted=cv2.cvtColor(converted,cv2.COLOR_BGR2RGB)
    
        converted=Image.fromarray(converted)
        
        converted=ImageTk.PhotoImage(converted)
        
        if panelB is None:
            panelB=Label(image_cont,image=converted)
            panelB.image=converted
            panelB.pack(side=RIGHT,pady=10,padx=50)
        else:
            panelB.configure(image=converted)
            panelB.image=converted
    else:
        message()

def sketch_draw():
    if uploaded==True:
        global panelA, panelB
        image=imag
        RGB_img=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        grey_img=cv2.cvtColor(RGB_img, cv2.COLOR_BGR2GRAY)
        invert_img=cv2.bitwise_not(grey_img)
        blur_img=cv2.GaussianBlur(invert_img, (111,111),0) 
        invblur_img=cv2.bitwise_not(blur_img)
        sketch_img=cv2.divide(grey_img,invblur_img, scale=256.0)
        rgb_sketch=cv2.cvtColor(sketch_img, cv2.COLOR_BGR2RGB)
        
        converted=Image.fromarray(rgb_sketch)
        
        converted=ImageTk.PhotoImage(converted)

        if panelB is None:
            panelB=Label(image_cont,image=converted)
            panelB.image=converted
            panelB.pack(side=RIGHT,pady=10,padx=50)
        else:
            panelB.configure(image=converted)
            panelB.image=converted
    else:
        message()

##............................Defined in-app functions....................##       

def upload():
    global imag,panelA,uploaded
    img=filedialog.askopenfilename()
    imag=cv2.imread(img)
    imag=modify(imag)
    image=cv2.cvtColor(imag,cv2.COLOR_BGR2RGB)
    image=Image.fromarray(image)
    image=ImageTk.PhotoImage(image)
    if panelA is None:
        panelA=Label(image_cont,image=image)
        panelA.image=image
        panelA.pack(side=LEFT,pady=10,padx=50)
    else:
        panelA.configure(image=image)
        panelA.image=image
    
    uploaded=True
    return image


def modify(imagi):
    size=imagi.shape
    l=size[0]
    w=size[1]
    if l<500 or w<500:
        if l >= w:
            diff=l/w
            imagi=cv2.resize(imagi,dsize=(int(300/diff),300),interpolation=cv2.INTER_CUBIC)
        else:
            diff=w/l
            imagi=cv2.resize(imagi,dsize=((300,int(300/diff))),interpolation=cv2.INTER_CUBIC)
    else:
        if l >= w:
            diff=l/w
            imagi=cv2.resize(imagi,dsize=(int(500/diff),500),interpolation=cv2.INTER_CUBIC)
        else:
            diff=w/l
            imagi=cv2.resize(imagi,dsize=((500,int(500/diff))),interpolation=cv2.INTER_CUBIC)
    return imagi
    
def message():
    messagebox.showinfo('Upload Image','Please upload the Image first..!!')

##------------------------for exporting/saving the converted image----------------------------##

def export():
    global exp
    exp=True
    return None

##-------------------------------------App Window------------------------------##

root=Tk()
root.title("Sketch Imagier")
root.configure(bg='#3f00a7')
screen_width=str(root.winfo_screenwidth() - 68)
screen_height=str(root.winfo_screenheight()-68)
root.geometry(screen_width+'x'+screen_height)
root.minsize(int(screen_width),int(screen_height))
root.maxsize(int(screen_width),int(screen_height))


##-----------Start-------------------------##

heading=Label(root,text='Sketch',bg='#000',font=my_font,fg='#fff').pack(fill=X,side=TOP,ipady=10,expand=False)     
order=Label(root,text='Please upload your image in jpg/jpeg/png image here:',font=label_font,bg='#3f00a7',fg='white').pack(side=TOP,pady=15,fill=X) 
upload_btn=Button(root, text='Upload',bg='white',font=bt_font,fg='black',activebackground='#bbbbbb',command=lambda:upload()).pack(side=TOP,pady=15)
convert=Label(root,text='Convert to:',bg='#3f00a7',font=label_font,fg='white').pack(side=TOP,pady=10)
 
##-------------Options---------------------##
options=Frame(root,bg='#3f00a7')
sketch=Button(options,text='Sketch',bg='white',fg='black',activebackground='black',activeforeground='white',command=lambda:sketch_draw()).pack(side=LEFT,padx=3)
black_and_white=Button(options,text='B & W',bg='white',fg='black',activebackground='black',activeforeground='white').pack(side=LEFT,padx=3)
cartoon=Button(options,text='Cartoon',bg='white',fg='black',activebackground='black',activeforeground='white',command=lambda:cartoonf()).pack(side=LEFT,padx=3)
word_sketch=Button(options,text='Word Sketch',bg='white',fg='black',activebackground='black',activeforeground='white').pack(side=LEFT,padx=3)
painting=Button(options,text='Painting',bg='white',fg='black',activebackground='black',activeforeground='white').pack(side=LEFT,padx=3)
options.pack(side=TOP,ipady=5,ipadx=5)

divider=Canvas(root,width=int(screen_width)-100,height=1).pack(side=TOP)

##---------------Image Section-------------##

original_title=Label(root,text='Your Original Image:',font=img_title,bg='#3f00a7',fg='white')
converted_title=Label(root,text='Your Converted Image:',font=img_title,bg='#3f00a7',fg='white')

image_cont=Frame(root,bg='#3f00a7')
panelA=None   
panelB=None
image_cont.pack(side=TOP)

export=Button(root, text='Export',bg='white',font=bt_font,fg='black',activebackground='#bbbbbb',command=lambda:export()).pack(side=BOTTOM,pady=5)

root.mainloop()
