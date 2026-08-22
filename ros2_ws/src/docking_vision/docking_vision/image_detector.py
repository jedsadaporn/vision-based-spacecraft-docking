import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image 
import numpy as np
from cv_bridge import CvBridge
import cv2
from docking_vision.target_detector import detect_target

class ImageDetectorNode(Node):
    def __init__(self):
        super().__init__('image_detector_node')
        self.create_subscription(Image, '/camera/image_raw',self.image_callback, 10)
        # 1/SEC
        # self.create_timer(1, self.timer_callback)
        self.bridge = CvBridge()

    def image_callback(self, msg):
        # print(msg)
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono8')
        # cv2.imshow('Binary Image', cv_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        print("Received Image")
        print("shape: ", cv_image.shape)
        result = detect_target(cv_image)
        if result is None:
            print("Target Not Found")
        else:
            cx, cy = result
            print("Target:", cx, cy)

def main(args=None):
    rclpy.init(args=args)
    node = ImageDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()