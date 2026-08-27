import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image 
import numpy as np
from docking_vision.synthetic_target import create_target, SpacecraftState
from geometry_msgs.msg import Twist
import csv
from datetime import datetime
import os


class ImagePublisherNode(Node):
    def __init__(self):
        super().__init__('image_publisher_node')
        self.declare_parameter('kp', 0.1)
        self.kp = self.get_parameter('kp').value
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.declare_parameter('trial_id', 0)
        self.trial_id =self.get_parameter('trial_id').value
        self.image_publisher = self.create_publisher(Image, '/camera/image_raw', 10)
        self.create_subscription(Twist, '/cmd_vel', self.command_callback, 10)
        self.declare_parameter('initial_x', 80.0)
        self.initial_x = self.get_parameter('initial_x').value
        self.declare_parameter('initial_y', 50.0)
        self.initial_y = self.get_parameter('initial_y').value
        self.declare_parameter('initial_z', 2.0)
        self.initial_z = self.get_parameter('initial_z').value
        # freq = 1 / period
        # Want Freq = 10hz (10/sec), period = 0.1
        # self.create_timer(0.1, self.timer_callback)
        # 1/SEC
        self.declare_parameter('dt', 0.1)
        self.dt = self.get_parameter('dt').value
        # self.dt = 0.1
        self.create_timer(self.dt, self.timer_callback)

        self.summary_written = False
        # ==================================================
        # Initial condition
        # Change these values for each experiment
        # ==================================================
        # self.initial_x = 80.0
        # self.initial_y = 50.0
        # self.initial_z = 2.0

        # # Initial 2
        # self.initial_x = -80.0
        # self.initial_y = -50.0
        # self.initial_z = 2.0

        # # Initial 3
        # self.initial_x = 50.0
        # self.initial_y = -30.0
        # self.initial_z = 0.5

        # # Initial 4
        # self.initial_x = -100.0
        # self.initial_y = 70.0
        # self.initial_z = 1.5

        # Target position
        self.declare_parameter('target_x', 0.0)
        self.x_target = self.get_parameter('target_x').value
        self.declare_parameter('target_y', 0.0)
        self.y_target = self.get_parameter('target_y').value
        self.declare_parameter('target_z', 1.0)
        self.z_target = self.get_parameter('target_z').value

        # self.x_target = 0.0
        # self.y_target = 0.0
        # self.z_target = 1.0

        # Docking tolerance
        self.declare_parameter('tolerance_x', 1.0)
        self.tolerance_x = self.get_parameter('tolerance_x').value
        self.declare_parameter('tolerance_y', 1.0)
        self.tolerance_y = self.get_parameter('tolerance_y').value
        self.declare_parameter('tolerance_z', 0.05)
        self.tolerance_z = self.get_parameter('tolerance_z').value

        # self.tolerance_x = 1.0
        # self.tolerance_y = 1.0
        # self.tolerance_z = 0.05

        self.docking_success = False

        # ==================================================
        # State
        # ==================================================
        self.state = SpacecraftState(
            self.initial_x,
            self.initial_y,
            self.initial_z
        )

        # (80, 50, 2)
        # (-80, -50, 2)
        # (50, -30, 0.5)
        # (-100, 70, 1.5)

        self.command_x = 0.0
        self.command_y = 0.0
        self.command_z = 0.0
        
        self.history = []
        self.time = 0
        self.step = 0

        #Create csv File trajectory docking position and #Create csv experiment_summary
        trajectory_exists = os.path.exists('docking_position.csv')
        if trajectory_exists:
            #append
            self.csv_file = open('docking_position.csv', 'a', newline='')
            self.csv_writer = csv.writer(self.csv_file)
        else:
            #write
            self.csv_file = open('docking_position.csv', 'w', newline='')
            self.csv_writer = csv.writer(self.csv_file)
            self.csv_writer.writerow([
                'run_id',
                'trial_id',
                'kp',
                'time',
                'x',
                'y',
                'z',
                'error_x',
                'error_y',
                'error_z'
            ])

        summary_exists = os.path.exists('experiment_summary.csv')
        if summary_exists:
            #append
            self.exp_sum_file = open('experiment_summary.csv', 'a', newline='')
            self.exp_sum_writer = csv.writer(self.exp_sum_file)
        else:
            #write
            self.exp_sum_file = open('experiment_summary.csv', 'w', newline='')
            self.exp_sum_writer = csv.writer(self.exp_sum_file)
            self.exp_sum_writer.writerow([
                'run_id',
                'trial_id',
                'kp',
                'initial_x',
                'initial_y',
                'initial_z',
                'time_to_dock',
                'final_x',
                'final_y',
                'final_z',
                'success'
            ])

    def command_callback(self, msg):
        self.command_x = msg.linear.x
        self.command_y = msg.linear.y
        self.command_z = msg.linear.z

        print("Received command:")
        print(self.command_x, self.command_y, self.command_z)
        

    def timer_callback(self):
        if self.docking_success:
            return
    
        image_msg = Image()
        image = np.zeros((480, 640), dtype=np.uint8)

        # ==========================================
        # Update spacecraft state
        # ==========================================
        self.state.x += self.command_x * self.dt
        self.state.y += self.command_y * self.dt
        self.state.z += self.command_z * self.dt

        print("State x, y, z :", self.state.x, self.state.y, self.state.z)

        # ==========================================
        # Create synthetic image
        # ==========================================
        image_with_target = create_target(
            image,
            self.state
        )

        self.step +=1 
        self.time = self.step * self.dt

        # ==========================================
        # Calculate state error
        # ==========================================
        error_x = self.state.x - self.x_target
        error_y = self.state.y - self.y_target
        error_z = self.state.z - self.z_target


        # ==========================================
        # Check docking condition
        # ==========================================
        docked = (
            abs(error_x) <= self.tolerance_x
            and abs(error_y) <= self.tolerance_y
            and abs(error_z) <= self.tolerance_z
        )
        
        # ==========================================
        # Save trajectory
        # ==========================================
        self.history.append({
            "time": self.time,
            "x": self.state.x,
            "y": self.state.y,
            "z": self.state.z,
            "error_x": error_x,
            "error_y": error_y,
            "error_z": error_z
        })
        #Write history data to csv file and use this file to plot the graph
        self.csv_writer.writerow([
            self.run_id,
            self.trial_id,
            self.kp,
            self.time,
            self.state.x,
            self.state.y,
            self.state.z,
            error_x,
            error_y,
            error_z
        ])
        self.csv_file.flush()

        if(self.step % 10 == 0):
            print(self.history[-1])

        # ==========================================
        # Docking success
        # ==========================================
        if docked:
            self.docking_success = True

            self.exp_sum_writer.writerow([
                self.run_id,
                self.trial_id,
                self.kp,
                self.initial_x,
                self.initial_y,
                self.initial_z,
                self.time,
                self.state.x,
                self.state.y,
                self.state.z,
                True
            ])

            self.exp_sum_file.flush()
            self.summary_written = True

            print("================================")
            print("DOCKING SUCCESS")
            print("Time to dock:", self.time)
            print(
                "Final state:",
                self.state.x,
                self.state.y,
                self.state.z
            )
            print("================================")
            


        # print(len(image.tobytes()))
        # print(image.shape)
        # print(image.dtype)
        # print(image.size)
        # print(image.nbytes)
        data = image_with_target.tobytes()
        # print(type(data))
        # print(len(data))
        # print(data[:10])
        
        # ==========================================
        # Publish image
        # ==========================================
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
    try:
        rclpy.spin(node)
    finally:
        if (node.summary_written == False):
            node.exp_sum_writer.writerow([
                node.run_id,
                node.trial_id,
                node.kp,
                node.initial_x,
                node.initial_y,
                node.initial_z,
                node.time,
                node.state.x,
                node.state.y,
                node.state.z,
                False
            ])
            node.exp_sum_file.flush()
        
        node.csv_file.close()
        node.exp_sum_file.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__=='__main__':
    main()