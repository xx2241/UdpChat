# UdpChat

## How to use this project      
#### 1. Server Mode   
##### 1.1 run program    
python UdpChat.py -s &lt;port&gt;   
##### 2.1 stop program    
ctrl + c
#### 2. Client Mode      
##### 2.1 run program    
python UdpChat.py -c &lt;nick-name&gt; &lt;server-ip&gt; &lt;server-port&gt; &lt;client-port&gt;    
##### 2.2 send message    
send &lt;target-nick-name&gt; &lt;message&gt;      
##### 2.3 deregistration     
dereg &lt;nick-name&gt;   
##### 2.4 registration again after deregistration    
reg &lt;nick-name&gt;  
##### 2.3 stop program   
ctrl + c

## Program Features     
#### 1. Run program    
##### 1.1 Client    
If client can communicate with server, it will perform registration.    
If client can't communicate with server, it will raise a timeout error and exit.   
##### 1.2 Server    
The server will start and listen to upcoming message     
#### 2. Registration        
##### 2.1 Client      
When the client run the program, the server will register the client in.    
It will also display a welcome message in the client side.   
The client dictionary will be update.         
##### 2.2 Server   
Server will update the client dictionary.
Server will broadcast the client dictionary to all active client.  
#### 3. Online-Chat    
##### Online chat is client to client directly.
Client can send message to another active client.   
Client can receive message from another active client.   
After the target client receive the message it will display a message indicating that the message has been received.   
If the client not respond it will send to the server and it will display a message indicating that the message has been send to server.    
#### 4. De-registering   
##### 4.1 Client   
Client can deregister.     
Deregistered client can't hear from other clients' online chat and other message.   
After deregistering, the client can register again, other input information is all invalid.    
##### 4.2 Server   
Server will update the client dictionary and broadcast to all active users when a user de-register.   
Server will update the client dictionary and broadcast to all active users when a user re-register.   
#### 5. Offline-Chat    
##### 5.1 Client   
When the recipient or end-client is offline in its local-table of clients, client will send offline-chat to the server.  
When there is a time-out on a message sent to a client, client will send offline-chat to the server.     
When a de-registered client login back it will display the offline message for him.   
##### 5.2 Server   
Server maintains a dictionary to store the offline message for different users.    
When a server receives a save-message request from a client it has to check for the status of the intended recipient.    
If the recipient client is still active, send an error message back to the source client and update its client dictionary.    
If the recipient client is not active and it is different from server's table, then the server should change the status of the appropriate client to offline, and broadcast to all active users.    

## Data Structure or algorithms       
##### 1. Dictionary        
1.1 A dictionary to maintain the information of user registration in both client side and server side. It use clients' name as key and a tuple of clients' address and active status as value.    
1.2 A dictionary to maintain the information of user's offfline message in server side. The key is clients' name and the value is the offlinemessages.       
1.3 Message in every communication is a dictionary. This dictionary contains key 'tag' for the receiver to identify the type of message and contains key 'info' for actual message it want to send.   
##### 2. Multithreading  
In client mode, I use two threads simultaneously. One is for receiving message, the other is for sending message. The two threads share information about client dictionary and acklist. Client dictionary will only be update by "receive" thread, the acklist can be update by both threads but the updating can never be simultaneously.

## Known bugs
1. One of the prompt after sending message has an whitespace before it   
2. When receive save message request, instead of using multithreading in server mode, for convenience I set 0.7 second settimeout to detect the user's state, if another user send message within this 0.7 second the server won't receive it. Since I assume this program support only small amounts of users, this bug has a very small chance to occur.


