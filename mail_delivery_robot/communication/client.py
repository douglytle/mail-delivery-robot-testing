import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import requests
import json

from tools.csv_parser import loadConfig

class Client(Node):
    '''
    The Node in charge of communicating to the webapp.

    @Subscribers:
    - Listens to /updates for any logs to share with the web app.

    @Publishers:
    - Publishes new trip information to /trips.
    '''
    def __init__(self):
        '''
        The constructor for the node.
        Defines the necessary publishers and subscribers.
        '''
        super().__init__('client')
        
        # Load the global config.
        self.config = loadConfig()

        # Get the model of the robot.
        self.declare_parameter('robot_model', 'CREATE_2')
        self.robot_model = self.get_parameter('robot_model').get_parameter_value().string_value

        # The current trip
        self.currentTrip = ""

        # The publishers for the node.
        self.tripPublisher = self.create_publisher(String, 'trips', 10)

        # The subscribers for the node.
        self.updateSubscriber = self.create_subscription(String, 'update', self.handleUpdate, 10)

        # The timer to check for new requests with the web app.
        self.request_timer = self.create_timer(self.config["CLIENT_REQUEST_TIMER"], self.sendRequest)

        # The timer to check if the system needs to be killed.
        self.kill_timer = self.create_timer(self.config["CLIENT_KILL_TIMER"], self.killSystem)
    
    def handleUpdate(self, data):
        '''
        The callback for /update.

        @param data: the new update data.
        '''
        update_data = data.data
        self.get_logger().info("Got a new updated: " + update_data)

        url = 'https://cudelivery.azurewebsites.net/api/v1/updateStatus/' + self.currentTrip
        post_data = {"status": update_data}

        try:
            x = requests.post(url, json = post_data)
            #self.get_logger().info(x.text)
        except:
            self.get_logger().info("ERROR: FAILED TO CONNECT TO THE WEBSITE.")
    
    def sendRequest(self):
        '''
        The callback for the requests timer.
        '''
        if self.currentTrip == "":
            url = "https://cudelivery.azurewebsites.net/api/v1/getRobotDeliveries/" + self.robot_model
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    r = json.loads(res.text)

                    # Get a new trip once you are done.
                    if len(r) != 0:
                        for k in r:
                            trip = r[k]["sourceDest"]+":"+r[k]["finalDest"]
                            self.currentTrip = k
                            break

                        tripMessage = String()
                        tripMessage.data = trip 
                        self.tripPublisher.publish(tripMessage)
                        self.get_logger().info("Got a new request: " + trip)
                else:
                    self.get_logger().info("ERROR: Failed to get an update.")
            except:
                self.get_logger().info("ERROR: FAILED TO CONNECT TO THE WEBSITE.")

    def killSystem(self):
        '''
        Checks to see if the system needs to be killed.
        '''
        url = "https://cudelivery.azurewebsites.net/api/v1/killRobot/" + self.robot_model
        try:
            res = requests.get(url)
            if res.status_code == 200:
                r = json.loads(res.text)

                if len(r) != 0:
                    if r["kill"]:
                        # Attempts to kill the system.
                        nodes = ["sllidar_node", "action_translator", "robot_driver", "captain", "client", "lidar_sensor", "beacon_sensor", "bumper_sensor"]
                        if self.robot_model != "CREATE_3":
                            nodes.append("create_driver")

                        for node in nodes:
                            os.system('killall ' + node)
            else:
                self.get_logger().info("ERROR: Failed to get a kill update.")
        except:
            self.get_logger().info("ERROR: FAILED TO CONNECT TO THE WEBSITE")
        
def main():
    '''
    Starts up the node. 
    '''
    rclpy.init()
    client = Client()
    rclpy.spin(client)


if __name__ == '__main__':
    main()
