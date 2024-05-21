import socket
import chatlib

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    final_msg = chatlib.build_message(code, data)
    # print(f"final_msg: {final_msg}")
    conn.send(final_msg.encode())


def recv_message_and_parse(conn):
    full_msg = conn.recv(1024).decode()
    # print(f"Full message received: {full_msg}")  # Added print statement
    try:
        cmd, msg = chatlib.parse_message(full_msg)
        # print(f"code: {cmd}")      # Check what `code` is after parsing
        # print(f"data: {msg}")      # Check what `data` is after parsing
        # print(cmd, msg)
        return cmd, msg

    except Exception as e:
        error_and_exit("Failed to connect to server: " + str(e))


def connect():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((SERVER_IP, SERVER_PORT))
    except Exception as e:
        error_and_exit("Failed to connect to server: " + str(e))
    return conn

def error_and_exit(error_msg):
    print("Error:", error_msg)
    exit(1)



def login(conn):
    while True:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        login_data = f"{username}#{password}"
        code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["login_msg"], login_data)
        if code == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print("Logged in, Weclome!")
            break

        else:
            print("Login failed. Please try again.")


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    conn.close()

def build_send_recv_parse(conn, code, data):
    """
    Sends a message using the built message, receives a response, and parses it.
    Args:
        conn: The socket connection.
        code: The message code to send.
        data: The data to send with the message.
    Returns:
        A tuple containing the response code and data.
    """
    build_and_send_message(conn, code, data)
    return recv_message_and_parse(conn)


def get_score(conn):
    code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["myscore_msg"], "")
    if code == chatlib.PROTOCOL_SERVER["score_reply"]:
        print(f"Your score: {data}")
    else:
        print(f"Error getting score: {data}")


def get_highscore(conn):
    code, data = build_send_recv_parse(conn,chatlib.PROTOCOL_CLIENT["highscore_msg"], "")
    if code == chatlib.PROTOCOL_SERVER['highestscore_reply']:
        print(data)
    else:
        print('error')

def play_question(conn):
    question_id = handle_question(conn)
    user_answer = int(input("What is your answer? "))
    code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["answer_msg"], f"{question_id}#{user_answer}")
    if code == chatlib.PROTOCOL_SERVER['correctanswer_reply']:
        print('Correct Answer')
    elif code == chatlib.PROTOCOL_SERVER['wronganswer_reply']:
        print('Wrong Answer')

def handle_question(conn):
    code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["getquestion_msg"], "")
    new_data = data.replace('#', '\n')
    lines = []
    for line in new_data.splitlines():
        lines.append(line)
    question_id = lines[0]
    question = lines[1]
    answers = lines[2::]
    print(question)
    for count, item in enumerate(answers, 1):
        print(count, item)
    return question_id


def get_logged_users(conn):
    code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["logged_msg"], "")
    if code == chatlib.PROTOCOL_SERVER['logged_reply']:
        print(data)
    else:
        print('reply')



def user_menu(conn):
    while True:
        user_menu_pick = input(f"1     Get my score\n2     Get high score\n3     Get logged users\n4     Play a trivia question\n5     Quit\nEnter your choice: ").strip()

        if user_menu_pick == '1':
            get_score(conn)

        elif user_menu_pick == '2':
            get_highscore(conn)

        elif user_menu_pick == '3':
            get_logged_users(conn)


        elif user_menu_pick == '4':
            play_question(conn)

        elif user_menu_pick == '5':
            print("Thanks for playing, Bye.")
            break


        else:
            print("Please enter a valid choice.")


def main():
    conn = connect()
    login(conn)
    user_menu(conn)
    logout(conn)


if __name__ == '__main__':
    main()
