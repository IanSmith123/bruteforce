#coding:utf-8
from keras.layers import(
	Input,
	Activation,
	merge,
	Dense,
	Reshape,
	Flatten,
	advanced_activations,
	TimeDistributed
)
from keras.layers.core import Dropout
from keras.models import Sequential
from keras.layers.pooling import MaxPooling2D
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import Conv2D
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from keras.models import Model
from keras.utils import plot_model
from keras.engine.topology import Layer
from keras import backend as K
from keras.layers.core import Permute
from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPool2D,Conv1D
import numpy as np
import tensorflow as tf
import sys  
sys.path.append('../')
#from utils import *  

def CNN2D_NET():
	'''
	模型结构
	'''
	#model.add(TimeDistributed(Dense(1)))
	input = Input(shape = (50,100,3))
	#reshape = Reshape((3,1,80,170))(input)
	#conv1 = Convolution2D(nb_filter = 32,kernel_size = 3,data_format='channels_last',border_mode = "same")(input)
	#conv2 = Convolution2D(nb_filter = 32,kernel_size = 3,data_format='channels_last',border_mode = "same")(conv1)
	conv1 = Convolution2D(nb_filter = 32,kernel_size = 3,data_format='channels_last')(input)
	conv1 = BatchNormalization()(conv1)
	conv1 = Activation('relu')(conv1)
	conv2 = Convolution2D(nb_filter = 32,kernel_size = 3,data_format='channels_last')(conv1)
	conv2 = BatchNormalization()(conv2)
	conv2 = Activation('relu')(conv2)
	pooling1 = MaxPooling2D((2,2))(conv2)

	conv3 = Convolution2D(nb_filter = 64,kernel_size = 3,data_format='channels_last')(pooling1)
	conv3 = BatchNormalization()(conv3)
	conv3 = Activation('relu')(conv3)
	conv4 = Convolution2D(nb_filter = 64,kernel_size = 3,data_format='channels_last')(conv3)
	conv4 = BatchNormalization()(conv4)
	conv4 = Activation('relu')(conv4)
	pooling2 = MaxPooling2D((2,2))(conv4)

	conv5 = Convolution2D(nb_filter = 128,kernel_size = 3,data_format='channels_last')(pooling2)
	conv5 = BatchNormalization()(conv5)
	conv5 = Activation('relu')(conv5)
	conv6 = Convolution2D(nb_filter = 128,kernel_size = 3,data_format='channels_last')(conv5)
	conv6 = BatchNormalization()(conv6)
	conv6 = Activation('relu')(conv6)
	pooling3 = MaxPooling2D((2,2))(conv6)

	'''
	conv7 = Convolution2D(nb_filter = 256,kernel_size = 3,data_format='channels_last')(pooling3)
	conv7 = BatchNormalization()(conv7)
	conv7 = Activation('relu')(conv7)
	conv8 = Convolution2D(nb_filter = 256,kernel_size = 3,data_format='channels_last')(conv7)
	conv8 = BatchNormalization()(conv8)
	conv8 = Activation('relu')(conv8)
	pooling4 = MaxPooling2D((2,2))(conv8)
	'''
	
	flatte1 = Flatten()(pooling3)
	d = Dropout(0.25)(flatte1)
	dense1 = Dense(10)(d)
	dense2 = Dense(10)(d)
	dense3 = Dense(10)(d)
	dense4 = Dense(10)(d)
	output1 = Activation('softmax')(dense1)
	output2 = Activation('softmax')(dense2)
	output3 = Activation('softmax')(dense3)
	output4 = Activation('softmax')(dense4)
	output = [output1,output2,output3,output4]
	#output = merge([output1,output2,output3,output4])
	model = Model(input = input,output = output)
	
	return model

if __name__ == '__main__':
	#测试用例
	model = CNN2D_NET()
	adam = Adam(lr=0.0001)
	model.compile(loss=weighted_loss_v1,optimizer=adam,metrics=[weighted_loss_v1])

	model.summary()

	hyperparams_name = 'CNN'
	plot_model(model,"{}.png".format(hyperparams_name),show_shapes = True)
