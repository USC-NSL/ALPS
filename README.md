# ALPS
Public code repository for paper [ALPS](https://nsl.cs.usc.edu/Papers?action=download&upname=Yitao16a.pdf)

## System requirements:
-Linux OS (Ubuntu 14.04 preferred) 
-Python 2.x
-OpenCV 2.4.x
-CUDA (if you want to accelerate with GPU)
-selenium for python

## How to Use
1. Specify the detection aera in *config/query_area.info*. The first GPS is southwest corner and the second GPS is northeast corner.
2. Specify other attributes in *config/* files.
3. Run each python scripts one by one. Just use $python xx.py.
4. For step 06 and 08, please use [YOLO](https://github.com/hyperchris/Yolo) for object detection. The input images can be found in *data/*.
5. The intermediate and final results will be stored in *data/*.

## FAQ
1. The image downloading process (05 and 07) sometimes failed. What can I do?

Google may break the link randomly (maybe due to security concern?). So you should mannually restart the script after updating the parameters in code with most recent downloaded image's filename. 

2. How to train ALPS to detect more objects? 

See [YOLO](https://github.com/hyperchris/Yolo).
