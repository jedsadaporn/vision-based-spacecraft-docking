import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image 
import numpy as np
from cv_bridge import CvBridge
import cv2
from docking_vision.target_detector import detect_target
from docking_vision.controller import control
from geometry_msgs.msg import Twist

class ImageDetectorNode(Node):
    def __init__(self):
        super().__init__('image_detector_node')
        self.create_subscription(Image, '/camera/image_raw',self.image_callback, 10)
        self.cmd_pub = self.create_publisher(Twist,'/cmd_vel', 10)
        # 1/SEC
        self.dt = 0.1
        self.create_timer(self.dt, self.timer_callback)
        self.bridge = CvBridge()
        self.command_x = 0.0
        self.command_y = 0.0
        self.command_z = 0.0
        self.docking_success = False

    def timer_callback(self):
        if self.docking_success:
            return
        
        msg = Twist()
        msg.linear.x = float(self.command_x)
        msg.linear.y = float(self.command_y)
        msg.linear.z = float(self.command_z)

        self.cmd_pub.publish(msg)

    def image_callback(self, msg):
        # print(msg)
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono8')
        # image = cv2.imread(cv_image,cv2.IMREAD_GRAYSCALE)
        cv2.imshow('Binary Image', cv_image)
        
        print("Received Image")
        print("shape: ", cv_image.shape)
        result = detect_target(cv_image)
        if result is None:
            print("Target Not Found")
        else:
            cx, cy, z = result
            print("Target:", cx, cy, z)
            error_x = cx - 320
            error_y = cy - 240
            error_z = z - 1.0
            self.command_x, self.command_y, self.command_z = control(error_x, error_y, error_z)
            tolerance_x = 5.0      # pixels
            tolerance_y = 5.0      # pixels
            tolerance_z = 0.05     # estimated distance
            if abs(error_z) < tolerance_z and abs(error_x) < tolerance_x and abs(error_y) < tolerance_y:
                self.command_z = 0.0
                self.command_x = 0.0
                self.command_y = 0.0
                self.docking_success = True
                print("SPACE DOCKING SUCCESS")
            print("Target:", cx, cy, z)

            print(
                "Error:",
                error_x,
                error_y,
                error_z
            )

            print(
                "Command:",
                self.command_x,
                self.command_y,
                self.command_z
            )
 
        #wait for key everytime callback not compactable with ros2
        # cv2.waitKey(0)
        #Open window
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = ImageDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()