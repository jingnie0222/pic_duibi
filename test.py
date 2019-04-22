from __future__ import print_function
from PIL import Image


im = Image.open("02_221_1--xianxia.png")
print(im)
print(im.format, im.size, im.mode)