# CarND-Path-Planning-Project
Self-Driving Car Engineer Nanodegree Program
   
### Simulator.
You can download the Term3 Simulator which contains the Path Planning Project from the [releases tab (https://github.com/udacity/self-driving-car-sim/releases/tag/T3_v1.2).  

To run the simulator on Mac/Linux, first make the binary file executable with the following command:
```shell
sudo chmod u+x {simulator_file_name}
```

### Goals
In this project your goal is to safely navigate around a virtual highway with other traffic that is driving +-10 MPH of the 50 MPH speed limit. You will be provided the car's localization and sensor fusion data, there is also a sparse map list of waypoints around the highway. The car should try to go as close as possible to the 50 MPH speed limit, which means passing slower traffic when possible, note that other cars will try to change lanes too. The car should avoid hitting other cars at all cost as well as driving inside of the marked road lanes at all times, unless going from one lane to another. The car should be able to make one complete loop around the 6946m highway. Since the car is trying to go 50 MPH, it should take a little over 5 minutes to complete 1 loop. Also the car should not experience total acceleration over 10 m/s^2 and jerk that is greater than 10 m/s^3.

#### The map of the highway is in data/highway_map.txt
Each waypoint in the list contains  [x,y,s,dx,dy] values. x and y are the waypoint's map coordinate position, the s value is the distance along the road to get to that waypoint in meters, the dx and dy values define the unit normal vector pointing outward of the highway loop.

The highway's waypoints loop around so the frenet s value, distance along the road, goes from 0 to 6945.554.

## Basic Build Instructions

1. Clone this repo.
2. Make a build directory: `mkdir build && cd build`
3. Compile: `cmake .. && make`
4. Run it: `./path_planning`.

Here is the data provided from the Simulator to the C++ Program

#### Main car's localization Data (No Noise)

["x"] The car's x position in map coordinates

["y"] The car's y position in map coordinates

["s"] The car's s position in frenet coordinates

["d"] The car's d position in frenet coordinates

["yaw"] The car's yaw angle in the map

["speed"] The car's speed in MPH

#### Previous path data given to the Planner

//Note: Return the previous list but with processed points removed, can be a nice tool to show how far along
the path has processed since last time. 

["previous_path_x"] The previous list of x points previously given to the simulator

["previous_path_y"] The previous list of y points previously given to the simulator

#### Previous path's end s and d values 

["end_path_s"] The previous list's last point's frenet s value

["end_path_d"] The previous list's last point's frenet d value

#### Sensor Fusion Data, a list of all other car's attributes on the same side of the road. (No Noise)

["sensor_fusion"] A 2d vector of cars and then that car's [car's unique ID, car's x position in map coordinates, car's y position in map coordinates, car's x velocity in m/s, car's y velocity in m/s, car's s position in frenet coordinates, car's d position in frenet coordinates. 

## Path Generation
This part is in line 104 - 268 in main.cpp. The main idea is to first choose a lane action, and then generate a smooth path trajectory using cubic splines. Details of two parts are explained in the following. To make it easier, we use Frenet Coordinates s and d. 
### Choose a lane and velocity
We use ref_lane to indicate our lane. The value is from 0 - 2.
If there is no car ahead, or the car is far from our car, then we just keep current lane and keep moving. To to this, we make "too_close" as fasle, and add a velocity .224 until 49.5.

If there is car ahead and it is very close (distance in Frenet Coordinates s < 30), we check if we can turn left or right. To do this, we enumerate all cars from sensor_fusion data, and compute their distance to our car in Frenet Coordinates.

If the car is in the left of our car, and the distance is less than 30, we set turn_left as false, which means we cannot trun left.  If the car is in the right of our car, and the distance is less than 30, we set turn_right as false.

If we are not in the 0 lane and can_left is ture, then --ref_lane.

If we are not in the 2 lane and can_right is ture, then ++ref_lane.

If it is too close, we also deduct the velocity with .224. 

#### the structure of this part is shown as:
'''cpp

          for(int i = 0; i< sensor_fusion.size(); ++i)
          {
            float d = sensor_fusion[i][6];
            double vx = sensor_fusion[i][3];
            double vy = sensor_fusion[i][4];
            double check_speed = sqrt(vx*vx + vy*vy);
            double check_car_s = sensor_fusion[i][5];

            check_car_s += ((double)prev_size * 0.02 * check_speed);

            if(d<(2+4*ref_lane + 2) && d>(2+4*ref_lane-2))
            {
             if((check_car_s > car_s) && ((check_car_s - car_s)< 30))
             {

                //ref_vel = 29.5;
                too_close = true;
                  // here we add some logic opeations for lane change to pass the car ahead
                /**************************************/
                for(int i = 0; i< sensor_fusion.size(); ++i)
                {
                  float d = sensor_fusion[i][6];
                  double vx = sensor_fusion[i][3];
                  double vy = sensor_fusion[i][4];
                  double check_speed = sqrt(vx*vx + vy*vy);
                  double check_car_s = sensor_fusion[i][5];

                  check_car_s += ((double)prev_size * 0.02 * check_speed);
                  if(ref_lane> 0 && d < (2+4*(ref_lane-1)+2) && d > (2+4*(ref_lane-1)-2)) // left lane
                  {
                    if(car_s - check_car_s < 30 && car_s - check_car_s > -30)
                    {
                      can_left = false;
                    }
                  }
                  if(ref_lane<2 && d < (2+4*(ref_lane+1)+2) && d > (2+4*(ref_lane+1)-2)) // left lane
                  {
                    if(car_s - check_car_s < 30 && car_s - check_car_s > -30)
                    {
                      can_right = false;
                    }
                  }
                }

                /**************************************/

                  if(ref_lane > 0 && can_left)
                  {
                    ref_lane -= 1;
                  }
                  else if(ref_lane < 2 && can_right)
                  {
                    ref_lane += 1;
                  }
                }
              }              
            }
'''

