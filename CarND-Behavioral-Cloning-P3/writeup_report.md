# **Behavioral Cloning** 
---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./examples/model_P4.png "Model Visualization"
[image2]: ./examples/sample_data.jpg "Grayscaling"
[image3]: ./examples/sample_left.png "Recovery Image"
[image4]: ./examples/sample_right.png "Recovery Image"
[image5]: ./examples/placeholder_small.png "Recovery Image"
[image6]: ./examples/placeholder_small.png "Normal Image"
[image7]: ./examples/placeholder_small.png "Flipped Image"

## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network 
* writeup_report.md or writeup_report.pdf summarizing the results

#### 2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py model.h5
```

#### 3. Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### Model Architecture and Training Strategy

#### 1. An appropriate model architecture has been employed

I used the model of [NVIDIA](https://images.nvidia.com/content/tegra/automotive/images/2016/solutions/pdf/end-to-end-dl-using-px.pdf). The only difference is that our image has a different size. 

#### 2. Attempts to reduce overfitting in the model

The model contains dropout layers in order to reduce overfitting (model.py lines 133). 

The model was trained and validated on different data sets to ensure that the model was not overfitting (code line 168-171). The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track. Here, we choose 20% of the data as validation data.

#### 3. Model parameter tuning

The model used an adam optimizer, so the learning rate was not tuned manually (model.py line 143).

#### 4. Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I directly used the sample data provided by Udacity which is enough for training track1. I used a combination of center lane driving, recovering from the left and right sides of the road with a correction 0.2 Also, image filp is used as a data augmentaion. 

For details about how I created the training data, see the next section. 

### Model Architecture and Training Strategy

#### 1. Solution Design Approach

In order to gauge how well the model was working, I split my image and steering angle data into a training and validation set. In the model, dropout is used to combat the overfitting. Also, some data augmentation strageties were used to boost learning, which wll be discussed later.

To test the model performance, I run the simulator to see how well the car was driving around track one. At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road.

#### 2. Final Model Architecture

The final model architecture is defiend in model.py lines 107-151 (Model class). The final architecture is shown as:

![alt text][image1]

#### 3. Creation of the Training Set & Training Process

In this project, I found that using the data provided by Udacity is enough. But I also collected my own data. Here is an example image of center lane driving:

![alt text][image2]

There are also left and right cameras, which shows:

![alt text][image3]
![alt text][image4]

To utilize these left and right images, I augment their measurments with a correction 0.2. For example, if the angle of center view is $a$, then the left one is $a +0.2$, and the right one is $a-0.2$. 

To augment the data sat, I also flipped images and angles thinking that this would can let the model learn a different direction. 

After the collection process, I had X number of data points. I then preprocessed this data by cropping the image from size of (160, 320, 3) to (65, 320, 3).

I finally randomly shuffled the data set and put 20% of the data into a validation set. 

I used this training data for training the model. The validation set helped determine if the model was over or under fitting. I found 2 epochs are enough for training a good model. I used an adam optimizer so that manually training the learning rate wasn't necessary.