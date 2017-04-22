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

conn = MySQLdb.connect(host='localhost',port=3306,user='root',passwd='ubuntu',db='O2M',charset="utf8")
cur = conn.cursor()

if not os.path.exists("./log/import.log"):
	os.mknod('./log/import.log')

def create_table():
	cur.execute("show tables")
	tables=cur.fetchall()
	a=zip(*tables)	
	if 'ofo_data' not in a[0]:
		cur.execute("create table ofo_data (date varchar(14),number varchar(7),passwd varchar(4))")
		conn.commit()
def insert_data(date,number,passwd):
 	cur.execute("insert into ofo_data values('%s','%s','%s')"%(date,number,passwd))
	conn.commit()
def get_files(topdown=True):
	dir=('./raw')
	fileList = [] 
 	for root, dirs, files in os.walk(dir, topdown):
		for PicName in files:
			fileList.append(os.path.join(root,PicName)) 
		for file in sorted(fileList):
			with open('./log/import.log','r') as f:
				f=f.read()
			if file in f :
				print "{}:------Has Been Exist!".format(file)
			if file not in f:
				with open("./log/import.log",'a') as f:
					f.write(file+'\n')
				print file
				result=get_rec(file)
				number,passwd=result[1],result[0]
				time=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
				print time
				print "number is :" + number
				print "passwd is :" + passwd
				insert_data(time,number,passwd)

				print("******************************************")
def get_rec(file):
	dict={}
	passwd_raw=[]
	number_raw=[]
	raw = cv2.imread(file)
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
				dict[pt[0]]=i
			order=sorted(dict.items(), key=lambda t: t[0])
		if len(order)==4:
			for i in range(0,len(order)):
				passwd_raw.append(order[i][1])
			passwd="".join(passwd_raw)
		else:
			for i in range(0,len(order)):
				number_raw.append(order[i][1])
			number="".join(number_raw)

		dict.clear()
	return  passwd,number


if __name__ == '__main__':
	create_table()
	get_files()
