## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/chessboard_undistort.png "Undistorted"
[image2]: ./output_images/distortion-corrected.png "Road Transformed"
[image3]: ./output_images/segment.png "Binary Example"
[image4]: ./output_images/bird_eye_example.png "Warp Example"
[image5]: ./output_images/color_fit_lines.jpg "Fit Visual"
[image6]: ./output_images/example.png "Output"
[video1]: ./project_video.mp4 "Video"



#### 1. All codes are at Advanced_Lane_Finding_Project.ipynb

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the first code cell 1-6 of the IPython notebook located in "Advanced_Lane_Finding_Project.ipynb".

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![alt text][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image at cell 8-10 located in "Advanced_Lane_Finding_Project.ipynb". In this step, thresholding for s channle of HSL color space is used. Also, I threshold the gradients with respect to x and y directions and the gradient magnitude. Here's an example of my output for this step.  (note: this is not actually from one of the test images)

![alt text][image3]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

In cell 11-12 in Advanced_Lane_Finding_Project.ipynb, I define the perspective transform. The src and dst points are used to estimate Perspective Transformation. The `get_perspective_img()` function takes as inputs an image (`img`), as well as estimated transformation matrix `M`.  I chose the hardcode the source and destination points in the following manner:

```python
src = np.float32([(585, 460),
                  (695, 460), 
                  (203, 720), 
                  (1127, 720)])

dst = np.float32([(320, 0),
                  (960, 0), 
                  (320, 720), 
                  (960, 720)])
```

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

In cell 15 of my IPython notebook, I defined `find_lane_pixels()` and `search_around_poly()`. `find_lane_pixels` is used if there were no line fitted yet, while `search_around_poly()` is used if we know the line of previous frame.
```python
Input: segmented and filtered image
1. Take the histogram of input to obtain two peaks positions (left and right).
2. Use sliding windows moving upward in the image (further along the road) to determine where the lane lines go.
Output: left and right lane line pixels positions.
```
When we know the fitting result of previous frame, we can start from the line of previous step. 

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

The algorithm is implemented in the Lane class in code cell 31 of the IPython notebook in the function _curvate_radius().

It basically fits the left and right curve with the polyfit function of OpenCV. After that these are converted into radian degrees and weighted half-half.
#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

This step is as well done in the Lane class with the function fill_lanes().

Here, some points of the calculated 2nd order fit are extracted and printed into the picture to fill the space between right and left lane.

Moreover, the curvature and distance are put into the picture.

Here is an example of my result on a test image:


![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [https://github.com/ywzcode/UDACITY-self-driving-car-ND/blob/master/CarND-Advanced-Lane-Lines/project_video.mp4](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  
