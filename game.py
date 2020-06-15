import numpy as np
import imageio
import tkinter as tk
import os
import glob as glob
from scipy.linalg import svd
from PIL import Image, ImageTk

def Remove_zeros(matr):
	eps = 10**-12
	# TODO add a loop that removes zeros from matrix
	return matr

# @do_QR_GS:
# return(s)
def do_QR_GS(matr):
	m,n = np.shape(matr)
	loc_matr = np.array(matr)
	Q =  np.zeros((m, m))
	R =  np.zeros((n, n))
	for j in range(n):
		v = loc_matr[:,j]
		for i in range(j):
			R[i,j] =  np.dot(Q[:,i].T , loc_matr[:,j])
			v = v.squeeze() - (R[i,j] * Q[:,i])
		R[j,j] =  np.linalg.norm(v)
		Q[:,j] = (v / R[j,j]).squeeze()
	return Q, R

def blockSvdPM(matr,s,pr):
	rowsize = len(matr[0])
	vv  = np.zeros((rowsize,s))
	iterations = 0
	for i in range(rowsize):
		for j in range(s):
			if i == j or i > rowsize or j > rowsize:
				vv[i][j] = 1


	while True:
		Q,R = do_QR_GS(np.dot(matr,vv))
		U = np.transpose(Q[0:s])
		Q,R = do_QR_GS(np.dot(np.transpose(matr), U))
		vv = np.transpose(Q[0:s])
		sigma = R[:s,:s]
		err = np.linalg.norm(np.subtract(np.dot(matr,vv),np.dot(U,sigma)))
		iterations = iterations +1
		if (err <= pr) or iterations > 10000:
			return U,sigma,vv




RED = 0
GREEN = 1
BLUE = 2 
def compose_png(red,green,blue):
    rgb = []
    for i in range(len(red)):
        rgb.append([])
        for j in range(len(red[0])):
            rgb[i].append([red[i][j],green[i][j],blue[i][j]])
    return rgb

def split_channel(arr,channnel):
    ret = []
    count = 0 
    for col in arr:
        ret.append([])
        for p in col:
            ret[count].append(p[channnel])
        count+=1
    return ret

def decompose_recompose(ch,treshhold):
    U_ch,S_ch,VT_ch = svd(ch)
    l_sigma = np.zeros((len(ch), len(ch[0])))
    
    for p in range(len(S_ch)):
        if S_ch[p] == 0:
            print ("threshold->",p)
            break

    if treshhold!=-1:
        for i in range(treshhold,len(S_ch)):
            S_ch[i] = 0
    
    for p in range(len(S_ch)):
        l_sigma[p][p] = S_ch[p] 

    ret_ch = U_ch.dot(l_sigma.dot(VT_ch))
    return ret_ch

def make_svd(name,coef,folder):
	im = imageio.imread(name)
	red = split_channel(im,RED) 
	green = split_channel(im,GREEN)
	blue = split_channel(im,BLUE)
	red_w = decompose_recompose(red,coef) 
	green_w = decompose_recompose(green,coef)
	blue_w = decompose_recompose(blue,coef)

	imageio.imwrite("./.tmp{}/".format(folder)+name,compose_png(red_w,green_w,blue_w))

def get_path(path,hard):
	ret = path.split('/')
	return "./.tmp{}/".format(hard)+ ret[len(ret)-1]

def generate_images():
	name_wild = "png"
	path = './'
	files = []
	for r, d, f in os.walk(path):
		for file in f:
			if name_wild in file:
				files.append(path+file)
	for i in files:
		print(i)
		make_svd(i,15,0)
		make_svd(i,12,1)
		make_svd(i,9,2)
		make_svd(i,6,3)
		make_svd(i,3,4)
	return

def dip_Image(where,image):
	img_label = tk.Label(where)
	img_label.image = tk.PhotoImage(file=image)
	img_label['image'] = img_label.image
	img_label.pack()


class App:
 
	def __init__(self, root, image_list):
		self.root = root
		self.difficulty = tk.StringVar()
		print("init")
		self.root.bind("<space>", lambda x: self.hide())
		self.image_list = image_list
		self.image_index = 0
		self.hard = 0
		self.score = 0
		self.hidden = 0
		self.qiestion = 0
		self.menu(True)
		self.test(False,self.image_list[0])
		self.test_solved(False,self.image_list[self.qiestion][0][0])
		self.fin(False,0)
		self.ans = 0
 
	def menu(self,vis):
		self.frame1 = tk.Frame(self.root,width=600, height=400)
		self.frame1.pack( fill=tk.BOTH, expand=1)
		tk.Label(self.frame1, text="Wanna play a game?\n\nSelect difficulty 0-4:",font=("Comic Sans MS", 30),anchor=tk.CENTER).pack()
		tk.Entry(self.frame1,textvariable=self.difficulty,font=("Comic Sans MS", 30)).pack()
		if not vis:
			self.frame1.pack_forget()
 
	def test(self,vis,disp_image):
		_image = disp_image[0][self.hard]
		right_answer = disp_image[len(disp_image)-1]
		self.frame2 = tk.Frame(self.root,width=1000, height=8)
		self.frame2.pack( fill=tk.BOTH, expand=1)
		dip_Image(self.frame2,_image)
		if disp_image[2] == right_answer:
			btn_o1 = tk.Button(self.frame2,text = disp_image[1],font=("Comic Sans MS", 30),command = self.btn_c)
		else:
			btn_o1 = tk.Button(self.frame2,text = disp_image[1],font=("Comic Sans MS", 30),command = self.btn_nc)
		btn_o1.pack(anchor = tk.CENTER)

		if disp_image[3] == right_answer:
			btn_o1 = tk.Button(self.frame2,text = disp_image[2],font=("Comic Sans MS", 30),command = self.btn_c)
		else:
			btn_o1 = tk.Button(self.frame2,text = disp_image[2],font=("Comic Sans MS", 30),command = self.btn_nc)
		btn_o1.pack(anchor = tk.CENTER)

		if disp_image[4] == right_answer:
			btn_o1 = tk.Button(self.frame2,text = disp_image[3],font=("Comic Sans MS", 30),command = self.btn_c)
		else:
			btn_o1 = tk.Button(self.frame2,text = disp_image[4],font=("Comic Sans MS", 30),command = self.btn_nc)
		btn_o1.pack(anchor = tk.CENTER)
		if not vis:
			self.frame2.pack_forget()

	def test_solved(self,vis,image):
		self.frame4 = tk.Frame(self.root,width=600, height=400)
		self.frame4.pack( fill=tk.BOTH, expand=1)
		print("image : ",image)
		dip_Image(self.frame4,image)
		if not vis:
			self.frame4.destroy()


	def fin(self,vis,score):
		self.frame3 = tk.Frame(self.root,width=600, height=400)
		self.frame3.pack(fill=tk.BOTH, expand=1)
		tk.Label(self.frame3, text="You guessed:\n{}".format(score),font=("Comic Sans MS", 30)).pack()
		if not vis:
			self.frame3.destroy()
 
	def hide(self):
		if self.hidden == 0:
			self.hard=int(self.difficulty.get())
			if self.hard >4:
				self.hard = 4
			elif self.hard<0:
				self.hard = 0
			
			self.frame1.pack_forget()
			self.frame2.pack_forget()
			self.frame3.pack_forget()
			self.frame4.pack_forget()
			
			self.test(True,self.image_list[self.qiestion])
			self.hidden = 1
			return
		if self.hidden == 2:
			self.fin(True,self.score)

	def btn_pressed(self):
		self.frame2.pack_forget()
		self.frame4.pack_forget()
		
		self.test_solved(True,self.image_list[self.qiestion-1][0][5])
		if self.qiestion == 5:
			self.hidden = 2
		else:
			self.hidden = 0
		return
# correct
	def btn_c(self):
		self.score+=1
		self.qiestion += 1
		self.btn_pressed()
#not correct 
	def btn_nc(self):
		self.qiestion += 1
		self.btn_pressed()  
 
 
 
root = tk.Tk()
root.geometry("1000x800")
#generate_images()
app = App(root,[[[	"./.tmp0/gospod.png",
					"./.tmp1/gospod.png",
					"./.tmp2/gospod.png",
					"./.tmp3/gospod.png",
					"./.tmp4/gospod.png",
					"./.gospod.png"],"Vesko","Babev","Kartof","Babev"],
				[[	"./.tmp0/slawi.png",
					"./.tmp1/slawi.png",
					"./.tmp2/slawi.png",
					"./.tmp3/slawi.png",
					"./.tmp4/slawi.png",
					"./.slawi.png"],"Vesko","Pleshiv kartof","Slavi","Slavi"],
				[[	"./.tmp0/vesko_m.png",
					"./.tmp1/vesko_m.png",
					"./.tmp2/vesko_m.png",
					"./.tmp3/vesko_m.png",
					"./.tmp4/vesko_m.png",
					"./.vesko_m.png"],"Vesko","Wodopad","Slavi","Vesko"],
				[[	"./.tmp0/sashimi.png",
					"./.tmp1/sashimi.png",
					"./.tmp2/sashimi.png",
					"./.tmp3/sashimi.png",
					"./.tmp4/sashimi.png",
					"./.sashimi.png"],"Yellow?","Squidward","Artist","Squidward"],
				[[	"./.tmp0/scoomy.png",
					"./.tmp1/scoomy.png",
					"./.tmp2/scoomy.png",
					"./.tmp3/scoomy.png",
					"./.tmp4/scoomy.png",
					"./.scoomy.png"],"Clay Pit","Brown","Scooby","Scooby"]])
root.mainloop()





