import imageio
from scipy.linalg import svd
from numpy import array
from numpy import diag
from numpy import dot
from numpy import zeros
from scipy.linalg import svd
#inslall imageio first form pip

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
    l_sigma = zeros((len(ch), len(ch[0])))
    
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

im = imageio.imread('milko.png')
red = split_channel(im,RED) 
green = split_channel(im,GREEN)
blue = split_channel(im,BLUE)

deep_fry = 2
red_w = decompose_recompose(red,deep_fry) 
green_w = decompose_recompose(green,deep_fry)
blue_w = decompose_recompose(blue,deep_fry)

imageio.imwrite("milko2.png",compose_png(red_w,green_w,blue_w))

 
