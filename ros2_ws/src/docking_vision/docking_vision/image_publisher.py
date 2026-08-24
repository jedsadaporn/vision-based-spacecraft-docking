import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image 
import numpy as np
from docking_vision.synthetic_target import create_target, SpacecraftState
from geometry_msgs.msg import Twist


class ImagePublisherNode(Node):
    def __init__(self):
        super().__init__('image_publisher_node')
        self.image_publisher = self.create_publisher(Image, '/camera/image_raw', 10)
        self.create_subscription(Twist, '/cmd_vel', self.command_callback, 10)
        # freq = 1 / period
        # Want Freq = 10hz (10/sec), period = 0.1
        # self.create_timer(0.1, self.timer_callback)
        # 1/SEC
        self.dt = 0.1
        self.create_timer(self.dt, self.timer_callback)
        self.command_x = 0.0
        self.command_y = 0.0
        self.command_z = 0.0
        self.state = SpacecraftState(-80, -50, 2)
        # (80, 50, 2)
        # (-80, -50, 2)
        # (50, -30, 0.5)
        # (-100, 70, 1.5)

    def command_callback(self, msg):
        self.command_x = msg.linear.x
        self.command_y = msg.linear.y
        self.command_z = msg.linear.z

        print("Received command:")
        print(self.command_x, self.command_y, self.command_z)
        

    def timer_callback(self):
        image_msg = Image()
        image = np.zeros((480, 640), dtype=np.uint8)
        self.state.x += self.command_x * self.dt
        self.state.y += self.command_y * self.dt
        self.state.z += self.command_z * self.dt
        print("State x, y, z :", self.state.x, self.state.y, self.state.z)
        image_with_target = create_target(image,self.state)
        # print(len(image.tobytes()))
        # print(image.shape)
        # print(image.dtype)
        # print(image.size)
        # print(image.nbytes)
        data = image_with_target.tobytes()
        # print(type(data))
        # print(len(data))
        # print(data[:10])
        
        image_msg.height = 480
        image_msg.width = 640
        #string encoding       # Encoding of pixels -- channel meaning, ordering, size
                                # taken from the list of strings in include/sensor_msgs/image_encodings.hpp
        image_msg.encoding = 'mono8'
        #uint32 step           # Full row length in bytes
        #Maybe Grayscale/Monochrome BPP = 1 , step = 640*1
        BPP = 1
        image_msg.step = image_msg.width * BPP
        #uint8[] data   actual matrix data, size is (step * rows) , rows is height
        #data = step * row = 640 * 480 = 307200
        # image_msg.data = image_msg.step * image_msg.height
        
        image_msg.data = data
        image_msg.is_bigendian = 0
        # print(image_msg.height)
        # print(image_msg.width)
        # print(image_msg.encoding)
        # print(len(image_msg.data))
        # print(image_msg.is_bigendian)
        self.image_publisher.publish(image_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisherNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()