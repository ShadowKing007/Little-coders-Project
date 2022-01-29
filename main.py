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
    global panelA, panelB
    k=12
    img=imag
    data=np.float32(img).reshape((-1,3))
    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,20,0.001)

    ret,label,center = cv2.kmeans(data,k,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    center=np.uint8(center)
    result=center[label.flatten()]
    result=result.reshape(img.shape)

    edged=Image.fromarray(result)
    
    edged=ImageTk.PhotoImage(edged)
    
    if panelB is None:
        panelB=Label(image=edged)
        panelB.image=edged
        panelB.place(x=600,y=330)
    else:
        panelB.configure(image=edged)
        panelB.image=edged

def w_sketch():
    if uploaded==True:
        global panelA, panelB
        image=imag
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        edged=cv2.Canny(gray,50,100)
        
        edged=Image.fromarray(edged)
        
        edged=ImageTk.PhotoImage(edged)

        if panelB is None:
            panelB=Label(image=edged)
            panelB.image=edged
            panelB.pack(side=RIGHT,pady=10,padx=50)
        else:
            panelB.configure(image=edged)
            panelB.image=edged
    else:
        message()

##............................Defined in-app functions....................##       

def upload():
    global imag,panelA,uploaded
    img=filedialog.askopenfilename()
    imag=cv2.imread(img)
    imag=cv_modify(imag)
    image=cv2.cvtColor(imag,cv2.COLOR_BGR2RGB)
    image=Image.fromarray(image)
    image=ImageTk.PhotoImage(image)
    if panelA is None:
        panelA=Label(image=image)
        panelA.image=image
        #original_title.pack(side=TOP,pady=5)
        panelA.pack(side=LEFT,pady=10,padx=50)
    else:
        panelA.configure(image=image)
        panelA.image=image
    
    uploaded=True
    return image


def cv_modify(imagi):
    size=imagi.shape
    l=size[0]
    w=size[1]
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
print(screen_height,screen_width)
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
sketch=Button(options,text='Sketch',bg='white',fg='black',activebackground='black',activeforeground='white',command=lambda:w_sketch()).pack(side=LEFT,padx=3)
black_and_white=Button(options,text='B & W',bg='white',fg='black',activebackground='black',activeforeground='white').pack(side=LEFT,padx=3)
cartoon=Button(options,text='Cartoon',bg='white',fg='black',activebackground='black',activeforeground='white',command=lambda:cartoonf()).pack(side=LEFT,padx=3)
word_sketch=Button(options,text='Word Sketch',bg='white',fg='black',activebackground='black',activeforeground='white').pack(side=LEFT,padx=3)
painting=Button(options,text='Painting',bg='white',fg='black',activebackground='black',activeforeground='white').pack(side=LEFT,padx=3)
options.pack(side=TOP,ipady=5,ipadx=5)

divider=Canvas(root,width=int(screen_width)-100,height=1).pack(side=TOP)

##---------------Image Section-------------##

original_title=Label(root,text='Your Original Image:',font=img_title,bg='#3f00a7',fg='white')
converted_title=Label(root,text='Your Converted Image:',font=img_title,bg='#3f00a7',fg='white')
panelA=None   
panelB=None

export=Button(root, text='Export',bg='white',font=bt_font,fg='black',activebackground='#bbbbbb',command=lambda:export()).pack(side=BOTTOM,pady=5)

root.mainloop()