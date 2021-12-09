from tkinter import *
import tkinter.filedialog
from PIL import Image, ImageFilter, ImageTk
import os
import tkinter.messagebox
import tkinter.ttk
sizex=0
sizey=0
quality=100
path=''
output_path=None
output_file=None
root = Tk()
root.geometry()
label_img=None
# 设置窗口标题
root.title('图片格式转换')
def loadimg():
    global path
    global sizex
    global sizey
    path = tkinter.filedialog.askopenfilename()
    lb.config(text=path)
    if path != '':
        try:
            img = Image.open(path)
            sizex=img.size[0]
            sizey=img.size[1]
            x.set(sizex)
            y.set(sizey)
            img=img.resize((180,180),Image.ANTIALIAS)
            global img_origin
            img_origin = ImageTk.PhotoImage(img)
            global label_img
            label_img.configure(image=img_origin)
            label_img.pack()
        except OSError:
            tkinter.messagebox.showerror('错误', '图片格式错误，无法识别')


def convert(path,type='png',x=sizex,y=sizey,):
    x=int(x)
    y=int(y)
    file_path=os.path.dirname(path)
    filename=os.path.basename(path)
    front=filename.split('.')[0]
    def function(img):
        try:
            if (0 in cl_dict):
                img = img.convert('RGB').transpose(Image.FLIP_LEFT_RIGHT)
            if (1 in cl_dict):
                img = img.convert('RGB').transpose(Image.FLIP_TOP_BOTTOM)
            if (2 in cl_dict):
                img = img.convert('RGB').filter(ImageFilter.GaussianBlur)
            if (3 in cl_dict):
                img = img.convert('RGB').filter(ImageFilter.BLUR)
            if (4 in cl_dict):
                img = img.convert('RGB').filter((ImageFilter.EDGE_ENHANCE))
            if (5 in cl_dict):
                img = img.convert('RGB').filter(ImageFilter.FIND_EDGES)
            if (6 in cl_dict):
                img = img.convert('RGB').filter(ImageFilter.EMBOSS)
            if (7 in cl_dict):
                img = img.convert('RGB').filter(ImageFilter.CONTOUR)
            if (8 in cl_dict):
                img = img.convert('RGB').filter(ImageFilter.SHARPEN)
            if (9 in cl_dict):
                img = img.convert('RGB').filter(ImageFilter.SMOOTH)
            if (10 in cl_dict):
                img = img.convert('RGB').filter(ImageFilter.DETAIL)
        except ValueError as e:
            tkinter.messagebox.showerror('错误',repr(e))
        return img
    if path != '':
        try:
            img = Image.open(path)
            img=function(img)
            img = img.resize((x, y), Image.ANTIALIAS)
            img_n = img.resize((180, 180), Image.ANTIALIAS)
            global img_new
            img_new = ImageTk.PhotoImage(img_n)
            label_img2.configure(image=img_new)
            label_img2.pack()
            global  output_path,output_file
            output_path=file_path + '\\' + front + '.' + type
            output_file=img

        except OSError:
            lb.config(text="您没有选择任何文件")
            tkinter.messagebox.showerror('错误', '图片格式错误，无法识别')
    else:
        tkinter.messagebox.showerror('错误', '未发现路径')
        #im.transpose(Image.FLIP_LEFT_RIGHT)水平镜像 or im.transpose(Image.FLIP_TOP_BOTTOM)垂直镜像
#如何获得回调函数的对象呢
def output():
    global output_file,output_path
    output_file.save(output_path,quality=quality)

v=IntVar()
#列表中存储的是元素是元组
types=[('png',0),('jpg',1),('bmp',2),('pdf',3),('jpeg',4)]
type='png'
def callRB():
    for i in range(5):
        if (v.get()==i):
            global type
            type=types[i][0]
lb = Label(root,text = '选取格式后会在原路径生成对应格式')
lb.pack()
btn = Button(root,text="转换图片",command=lambda:convert(path,type,x.get(),y.get()))
btn2 = Button(root,text="选择图片",command=loadimg)
btn3 = Button(root,text="确定",command=output)
btn2.pack()

btn.pack()
btn3.pack()
fm1 = Frame(root)
#for循环创建单选框
for lan,num in types:
    Radiobutton(fm1, text=lan, value=num, command=callRB, variable=v).pack(anchor=W,side='left')
     # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
x=tkinter.StringVar()
y=tkinter.StringVar()
namex='当前x:{}'.format(sizex)
namey='当前y:{}'.format(sizey)
x.set(namex)
y.set(namey)
xEntered = tkinter.ttk.Entry(fm1, width=12, textvariable=x)
xEntered.pack(side='left')
temp_entered = tkinter.Message(fm1,text = '×')
temp_entered.pack(side='left',padx=0.5)
yEntered = tkinter.ttk.Entry(fm1, width=12, textvariable=y)
yEntered.pack(side='left')
fm1.pack(side=TOP, fill=BOTH, expand=YES)
fm2=Frame(root)
lb2 = Label(fm2,text = '警告：如果使用原格式会覆盖原图片',width=27,height=2,font=("Arial", 10),bg="red")
lb2.pack(side='top')
fm2.pack(side=TOP, fill=BOTH, expand=YES)
fm3=Frame(root)
fm3.pack(side=TOP, fill=BOTH, expand=YES)
cl=[IntVar() ,IntVar() ,IntVar() ,IntVar() ,IntVar() ,IntVar() ,IntVar() ,IntVar() ,IntVar() ,IntVar() ,IntVar() ]
cl_dict=[]

def call_checkbutton():
    cl_dict.clear()
    for i in range(11):
        if(cl[i].get()==1):
            cl_dict.append(i)
qualitys=[('max',0),('high',1),('mid',2),('low',3)]
q=IntVar()
def callQU():
    for i in range(4):
        if (q.get()==i):
            if(type!='jpg' and type!='jpeg'):
                tkinter.messagebox.showinfo('提示','压缩图片仅对输出jpg/jpeg有效')
            global quality
            quality=100-25*qualitys[i][1]
fm_definition=Frame(root)
fm_definition.pack(side=TOP,expand=YES)
for lan,num in qualitys:
    Radiobutton(fm_definition, text=lan, value=num, command=callQU, variable=q).pack(anchor=W,side='left')


l=[]
l.append(tkinter.Checkbutton(fm3,text="水平镜像",command=call_checkbutton,variable=cl[0],onvalue = 1, offvalue = 0))
l.append(tkinter.Checkbutton(fm3,text="垂直镜像",command=call_checkbutton,variable=cl[1],onvalue = 1, offvalue = 0))
l.append(tkinter.Checkbutton(fm3,text="高斯模糊",command=call_checkbutton,variable=cl[2],onvalue = 1, offvalue = 0))
l.append(tkinter.Checkbutton(fm3,text="普通模糊",command=call_checkbutton,variable=cl[3],onvalue = 1, offvalue = 0))
l.append(tkinter.Checkbutton(fm3,text="边缘加强",command=call_checkbutton,variable=cl[4],onvalue = 1, offvalue = 0))
l.append(tkinter.Checkbutton(fm3,text="寻找边缘",command=call_checkbutton,variable=cl[5],onvalue = 1, offvalue = 0))
l.append(tkinter.Checkbutton(fm3,text="浮雕",command=call_checkbutton,variable=cl[6],onvalue = 1, offvalue = 0))
l.append(tkinter.Checkbutton(fm3,text="轮廓",command=call_checkbutton,variable=cl[7],onvalue = 1, offvalue = 0))
l.append(tkinter.Checkbutton(fm3,text="锐化",command=call_checkbutton,variable=cl[8],onvalue = 1, offvalue = 0))
l.append(tkinter.Checkbutton(fm3,text="平滑",command=call_checkbutton,variable=cl[9],onvalue = 1, offvalue = 0))
l.append(tkinter.Checkbutton(fm3,text="细节",command=call_checkbutton,variable=cl[10],onvalue = 1, offvalue = 0))

for bt in l:
    bt.pack(side='left',expand=True)


fm_orgin=Frame(root)
fm_new=Frame(root)
fm_orgin.pack(side=LEFT, expand=YES)
fm_new.pack(side=LEFT, fill=BOTH, expand=YES)
label_img = tkinter.Label(fm_orgin, text='原始图片')
label_img.pack()
label_img2 = tkinter.Label(fm_new, text='获得图片')
label_img2.pack()
root.mainloop()

