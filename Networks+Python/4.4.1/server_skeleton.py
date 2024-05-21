##############################################################################
# server.py
##############################################################################

import socket
import chatlib

# GLOBALS
users = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]}
			}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
	"""
	 Builds a new message using chatlib, wanted code and message.
	 Prints debug info, then sends it to the given socket.
	 Paramaters: conn (socket object), code (str), data (str)
	 Returns: Nothing
	 """
	final_msg = chatlib.build_message(code, msg)
	# print(f"final_msg: {final_msg}")
	conn.send(final_msg.encode())
	print("[SERVER] ",final_msg)	  # Debug print

def recv_message_and_parse(conn):
	full_msg = conn.recv(1024).decode()
	# print(f"Full message received: {full_msg}")  # Added print statement
	try:
		cmd, msg = chatlib.parse_message(full_msg)
		# print(f"code: {cmd}")      # Check what `code` is after parsing
		# print(f"data: {msg}")      # Check what `data` is after parsing
		# print(cmd, msg)
		return cmd, msg

	finally:
		print("[CLIENT] ",full_msg)	  # Debug print
	


# Data Loaders #

def load_questions():
	"""
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: questions dictionary
	"""
	questions = {
				2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
				4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3} 
				}
	
	return questions

def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""
	users = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]}
			}
	return users

	
# SOCKET CREATOR

def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (SERVER_IP, SERVER_PORT)
	print("starting up on {} port {}".format(*server_address))
	sock.bind(server_address)
	sock.listen(1)
	return sock



		
def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	build_and_send_message(conn, 'ERROR', error_msg)
	


	
##### MESSAGE HANDLING


def handle_getscore_message(conn, username):
	global users
	# Implement this in later chapters

	
def handle_logout_message(conn):
	"""
	Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
	Receives: socket
	Returns: None
	"""
	global logged_users
	build_and_send_message(conn, 'LOGOUT', '')

	


def handle_login_message(conn, data):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Receives: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  # This is needed to access the same users dictionary from all functions
	global logged_users	 # To be used later
	# cmd, msg = recv_message_and_parse(conn)
	# if cmd == 'LOGIN':
	try:
		username, password = chatlib.split_data(data, 1)
		if username in users.values() and users[username]['password'] == password:
			build_and_send_message(conn, 'LOGIN_OK', '')
	except:
		send_error(conn, "Invalid login information")


def handle_client_message(conn, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Receives: socket, message code and data
	Returns: None
	"""
	global logged_users	 # To be used later
	if cmd == 'LOGIN':
		handle_login_message(conn, data)


	


def main():
	# Initializes global users and questions dicionaries using load functions, will be used later
	global users
	global questions
	
	print("Welcome to Trivia Server!")
	
	# Implement code ...



if __name__ == '__main__':
	main()

	