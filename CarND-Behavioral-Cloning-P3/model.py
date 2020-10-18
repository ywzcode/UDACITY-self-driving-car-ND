import numpy as np
import cv2
import os
import csv
from keras.models import Sequential, Model
from keras.layers import Flatten, Dense, Lambda, Convolution2D, Cropping2D, Dropout
from keras.layers.pooling import MaxPooling2D
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import sklearn

args = {}
args['data_path'] = '/opt/carnd_p3/data'
args['epochs'] = 2
args['correction'] = 0.2
args['batch_size'] = 32
args['test_size'] = 0.2


def shuffle_data(img_list, target_list):

	index = np.arange(len(img_list), dtype=np.int8)
	np.random.shuffle(index)

	return img_list[index], target_list[index]


def read_data(path, correction = None):
	
	imgs_path = {'center':[], 'left':[], 'right':[]}
	measurements = {'center':[], 'left':[], 'right':[]}
	with open(path + '/driving_log.csv') as csvFile:
		reader = csv.reader(csvFile)
		next(reader, None)
		for line in reader:
			imgs_path['center'].append(line[0].strip())
			imgs_path['left'].append(line[1].strip())
			imgs_path['right'].append(line[2].strip())
			angle = float(line[3].strip())
			measurements['center'].append(angle)
			
			if correction is not None:
				measurements['left'].append(angle + correction)
				measurements['right'].append(angle - correction)
				
	return imgs_path, measurements

def merge_data(path_dicts, measurements_dicts):
	'''
	If there are multiple data folders, then collect data and merge them.
	Args:
		path_dicts: list containing all path dicts. [{'center':[], 'left':[], 'right':[]}, {}....]
		measurements_dicts: list containing all measurements dicts. [{'center':[], 'left':[], 'right':[]}, {}....]
	return:
		img_paths: a list of all image path
		measurments: a list containing corresponding measurment
	'''
	img_paths = []
	measurments = []
	
	for i in range(len(path_dicts)):
		path_dict = path_dicts[i]
		measurements_dict = measurements_dicts[i]
		
		for key in path_dict:
			img_paths.extend(path_dict[key])
		
		for key in measurements_dict:
			measurments.extend(measurements_dict[key])
	
	return np.array(img_paths), np.array(measurments)


def generator(img_paths, measurments, batch_size=32, if_aug = True):
	"""
	Args:
		img_paths: a list of img path
		measurements: a list of measurments
		batch_size
	output:
		a gnerator
	"""
	num_samples = len(img_paths)
	while 1: # Loop forever so the generator never terminates
		img_paths, measurments = sklearn.utils.shuffle(img_paths, measurments)
		
		for offset in range(0, num_samples, batch_size):
			batch_img_paths, batch_measurments = img_paths[offset:offset+batch_size],\
												 measurments[offset:offset+batch_size]

			images, angles = [], []
			for imagePath, measurement in zip(batch_img_paths, batch_measurments):
				originalImage = cv2.imread('/opt/carnd_p3/data/'+imagePath)
				image = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)
				images.append(image)
				angles.append(measurement)
					
				images.append(cv2.flip(image, 1))
				angles.append(-1.0*measurement) 

			# trim image to only see section with road
			inputs = np.array(images)
			outputs = np.array(angles)
			yield sklearn.utils.shuffle(inputs, outputs)


class Model:
	def __init__(self, args):

		self.model = self.create_model()
		self.args = args
		

	def create_model(self):

		model = Sequential()

		model.add(Lambda(lambda x: (x / 255.0) - 0.5, input_shape=(160,320,3)))

		model.add(Cropping2D(cropping=((70,25),(0,0))))           

		model.add(Convolution2D(24,5,5, activation='relu',subsample=(2,2)))
		model.add(Convolution2D(36,5,5, activation='relu',subsample=(2,2)))
		model.add(Convolution2D(48,5,5, activation='relu',subsample=(2,2)))

		model.add(Convolution2D(64,3,3, activation='relu'))
		model.add(Convolution2D(64,3,3, activation='relu'))

		model.add(Flatten())

		model.add(Dense(100, activation='relu'))

		model.add(Dropout(0.25))

		model.add(Dense(50, activation='relu'))

		model.add(Dense(10, activation='relu'))

		model.add(Dense(1)) 

		return model
	def compile(self):
		self.model.compile(loss='mse',optimizer='adam')

	def fit_model(self, train_generator, validation_generator, num_train, num_val):
		self.model.fit_generator(train_generator, samples_per_epoch= \
			num_train, validation_data=validation_generator, \
			nb_val_samples=num_val, nb_epoch=self.args['epochs'], verbose=1)

	def save_model(self):
		self.model.save('model.h5')


if __name__ == "__main__":

	path_dicts, measurements_dicts = read_data(args['data_path'], correction = args['correction'])
	imagePaths, measurements = merge_data([path_dicts], [measurements_dicts])
	print(len(imagePaths))
	imagePaths, measurements = sklearn.utils.shuffle(imagePaths, measurements)#shuffle_data(imagePaths, measurements)

	num_val = int(len(imagePaths) * args['test_size'])
	num_train = len(imagePaths) - num_val
	

	print('Train samples: {}'.format(num_train))
	print('Validation samples: {}'.format(num_val))

	train_generator = generator(imagePaths[:num_train], measurements[:num_train], \
					batch_size=args['batch_size'])
	validation_generator = generator(imagePaths[num_train:], measurements[num_train:], \
					batch_size=args['batch_size'])


	model = Model(args)
	model.compile()
	model.fit_model(train_generator, validation_generator, num_train, num_val)
	model.save_model()
	print('Done! Model Saved!')
	model.model.summary()

	# plt.plot(history_object.history['loss'])
	# plt.plot(history_object.history['val_loss'])
	# plt.title('model mean squared error loss')
	# plt.ylabel('mean squared error loss')
	# plt.xlabel('epoch')
	# plt.legend(['training set', 'validation set'], loc='upper right')
	# plt.show()

					  