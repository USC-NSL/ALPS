# ALPS
Public code repository for paper [ALPS]{https://nsl.cs.usc.edu/Papers?action=download&upname=Yitao16a.pdf}

## System requirements:
-Linux OS (Ubuntu 14.04 preferred) 
-Python 2.x
-OpenCV 2.4.x
-CUDA (if you want to accelerate with GPU)

## How to Use
1. Specify the detection aera in *config/query_area.info*. The first GPS is northwest corner and the second GPS is southeast corner.
2. Specify other attributes in *config/* files.
3. Run each python scripts one by one. Just use $python xx.py.
4. For step 06 and 08, please use [YOLO]{https://github.com/hyperchris/Yolo} for object detection.
5. The intermediate and final results will be stored in *data/*.
