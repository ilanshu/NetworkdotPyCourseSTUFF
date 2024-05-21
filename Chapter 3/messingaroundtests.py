

"""
Helper method. gets a string and number of expected fields in it. Splits the string 
using protocol's data field delimiter (|#) and validates that there are correct number of fields.
Returns: list of fields if all ok. If some error occured, returns None
# """
# def split_data(msg: str, expected_fields: int):
#     splitted_msg_lst = msg.split(DATA_DELIMITER)
#     msg_deli_cnt = msg.count('#')
#     if expected_fields == msg_deli_cnt:
#         return splitted_msg_lst
#     else:
#         return [None]

# """
# 	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
# 	Returns: string that looks like cell1#cell2#cell3
# 	"""
# def join_data(msg_fields: list):
#     msg_field_converted = [str(var) for var in msg_fields]
#     joined_lst = DATA_DELIMITER.join(msg_field_converted)
#     return joined_lst
#
# print(join_data(["username" , "password"]))
# print(join_data([1, 10]))
# print(join_data(["question", "ans1", "ans2", "ans3", "ans4", "correct", 500, 5.5]))
#
# """
# Gets command name (str) and data field (str) and creates a valid protocol message
# Returns: str, or None if error occured
# """
DATA_DELIMITER = "#"  # Delimiter in the data part of the message
CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
DELIMITER = "|"
valid_cmd = ('LOGIN', 'LOGOUT', 'LOGGED', 'GET_QUESTION', 'SEND_ANSWER', 'MY_SCORE', 'HIGHSCORE')
# def build_message(cmd, data):
#     if cmd in valid_cmd:
#         spaces = (CMD_FIELD_LENGTH - len(cmd)) * ' '
#         data_length = f"{len(data):04d}"
#         full_msg = cmd + spaces + DELIMITER + data_length + DELIMITER + data
#         return full_msg
#     else:
#         return None
#
# print(build_message('LOGIN', "aaaa#bbbb"))
# print(build_message('LOGIN', "aaaabbbb"))
# print(build_message('LOGIN', ""))
# print(build_message("0123456789ABCDEFGH", ''))







#Valid commands: LOGIN, LOGOUT, LOGGED, GET_QUESTION, SEND_ANSWER, MY_SCORE, HIGHSCORE
# Example: input: "LOGIN", "aaaa#bbbb"
#Output: LOGIN           |0009|aaaa#bbbb
# explanation: login + 11 spaces (16 - len(login))| len(message)|aaaa#bbbb

"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
"""

def parse_message(data: str):
	split_message = data.split(DELIMITER)
	if len(split_message) != 3:
		return None, None
	cmd = split_message[0].strip().upper()
	if cmd not in valid_cmd:
		return None, None
	data_length_str = split_message[1].strip()
	msg = split_message[2]
	print('msg:',msg)
	print('len_msg:', len(msg))
	print('datalen:',data_length_str)
	try:
		if len(msg) != int(data_length_str):
			return None, None
	except Exception as E:
		return None, None

	return cmd, msg
# print(parse_message("LOGIN           |   9| aaaa#bbbb"))
# print(parse_message("LOGIN          |    8|user#pass"))
print(parse_message("LOGIN           |9   | aaa#bbbb"))
# print(parse_message("LOGIN           |	  z|data"))