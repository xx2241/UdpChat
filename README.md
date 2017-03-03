# UdpChat

### How to run this program   
#### 1. Server Mode   
python UdpChat.py -s &lt;port&gt;     
#### 2. Client Mode      
python UdpChat.py -c &lt;nick-name&gt; &lt;server-ip&gt; &lt;server-port&gt; &lt;client-port&gt;    

### Program Features   
#### 1. Registration   
1.1 client:
When the client run the program, the server will register the client in. It will also display a welcome message in the client side.

### Data Structure or algorithms       
1. Dictionary:




### Known bugs
1.
One of the prompt after sending message has an whitespace before it
2.
Instead of using multithreading in server mode, I set 0.7 second settimeout to detect the user's state when receive save message request, if another user send message within this 0.7 second the server won't receive. Since I assume this program support only small amounts of users, this bug has a very small chance to occur.


