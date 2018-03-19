# GulliView Socket Server

This socket server listens for tag data captured by the GulliView cameras. Clients connected to this server only receives
position data from the tags they to subscribe to. It also allows for multiple clients to be connected. 

## Prerequisites
You need numpy installed on the machine running this server.

```
pip install numpy
```

## Installation
The first step is to start the GulliView server. 

Connect to the GulliView server and start the cameras. The ip address should be to the machine you're running 
this socket server.

```
ssh 192.168.1.136 -X -l bachelor
cd repository/visionlocalization_old/build/
bash ./startCameras.sh 192.168.1.XXX
```

Place `socketserver.py` on the computer you want to run the socket server. 
Start the server with the following command:

```
python socketserver.py 192.168.1.XXX
```
 
The server prompts you to add clients which will receive the GulliView data.

* **Ros Master Ip** - Ip address to the computer running the car's ros master
* **Back / Front tag id** - The id's of the GulliView tags placed on the car


Below is an example of adding a car which ros master is running on 192.1.168.125 
with the GulliView tags 4 and 5 on the truck.

```
Enter ROS Master Ip: 192.1.168.125
Enter the back tag ID: 4
Enter the front tag ID: 5
```

## Errors

If you get this error:

```
socket.error: [Errno 49] Can't assign requested address
```

Then you're probably not connected to the correct network.