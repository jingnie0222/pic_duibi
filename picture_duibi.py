# -*- coding: utf-8 -*-
"""
https://blog.csdn.net/gzlaiyonghao/article/details/2325027

"""

# import Image
import PIL
from PIL import Image
from PIL import ImageDraw
# import ImageDraw

#统一转化为RGB模式
def make_regalur_image (img, size = (256, 256)):
	return img.resize(size).convert('RGB')

#切分图片，细化局部图片信息
def split_image(img, part_size = (64, 64)):
	w, h = img.size
	pw, ph = part_size
	assert w % pw == h % ph == 0
	return [img.crop((i, j, i+pw, j+ph)).copy() \
				for i in range(0, w, pw) \
				for j in range(0, h, ph)]

#计算直方图数据
def hist_similar(lh, rh):
	assert len(lh) == len(rh)
	return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

#计算图片相似度
def calc_similar(li, ri):
	return hist_similar(li.histogram(), ri.histogram())
	#return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0

def calc_similar_by_path(lf, rf):
	li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
	return calc_similar(li, ri)

def make_doc_data(lf, rf):
	li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
	li.save(lf + '_regalur.png')
	ri.save(rf + '_regalur.png')
	fd = open('stat.csv', 'w')
	fd.write('\n'.join(l + ',' + r for l, r in zip(map(str, li.histogram()), map(str, ri.histogram()))))
#	print >>fd, '\n'
#	fd.write(','.join(map(str, ri.histogram())))
	fd.close()

	li = li.convert('RGB')
	draw = PIL.ImageDraw.Draw(li)
	for i in range(0, 256, 64):
		draw.line((0, i, 256, i), fill = '#ff0000')
		draw.line((i, 0, i, 256), fill = '#ff0000')
	li.save(lf + '_lines.png')


if __name__ == '__main__':
	print(calc_similar_by_path('02_221_1--xianxia.png','02_221_1--线上.png'))

