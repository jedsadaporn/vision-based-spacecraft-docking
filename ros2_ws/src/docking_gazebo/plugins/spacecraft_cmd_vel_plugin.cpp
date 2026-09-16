#include <iostream>
#include <rclcpp/rclcpp.hpp>
#include <gazebo/common/Plugin.hh>
#include <gazebo/physics/physics.hh>
#include <geometry_msgs/msg/twist.hpp>
#include <gazebo_ros/node.hpp>
#include <boost/bind.hpp>

class SpacecraftCmdVelPlugin : public gazebo::ModelPlugin
{

public:
    void Load(
        gazebo::physics::ModelPtr model,
        sdf::ElementPtr sdf)
    {
        // 1. model
        model_ = model;

        std::cerr << "=== SpacecraftCmdVelPlugin: Load() called ===" << std::endl;
        // 2. ROS node
        node_ = gazebo_ros::Node::Get(sdf);
        RCLCPP_INFO(node_->get_logger(), "SpacecraftCmdVelPlugin loaded");

         subscription_ = node_->create_subscription<geometry_msgs::msg::Twist>(
            "/cmd_vel", 
            10, 
            std::bind(&SpacecraftCmdVelPlugin::OnCmdVel, this, std::placeholders::_1)
        );

        // 3. Gazebo update callback
        update_connection_ = 
            gazebo::event::Events::ConnectWorldUpdateBegin(
                boost::bind(
                    &SpacecraftCmdVelPlugin::OnUpdate,
                    this
                )
            );
    }

private:
    void OnCmdVel(const geometry_msgs::msg::Twist::SharedPtr msg)
    {
        vx_ = msg->linear.x;
        vy_ = msg->linear.y;
        vz_ = msg->linear.z;
    }
    void OnUpdate()
    {
        model_->SetLinearVel(
        ignition::math::Vector3d(
            vz_,   // Gazebo X ← controller Z
            vx_,   // Gazebo Y ← controller X
            vy_    // Gazebo Z ← controller Y
        )
    );
    }
    // 1. Gazebo
    gazebo::physics::ModelPtr model_;

    // 2. ROS
    gazebo_ros::Node::SharedPtr node_;
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr subscription_;

    // 3. Latest command
    double vx_ = 0.0;
    double vy_ = 0.0;
    double vz_ = 0.0;

    // 4. Gazebo update
    gazebo::event::ConnectionPtr update_connection_;
};

// Tell Gazebo to create from this class
GZ_REGISTER_MODEL_PLUGIN(SpacecraftCmdVelPlugin)