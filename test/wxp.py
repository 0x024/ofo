import cv2
import os
import datetime
import MySQLdb
import numpy as np

part_number=['./data/B-1.png','./data/B-2.png',
		'./data/B-3.png','./data/B-4.png','./data/B-5.png','./data/B-6.png',
		'./data/B-7.png','./data/B-8.png','./data/B-9.png','./data/B-0.png']

part_passwd=['./data/A-1.png','./data/A-2.png','./data/A-3.png','./data/A-4.png',
		'./data/A-5.png','./data/A-6.png','./data/A-7.png','./data/A-8.png',
		'./data/A-9.png','./data/A-0.png']

def get_rec():
	raw = cv2.imread('./temp.png')
	img_gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
	for data1 in [part_passwd,part_number]:
		for data in  data1:
			i=data.split('/')[2].split('-')[1].split('.')[0]
			template = cv2.imread(data,0)
			w, h = template.shape[::-1]
			res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
			threshold = 0.99
			loc = np.where( res >= threshold)
			for pt in zip(*loc[::-1]):
				cv2.rectangle(raw, pt, (pt[0] + w, pt[1] + h), (255,255,0), 2)
				cv2.putText(raw,i, (pt[0],pt[1] ), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255), 5)

			cv2.imwrite('res.png',raw)



if __name__ == '__main__':
	get_rec()
