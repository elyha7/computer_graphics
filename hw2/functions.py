from PIL import Image
import PIL
import numpy as np
import numpy as np
from math import pi,exp
def Correction(img,mode='linear',gamma=0.5):
    r,g,b=map(lambda x:np.array(x,dtype='float')/255,img.split())
    if mode=='linear':
        r,g,b=map(lambda p: ApplyCorrection(p,mode='linear'),(r,g,b))
        img=PilFromRGB(r,g,b)
        return img
    if mode=='power':
        r,g,b=map(lambda p: ApplyCorrection(p,mode='power',gamma=gamma),(r,g,b))
        img=PilFromRGB(r,g,b)
        return img
        
def ApplyCorrection(img,mode='linear',gamma=0.5):
    if mode=='linear':
        max_v=img.max()
        min_v=img.min()
        for i in np.nditer(img,op_flags=['readwrite']):
            i[...]=((i-min_v)/(max_v-min_v))
        return img*255
    if mode=='power':
        img=img**gamma
        return img*255

def Crop(img,left,top,width,hight):
    r,g,b=map(np.array,img.split())
    r,g,b=map(lambda p:ApplyCrop(p,left,top,width,hight),(r,g,b))
    return PilFromRGB(r,g,b)
def ApplyCrop(img,left,top,width,hight):
    return img[top:(top+hight),left:(left+width)]


def CustomFilter(img,filter_size,mode='box',sigma=None):
    #my_filter=np.zeros((filter_size,filter_size))
    r,g,b=map(lambda x:np.array(x,dtype='float'),img.split())
    r,g,b=map(lambda x:AddBorders(x,filter_size),(r,g,b))
    if mode=='box':
        r,g,b=map(lambda x:ApplyCustomFilter(x,filter_size,mode='box'),(r,g,b))
    if mode=='gaus':
        r,g,b=map(lambda x:ApplyCustomFilter(x,filter_size,mode='gaus',sigma=sigma),(r,g,b))
    if mode=='median':
        r,g,b=map(lambda x:ApplyCustomFilter(x,filter_size,mode='median'),(r,g,b))
    return PilFromRGB(r,g,b)
def ApplyCustomFilter(img,filter_size,mode='box',sigma=None):
    border=int((filter_size-1)/2)
    new_img=np.zeros((img.shape[0]-border*2,img.shape[1]-border*2))
    if mode=='box':
        myfilter=np.ones((filter_size,filter_size))/(filter_size**2)
        for i in range(new_img.shape[0]):
            for j in range(new_img.shape[1]):
                new_img[i][j]=np.multiply(img[i:i+filter_size,j:j+filter_size],myfilter).sum()
    if mode=='gaus':
        myfilter=gkern(filter_size,sigma)
        for i in range(new_img.shape[0]):
            for j in range(new_img.shape[1]):
                new_img[i][j]=np.multiply(img[i:i+filter_size,j:j+filter_size],myfilter).sum()
    if mode=='median':
        for i in range(new_img.shape[0]):
            for j in range(new_img.shape[1]):
                new_img[i][j]=np.median(img[i:i+filter_size,j:j+filter_size])      
    return new_img


def ColorFilter(img,mode='monochrome'):
    r,g,b=map(lambda x:np.array(x,dtype='float')/255,img.split())
    rgb=np.stack((r,g,b))
    new_img=np.zeros_like(rgb)
    if mode=='monochrome':
        matrix=[[0.2125,0.7154,0.0721],
                [0.2125,0.7154,0.0721],
                [0.2125,0.7154,0.0721]]
        new_img=ApplyColorFilter(rgb,matrix)
        if np.array_equal(new_img[0,::],new_img[1,::]):
            new_img=(new_img*255).astype('uint8')
            return Image.fromarray(new_img[0,::],mode='L')
        else:
            print('Error monochrome')
            return -1
    if mode=='negative':
        matrix=[[-1,0,0],
                [0,-1,0],
                [0,0,-1]] 
        new_img=ApplyColorFilter(rgb,matrix)
        new_img=((new_img+1)*255).astype('uint8')
        return PilFromRGB(new_img[0],new_img[1],new_img[2])
def ApplyColorFilter(img,matrix):
    new_img=np.zeros_like(img)
    for i in range(img.shape[1]):
        for j in range(img.shape[2]):
            new_img[:,i,j]=np.dot(matrix,img[:,i,j])
    return new_img


def WhiteBalance(img,mode='white'):
    r,g,b=map(lambda x:np.array(x,dtype='float'),img.split())
    Average=(r+g+b).mean()/3
    if mode=='white':
        rgb=np.stack((r,g,b))
        max_pixel=np.unravel_index(np.argmax(np.sum(rgb,axis=0)), r.shape)
        r,g,b=map(lambda x: np.clip(x*255/x[max_pixel],0,255),(r,g,b))
    if mode=='grey':
        r,g,b=map(lambda x:x*Average/x.mean(),(r,g,b))
    return PilFromRGB(r,g,b)


def AddBorders(img,filter_size):
    border_size=int((filter_size-1)/2)
    temp=np.zeros((img.shape[0]+2*(border_size),img.shape[1]+2*(border_size)))
    temp[border_size:-border_size,border_size:-border_size]=img
    return temp
def PilFromRGB(r,g,b):
    rgbArray = np.zeros((r.shape[0],r.shape[1],3), 'uint8')
    rgbArray[..., 0] = r
    rgbArray[..., 1] = g
    rgbArray[..., 2] = b
    return Image.fromarray(rgbArray)
def gkern(l=5, sig=1.):
    
    ax = np.arange(-l // 2 + 1., l // 2 + 1.)
    xx, yy = np.meshgrid(ax, ax)

    kernel = np.exp(-(xx**2 + yy**2) / (2. * sig**2))

    return kernel / np.sum(kernel)
