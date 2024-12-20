import os
from glob import glob
from setuptools import setup

package_name = 'mail_delivery_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
   py_modules=["control.robot_driver", "control.state_machine", "perceptions.lidar_sensor", "control.action_translator", "perceptions.beacon_sensor", "navigation.captain", "navigation.map", "perceptions.bumper_sensor", "communication.client", "tools.csv_parser", "tools.nav_parser", "stubs.stub_sensor"],
    data_files=[
        # Include the CSV files.
        (os.path.join('lib', package_name, 'config'), glob(os.path.join('config', '*.csv'))),
        # Install marker file in the package index
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        # Include our package.xml file
        (os.path.join('share', package_name), ['package.xml']),
        # Include all launch files.
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bardia',
    maintainer_email='bardiaparmoun@gmail.com',
    description='An autonomous robot in charge of delivering mail across the Carleton University tunnels.',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_driver = control.robot_driver:main',
            'lidar_sensor = perceptions.lidar_sensor:main',
            'action_translator = control.action_translator:main',
            'beacon_sensor = perceptions.beacon_sensor:main',
            'captain = navigation.captain:main',
            'bumper_sensor = perceptions.bumper_sensor:main',
            'client = communication.client:main',
            'stub_sensor = stubs.stub_sensor:main'
        ],
    },
)
