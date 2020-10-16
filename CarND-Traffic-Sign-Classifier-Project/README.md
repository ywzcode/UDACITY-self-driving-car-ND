# **Traffic Sign Recognition** 

---

**Build a Traffic Sign Recognition Project**

The goals / steps of this project are the following:
* Load the data set (see below for links to the project data set)
* Explore, summarize and visualize the data set
* Design, train and test a model architecture
* Use the model to make predictions on new images
* Analyze the softmax probabilities of the new images
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./examples/example1.jpg "Visualization"
[image2]: ./examples/example_gray2.png "Grayscaling"
[image3]: ./examples/accuracy_curve.png "Random Noise"
[image4]: ./examples/example_mysigns.png "Traffic Sign 1"
[image5]: ./examples/example_mysigns_prediction.png "Traffic Sign 2"
[image6]: ./examples/example_softmax.png "Traffic Sign 3"


## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/481/view) individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

You're reading it! and here is a link to my [project code](https://github.com/ywzcode/UDACITY-self-driving-car-ND/blob/master/CarND-Traffic-Sign-Classifier-Project/Traffic_Sign_Classifier.ipynb)

### Data Set Summary & Exploration

#### 1. Provide a basic summary of the data set. In the code, the analysis should be done using python, numpy and/or pandas methods rather than hardcoding results manually.

I used the numpy and pandas library to calculate summary statistics of the traffic
signs data set:

* The size of training set is 34799
* The size of the validation set is 4410
* The size of test set is 12630
* The shape of a traffic sign image is (32, 32, 3)
* The number of unique classes/labels in the data set is 43

#### 2. Include an exploratory visualization of the dataset.

The code for this step is contained in the 3-5 cell of the IPython notebook.

Here is an exploratory visualization of the data set. In this step, I select 20 samples for 20 classes. Also, the label name is used based on signnames.csv. Part of the example is shown as:

![alt text][image1]

### Design and Test a Model Architecture

#### 1. Describe how you preprocessed the image data. What techniques were chosen and why did you choose these techniques? Consider including images showing the output of each preprocessing technique. Pre-processing refers to techniques such as converting to grayscale, normalization, etc. (OPTIONAL: As described in the "Stand Out Suggestions" part of the rubric, if you generated additional data for training, describe why you decided to generate additional data, how you generated the data, and provide example images of the additional data. Then describe the characteristics of the augmented training set like number of images in the set, number of images for each class, etc.)

The code for this step is contained in the 6-9 cell of the IPython notebook.

As a first step, I decided to convert the images to grayscale because it has been shown effective in the technical paper "Traffic Sign Recognition with Multi-Scale Convolutional Networks". It seems that grayscale image is easier to learn good features for this small neural network (LeNet).

Here is an example of a traffic sign image before and after grayscaling.

![alt text][image2]

As a last step, I normalized the image data because it is beneficial to normalize the input to [-1, 1] in neural network. 

#### 2. Describe what your final model architecture looks like including model type, layers, layer sizes, connectivity, etc.) Consider including a diagram and/or table describing the final model.
The code for this step is contained in the cell 10 of the IPython notebook.
In this step, I employed the LeNet architecture. Also, some additional dropout and batch normalization layers are added to overcome overfitting on test set. The input I use is the gray scale image. 

My final model consisted of the following layers:
| Layer         		|     Description	        					| 
|:---------------------:|:---------------------------------------------:| 
| Input         		| 32x32x1 gray image   							| 
| Convolution 	5x5     	| 1x1 stride, valid padding, outputs 28x28x6	|
| RELU					|												|
| Max pooling	      	| 2x2 stride,  outputs 14x14x6 				|
| Convolution 5x5	    | 1x1 stride, valid padding, outputs 10x10x16				|
| RELU					|												|
| Max pooling	      	| 2x2 stride,  outputs 5x5x16 				|
| Flatten	      	| Inputs 5x5x16,  outputs 400 				|
| Dropout | 0.5 keep prob |
| Fully connected| Output = 120. |
| RELU					|												|
| Batch normalization					|												|
| Dropout | 0.5 keep prob |
| Fully connected| Output = 84. |
| RELU					|												|
| Batch normalization					|												|
| Dropout | 0.5 keep prob |
| Fully connected| Output = 43. |

#### 3. Describe how you trained your model. The discussion can include the type of optimizer, the batch size, number of epochs and any hyperparameters such as learning rate.

The code for this step is contained in the cell 10 - 13 of the IPython notebook.
To train the model, I used the AdamOptimizer with learning rate 1e-3. I choose the batch size as 256 and train the model for 50 epochs. 

#### 4. Describe the approach taken for finding a solution and getting the validation set accuracy to be at least 0.93. Include in the discussion the results on the training, validation and test sets and where in the code these were calculated. Your approach may have been an iterative process, in which case, outline the steps you took to get to the final solution and why you chose those steps. Perhaps your solution involved an already well known implementation or architecture. In this case, discuss why you think the architecture is suitable for the current problem.

The code for this step is contained in the cell 13 - 14 of the IPython notebook.
The validtion accuracy curve is shown as:
![alt text][image3]

My final model results were:
* training set accuracy of 0.992
* validation set accuracy of 0.963
* test set accuracy of 0.945

If an iterative approach was chosen:
* What was the first architecture that was tried and why was it chosen?
My first version architecture is the original LeNet without dropout and batch normalization. Also, I used RGB image as the input at the begining. I choose this architecture since it is a simple but effective conv net. 

* What were some problems with the initial architecture?
I found that it works not as good as I expected on the test set. Overfitting problem exists. 

* How was the architecture adjusted and why was it adjusted? Typical adjustments could include choosing a different model architecture, adding or taking away layers (pooling, dropout, convolution, etc), using an activation function or changing the activation function. One common justification for adjusting an architecture would be due to overfitting or underfitting. A high accuracy on the training set but low accuracy on the validation set indicates over fitting; a low accuracy on both sets indicates under fitting.

I found the gray image works better. Also, the dropout and batch normalization can boost the performance on the test set. Typically these two tricks can alleviate the overfitting problem.

* Which parameters were tuned? How were they adjusted and why?
The learning rate was tuned. I tried the learning rate with 1e-4, 5e-4 and 1e-3, and 1e-3 works the best. The learning rate is significant in leanring-based problem. It should be suitable, otherwise the network cannot converge. 

* What are some of the important design choices and why were they chosen? For example, why might a convolution layer work well with this problem? How might a dropout layer help with creating a successful model?
I think the data normalization is important. By limiting the data to [-1, 1], it is better for the activation function and network backpropagation. Also, the convolution layer can learn the local spatial feature, thus it works well on this task. Dropout can alleviate the overfitting problem. 

### Test a Model on New Images

#### 1. Choose five German traffic signs found on the web and provide them in the report. For each image, discuss what quality or qualities might be difficult to classify.

Here are 6 German traffic signs that I found on the web:

![alt text][image4]
The 4th image (Road work) might be difficult to classify because the center part may be hard for network to distinguish. 

#### 2. Discuss the model's predictions on these new traffic signs and compare the results to predicting on the test set. At a minimum, discuss what the predictions were, the accuracy on these new predictions, and compare the accuracy to the accuracy on the test set (OPTIONAL: Discuss the results in more detail as described in the "Stand Out Suggestions" part of the rubric).

Here are the results of the prediction:

| Image			        |     Prediction	        					| 
|:---------------------:|:---------------------------------------------:| 
| Keep right     		| Keep right   									| 
| Priority     			| Priority 										|
| Speed limit (30 km/h)					| Speed limit (30 km/h)											|
| Road work	      		| Keep left					 				|
| Go straight or left		| Go straight or left      							|
| General caution		| General caution      							|


The model was able to correctly guess 5 of the 6 traffic signs, which gives an accuracy of 83.3%. The wrong prediction is the one we guess that may be hard for the netowrk. It seems that the learned feature for the centeral part is misleading. The result is shown as:

![alt text][image5]

#### 3. Describe how certain the model is when predicting on each of the five new images by looking at the softmax probabilities for each prediction. Provide the top 5 softmax probabilities for each image along with the sign type of each probability. (OPTIONAL: as described in the "Stand Out Suggestions" part of the rubric, visualizations can also be provided such as bar charts)

The code for making predictions on my final model is located in the 19th cell of the Ipython notebook.

The top five soft max probabilities are
![alt text][image6]

### (Optional) Visualizing the Neural Network (See Step 4 of the Ipython notebook for more details)
#### 1. Discuss the visual output of your trained network's feature maps. What characteristics did the neural network use to make classifications?

