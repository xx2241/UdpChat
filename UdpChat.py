import socket
import sys
import json
import time
from time import localtime, strftime
from threading import Thread

class MyException(Exception): pass

def servermode():
	def broadcast(message):
		for name, data in server_dict.items():
			if data[1]==True:
				s.sendto(json.dumps(message),data[0])
		sys.stdout.flush()

	try:
		try:
			server_port = int(sys.argv[2])
		except: 
			raise MyException("port number should be integer")
		if server_port<1024 or server_port>65536: 
			raise MyException('Invalid port number')
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.bind(('',server_port))
		print(">>> server start " + str(socket.gethostbyname(socket.gethostname())))
		sys.stdout.flush()

		server_dict = dict()
		message_dict = dict()

		while True:
			data = None
			clientaddress = None
			data, clientaddress = s.recvfrom(server_port)
			print(">>> receive message")
			try:
				message = json.loads(data)				
			except:
				raise MyException('>>> not json data type')
			print('splitting message')
			tag = message['tag']
			print(tag)
			
			if tag == 'first_reg':
				nick_name = message['info']
				print('tag correct: first_reg')
				if nick_name in server_dict:
					print('nickname in dict')
					try:
						s.sendto(json.dumps({'tag':"first_reg_fail",'info':'fail'}),clientaddress)
						print(">>> send message")
					except:
						print('>>> message sending problem')
						raise MyException('>>> problem with sending data to client')
				else:
					print('register a new user')
					server_dict[nick_name] = (clientaddress, True)
					s.sendto(json.dumps({'tag':"first_reg_succeed",'info':'success'}),clientaddress)
					time.sleep(0.01)
					broadcast({'tag':"client_dict", 'info':server_dict})
			elif tag == 'dereg':
				nick_name = message['info']
				print('tag is dereg')	
				server_dict[nick_name] = (clientaddress, False)
				print('update the server_dict')
				s.sendto(json.dumps({'tag':'ACK1','info':'dereg'}),clientaddress)
				print('send ACK1 dereg back')
				broadcast({'tag':"client_dict", 'info':server_dict})
				print('broadcast')
			elif tag == 'reg':
				print('tag is reg')
				nick_name = message['info']
				server_dict[nick_name] = (clientaddress,True)
				broadcast({'tag':"client_dict", 'info':server_dict})
				print('update the server_dict')
				s.sendto(json.dumps({'tag':'ACK1','info':'reg'}),clientaddress)
				print('send ACK1 back')
				time.sleep(0.1)
				print(nick_name)
				if nick_name in message_dict:
					print('nick_name in dict...')
					s.sendto(json.dumps({'tag':'offlinechat','info':message_dict[nick_name]}),clientaddress)
					del message_dict[nick_name]
					print('finish senindg offline message....')
			elif tag == 'offlinechat':
				print('offlinechat.....')
				print(message['info'])
				nick_name, target_name, offlinemessage = message['info']
				if target_name in message_dict:
					print('name in dict...')
					message_dict[target_name].append([nick_name,offlinemessage,strftime("%a, %d %b %Y %H:%M:%S ", localtime())])
				else:
					print('name not in dict...')
					message_dict[target_name] = [nick_name,offlinemessage,strftime("%a, %d %b %Y %H:%M:%S ", localtime())]
				print(message_dict)
				s.sendto(json.dumps({'tag':'ACK0','info':"ACK0"}),clientaddress)

			else:
				raise MyException('>>> invalid tag')
	except KeyboardInterrupt:
		raise KeyboardInterrupt
	except:
		raise MyException('server down')
		sys.exit(0)



def clientmode():
	def send(client_dict,acklist,nick_name):
		while True:
			data = None		
			try:
				data = raw_input().split()
				print('>>> ')
				sys.stdout.flush()
				if client_dict[nick_name][1]==False:
					print('>>> you are offline')
					if len(data)==2 and data[0]=='reg':
						if data[1] == nick_name:
							print('nick_name_valid...')
							acklist[1]=False
							for i in range(0,5):
								print('waiting for ack1...')
								s.sendto(json.dumps({'tag':'reg','info':nick_name}),serveraddress)
								if acklist[1]==True:
									acklist[1]=False
									client_dict[nick_name][1]=True
									print('>>> you are online again')
									break
								time.sleep(0.5)
								if i==4:
									print(">>> [Server not responding]")
									break
					continue
				if len(data)==2:
					if data[0]=='dereg':
						print('dereging....')
						if data[1] == nick_name:
							print('nick_name_valid...')
							acklist[1]=False
							client_dict[nick_name][1]=False
							for i in range(0,5):
								print('waiting for ack')
								if acklist[1]:
									acklist[1]=False
									print('>>> successfully dereg')
									break
								s.sendto(json.dumps({'tag':'dereg','info':nick_name}),serveraddress)
								time.sleep(0.5)
								if i==4:
									print('>>> [server not responding]')
									print('>>> [Exiting]')
									break
						else:
							print(data[1])
							print(nick_name)
							print('>>> you can dereg other user')
							continue
					if client_dict[nick_name][1]==False:
						print(">>> [You are offline, Bye.]")
						continue
					else:
						print('>>> invalid input')

				elif len(data)==3:
					if data[0]=='send':
						name = data[1]
						if name in client_dict:
							if client_dict[name][1]==True:
								acklist[0]=False
								for i in range(0,2):
									if i == 1 and acklist[0] == True:
										acklist[0]=False
										print(">>> [Message received by "+name+"]")
										break
									if i == 1 and acklist[0] == False:
										print('No ACK from ' +name+', message sent to server.')
										for i in range(0,2):
											if i==1 and acklist[0]== True:
												acklist[0]=False
												print('>>> offline message received by server')
												break
											if i==1 and acklist[0]==False:
												print('>>> server not received the message')
												break
											s.sendto(json.dumps({'tag':'offlinechat','info':(nick_name,name,data[2])}),serveraddress)
											time.sleep(0.5)
										break
									print('sending chat....')
									s.sendto(json.dumps({'tag':'chat','info':data[2]}),tuple(client_dict[name][0]))
									print('finish sending chat...')
									time.sleep(0.5)
							else:
								acklist[0]=False
								for i in range(0,2):
									if i==1 and acklist[0]==True:
										acklist[0]=False
										print('>>> [Messages received by the server and saved]')
										break
									if i==1 and acklist[0]==False:
										print('>>> server not received the message')
										break
									s.sendto(json.dumps({'tag':'offlinechat','info':(nick_name,name,data[2])}),serveraddress)
									time.sleep(0.5)


						else:
							print('>>> invalid user name')
									
				else:
					print('>>> invalid input')
			except Exception as x:
				print('>>> '+str(x))

	def receive(client_dict,acklist,nick_name):
		try:
			while True:	
				data = None
				addr = None
				try:
					data, addr = s.recvfrom(client_port)
				except socket.error:
					continue
				try:
					message = json.loads(data)			
				except:
					raise MyException('not json data type')
				print(message)
				tag = message['tag']
				info = message['info']
				if tag == 'client_dict':
					client_dict.update(info)
					print(">>> [Client table updated.]")
					print(">>> "+str(client_dict))
				elif tag == 'ACK1':
					acklist[1] = True
				elif tag == 'ACK0':
					acklist[0] = True
				elif tag == 'chat':
					s.sendto(json.dumps({'tag':'ACK0','info':'ACK0'}),addr)
					print('>>> '+ info)
				elif tag == 'offlinechat':
					time.sleep(0.5)
					print('>>> '+str(info))
				else:
					print('>>> invalid tag')
		except:
			raise 
			




	try:
		nick_name, server_ip, server_port, client_port = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
		try:
			serveraddress = (server_ip, int(server_port))
			client_port = int(client_port)
		except:
			raise MyException("port number should be integer")
		if client_port<1024 or client_port>65536: 
			raise MyException('Invalid port number')
		client_dict = dict()
		acklist = [False, False]
		###{name: addr, onlinestate}
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.bind(('',client_port))
		s.sendto(json.dumps({'tag': 'first_reg', 'info':nick_name}),serveraddress)
		data = None
		addr = None
		s.settimeout(3)
		data, addr = s.recvfrom(client_port)
		data = json.loads(data)
		if data['tag'] == 'first_reg_fail':
			print(">>> [user name already exist.]")
		elif data['tag'] == "first_reg_succeed":
			print(">>> [Welcome, You are registered.]")
			#client_dict.update(data['info'])
			
			####multithread
			t1 = Thread(target=send,args=(client_dict,acklist,nick_name))
			t2 = Thread(target=receive,args=(client_dict,acklist,nick_name))
			t1.setDaemon(True)
			t2.setDaemon(True)	
			t1.start()
			t2.start()
			while 1:
				pass
		else:
			raise MyException("invalid tag"+data['tag'])
		

	except KeyboardInterrupt:
		raise KeyboardInterrupt

	except Exception as x:
		print(">>>"+str(x))
	finally:
		sys.exit()



if __name__ == '__main__':

	 try:
	 	if len(sys.argv) == 3 and sys.argv[1]=='-s':
	 		servermode()	 		
	 	elif len(sys.argv) == 6 and sys.argv[1] == '-c':
	 		clientmode()	 		
	 	else:
	 		raise MyException("please input as the following format:\n>>> python <filename> -c <nick_name> <server_ip> <server_port> <client_port>\n>>> usage: python Client.py -s <server-port>")
	 except KeyboardInterrupt: 
	 	print(">>> Bye")
	 	raise KeyboardInterrupt
	 	sys.exit()
	 
	 except Exception as x: print(">>> "+str(x))
	 
	 finally: 
	 	sys.exit()

