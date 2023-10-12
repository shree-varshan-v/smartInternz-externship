#!/usr/bin/env python3
from __future__ import print_function # package used to import print function

import roslib # contains common data structures
import sys # system module
import rospy #python client library for ROS
import cv2 # opencv module 
import numpy as np # numerical array package 
from std_msgs.msg import String  #representing primitive data types and other basic message constructs
from sensor_msgs.msg import Image # #package for Camera module integrated with robot
from cv_bridge import CvBridge, CvBridgeError # package to convert opencv image into ros supporting image
print(sys.version)
#specify the location of the files in the code
net = cv2.dnn.readNet("/home/sv/project_ws/src/mybot_motion/scripts/yolov3.weights", "/home/sv/ros_work/src/mybot_motion/scripts/yolov3.cfg") 
classes = []
#specify the location of the files in the code
with open("/home/sv/project_ws/src/mybot_motion/scripts/yolov3.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

class image_converter: # main class

  def __init__(self):  # init method
    self.image_pub = rospy.Publisher("mybot/camera/face",Image,queue_size=10)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("mybot/camera/image_raw",Image,self.callback)
 
  #def upl(self,cv,image):
    #s3.meta.client.upload_file(cv, 'gnaneshwarb', image) 
  
  def callback(self,data): #call_back method
    try:
      img = self.bridge.imgmsg_to_cv2(data, "bgr8")
      print(img)
    except CvBridgeError as e:
      print(e)
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
      for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
        # Object detected
          center_x = int(detection[0] * width)
          center_y = int(detection[1] * height)
          w = int(detection[2] * width)
          h = int(detection[3] * height)
            
          # Rectangle coordinates
          x = int(center_x - w / 2)
          y = int(center_y - h / 2)

          boxes.append([x, y, w, h])
          confidences.append(float(confidence))
          class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_DUPLEX
    for i in range(len(boxes)):
      if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[i]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, label, (x, y - 5), font, 0.8, color, 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    try:
        self.image_pub.publish(self.bridge.cv2_to_imgmsg(img, "bgr8"))
    except CvBridgeError as e:
        print(e)
        
def main(args): #main function
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)