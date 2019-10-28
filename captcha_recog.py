#coding:utf-8
import sys  
sys.path.append('../')  
#from utils import *
from Net import *
import os
import numpy as np
from PIL import Image
from io import BytesIO
import numpy as np
from keras.preprocessing.image import img_to_array
import warnings

warnings.filterwarnings('ignore')


def read_img(img):
	'''
	将图片转化为模型标准输入
	'''
	img = Image.open(BytesIO(img))
	#print(type(img))
	x = img_to_array(img) # 将图片转为数组 
	x = x.astype('float32')
	x /= 255
	return x

def convert_predict2labels(predict):
	'''
	将模型输出（独热码）转为数字
	'''
	r = []
	for i in range(predict[0].shape[0]):
		temp = []
		for j in range(len(predict)):
			temp.append(np.argmax(predict[j][i]))
		r.append(temp)  
	return r


def get_captcha(img):
	'''
	识别图片验证码的内容
	param img:请求到的待识别验证码
	return :识别后的验证码内容
	'''
	X = []
	img = read_img(img)
	#print(type(img))
	X.append(img)
	X = np.array(X)
	model = CNN2D_NET()	
	adam = Adam(lr=0.0001)
	model.compile(loss='categorical_crossentropy',optimizer=adam,metrics = ['accuracy'])
	model.load_weights('./model/weights.97.hdf5')
	Y_predic_map = model.predict(X, batch_size = 32, verbose=0)
	#EvaluateSinglePrecision(Y,Y_predic_map)
	predict_labels = convert_predict2labels(Y_predic_map)
	code = predict_labels[0]
	return code

	