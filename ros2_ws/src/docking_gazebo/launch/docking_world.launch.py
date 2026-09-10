from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    
    set_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value = PathJoinSubstitution([
                    FindPackageShare('docking_gazebo'),
                    'models'
                ])
    )

    gazebo = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('gazebo_ros'),
                    'launch',
                    'gazebo.launch.py'
                ])
            ),
            launch_arguments={
                'world': PathJoinSubstitution([
                    FindPackageShare('docking_gazebo'),
                    'worlds',
                    'docking_world.world'
                ]),
            }.items()
        )

    return LaunchDescription([
        set_model_path,
        gazebo
    ])
