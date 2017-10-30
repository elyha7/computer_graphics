import argparse
from PIL import Image
import PIL
import numpy as np
import numpy as np
from math import pi,exp
from functions import *
parser = argparse.ArgumentParser()

parser.add_argument("-corr_linear",'--corr_linear', nargs = 2)
parser.add_argument("-corr_nonlinear",'--corr_nonlinear', nargs = 3)
parser.add_argument("-invert",'--invert', nargs = 2)
parser.add_argument("-bw",'--bw', nargs = 2)
parser.add_argument("-wb_ww",'--wb_ww', nargs = 2)
parser.add_argument("-wb_gw",'--wb_gw', nargs = 2)
parser.add_argument("-gauss",'--gauss', nargs = 4)
parser.add_argument("-box",'--box', nargs = 3)
parser.add_argument("-median",'--median', nargs = 3)
parser.add_argument("-crop",'--crop', nargs = 6)
args = parser.parse_args()
#print(args)
if args.corr_linear:
    img=Image.open(args.corr_linear[-2])
    result=Correction(img,mode='linear')
    result.save(args.corr_linear[-1])
if args.corr_nonlinear:
    img=Image.open(args.corr_nonlinear[-2])
    result=Correction(img,mode='power',gamma=float(args.corr_nonlinear[0]))
    result.save(args.corr_nonlinear[-1])
if args.invert:
    img=Image.open(args.invert[-2])
    result=ColorFilter(img,mode='negative')
    result.save(args.invert[-1])
if args.bw:
    img=Image.open(args.bw[-2])
    result=ColorFilter(img,mode='monochrome')
    result.save(args.bw[-1])
if args.wb_ww:
    img=Image.open(args.wb_ww[-2])
    result=WhiteBalance(img,mode='white')
    result.save(args.wb_ww[-1])
if args.wb_gw:
    img=Image.open(args.wb_gw[-2])
    result=WhiteBalance(img,mode='grey')
    result.save(args.wb_gw[-1])
if args.box:
    img=Image.open(args.box[-2])
    result=CustomFilter(img,filter_size=int(args.box[0]),mode='box')
    result.save(args.box[-1])
if args.gauss:
    img=Image.open(args.gauss[-2])
    result=CustomFilter(img,filter_size=int(args.gauss[0]),mode='gaus',sigma=int(args.gauss[1]))
    result.save(args.gauss[-1])
if args.median:
    img=Image.open(args.median[-2])
    result=CustomFilter(img,filter_size=int(args.median[0]),mode='median')
    result.save(args.median[-1])
if args.crop:
    img=Image.open(args.crop[-2])
    l,t,w,h=map(int,(args.crop[0],args.crop[1],args.crop[2],args.crop[3]))
    result=Crop(img,l,t,w,h)
    result.save(args.crop[-1])
