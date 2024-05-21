# Protocol Constants

CMD_FIELD_LENGTH = 16# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg": "LOGIN",
"logout_msg": "LOGOUT",
"logged_msg": "LOGGED",
"getquestion_msg": "GET_QUESTION",
"sendanswer_msg": "SEND_ANSWER",
"myscore_msg": "MY_SCORE",
"highscore_msg": "HIGHSCORE"
}


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR",
"score_msg" : "YOUR_SCORE"
} # ..  Add more commands if needed


# Other constants
ERROR_RETURN = None  # What is returned in case of an error

"""
Gets command name (str) and data field (str) and creates a valid protocol message
Returns: str, or None if error occured
"""

# valid_cmd = ('LOGIN', 'LOGOUT', 'LOGGED', 'GET_QUESTION', 'SEND_ANSWER', 'MY_SCORE', 'HIGHSCORE')
def build_message(cmd, data):
	if cmd in PROTOCOL_CLIENT.values():
		spaces = (CMD_FIELD_LENGTH - len(cmd)) * ' '
		data_length = f"{len(data):04d}"
		if cmd != PROTOCOL_CLIENT['login_msg']:
			full_msg = f"{cmd}{spaces}{DELIMITER}{data_length}{DELIMITER}{data}"

		elif cmd == PROTOCOL_CLIENT['login_msg']:
			splitted_data = split_data(data, 1)
			login_data = join_data(splitted_data)
			full_msg = f"{cmd}{spaces}{DELIMITER}{data_length}{DELIMITER}{login_data}"

		print("Final Message in build_message:", full_msg)
		return full_msg

	else:
		return ERROR_RETURN


"""
Parses protocol message and returns command name and data field
Returns: cmd (str), data (str). If some error occured, returns None, None
"""
def parse_message(data):
	split_message = data.split(DELIMITER)
	if len(split_message) != 3:
		print('1')
		return None, None
	cmd = split_message[0].strip().upper()
	if cmd not in PROTOCOL_SERVER.values():
		print('2')
		return None, None
	data_length_str = split_message[1].strip()
	msg = split_message[2]
	try:
		if len(msg) != int(data_length_str):
			print('3')
			return None, None
	except Exception as E:
		print('4')
		return None, None

	return cmd, msg




def split_data(msg: str, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
	splitted_msg_lst = msg.split(DATA_DELIMITER)
	msg_deli_cnt = msg.count('#')
	if expected_fields == msg_deli_cnt:
		return splitted_msg_lst
	else:
		return [ERROR_RETURN]


def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
	Returns: string that looks like cell1#cell2#cell3
	"""
	msg_field_converted = [str(var) for var in msg_fields]
	joined_lst = DATA_DELIMITER.join(msg_field_converted)
	return joined_lst

