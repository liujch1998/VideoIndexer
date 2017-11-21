import os
import sys
import numpy as np
import h5py
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications

image_size = (128, 128)

neg_cnt = int(sys.argv[1])
pos_cnt = int(sys.argv[2])
sample_cnt = neg_cnt + pos_cnt
epochs = 100
batch_size = 16
data_dir = 'lib/crowded/'
dir_test = 'frame/ZuTA81uGJjU/'
sample_cnt_test = 301

model = applications.VGG16(include_top=False, weights='imagenet')
datagen = ImageDataGenerator(rescale=1./255)

gen = datagen.flow_from_directory(
	data_dir, 
	target_size=image_size, 
	batch_size=batch_size, 
	class_mode=None, 
	shuffle=False)
x = model.predict_generator(gen, sample_cnt // batch_size)
y = np.array([0] * neg_cnt + [1] * pos_cnt)

gen_test = datagen.flow_from_directory(
	dir_test, 
	target_size=image_size, 
	batch_size=batch_size, 
	class_mode=None, 
	shuffle=False)
x_test = model.predict_generator(gen_test, sample_cnt_test // batch_size)

model = Sequential()
model.add(Flatten(input_shape=x.shape[1:]))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(
	optimizer='rmsprop', 
	loss='binary_crossentropy', 
	metrics=['accuracy'])
model.fit(x, y, 
	epochs=epochs, 
	batch_size=batch_size)

w = model.predict(x_test, 
	batch_size=batch_size)
def formate(name):
	num = int(name[2:10], base=10) // 25
	return str(num // 60) + ':' + str(num % 60)
for t in range(sample_cnt_test):
	if w[t][0] >= 0.9:
		print(formate(gen_test.filenames[t]))
'''
t = np.array(w).reshape((sample_cnt_test,)).argsort()[-10:][::-1]
t = sorted(t)
for tt in t:
	print(formate(gen_test.filenames[tt]))
'''

