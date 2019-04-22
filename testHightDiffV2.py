# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/23 10:46
# @Author  : nanganglei
# @File    : testHightDiff.py
from PIL import Image, ImageChops, ImageDraw
point_table = ([0] + ([255] * 255))

def  new_gray( size, color):
    img = Image.new('L',size)
    dr = ImageDraw.Draw(img)
    dr.rectangle((0,0) + size, color)
    return img

def black_or_b(nameA, nameB, opacity=0.8):
    a = Image.open(nameA)
    b = Image.open(nameB)
    #print a
    #print b
    # 如果要比较的两个图片大小不一致，创建一个max box，将较小的图片paste到max box中
    if a.size != b.size:
        max_size = (max(a.size[0],b.size[0]),max(a.size[1],b.size[1]))
        if a.size != max_size:
            new_im_a = Image.new("RGBA",max_size)
            new_im_a.paste(a,(0,0))
            a = new_im_a
        if b.size != max_size:
            new_im_b = Image.new("RGBA",max_size)
            new_im_b.paste(b,(0,0))
            b = new_im_b
    # print "The sizes of two images are same!"
    diff = ImageChops.difference(a, b)  # difference要求size、mode均要一致，可直接print查看
    diff = diff.convert('L')
    # Hack: there is no threshold in PILL,
    # so we add the difference with itself to do
    # a poor man's thresholding of the mask:
    # (the values for equal pixels-  0 - don't add up)
    thresholded_diff = diff
    for repeat in range(3):
        thresholded_diff = ImageChops.add(thresholded_diff, thresholded_diff)
    h,w = size = diff.size
    mask = new_gray(size, int(255 * (opacity)))
    shade = new_gray(size, 0)
    new = a.copy()
    new.paste(shade, mask=mask)
    # To have the original image show partially
    # on the final result, simply put "diff" instead of thresholded_diff bellow
    new.paste(b, mask=thresholded_diff)
    return new


def saveComparedImg(img1,img2,path):
    c = black_or_b(img1,img2)
    # print path
    c.save(path)



if __name__ == "__main__":
    nameA = ('1168_2300--985xianshang.jpg')
    nameB = ('1168_2300--985xianxia.jpg')
    saveComparedImg(nameA,nameB,"test3.png")
    # c = black_or_b(nameA, nameB)
    # c.save('test3.png')