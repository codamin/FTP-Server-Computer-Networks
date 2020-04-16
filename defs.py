CONFIG_PATH = './config.json'
HOST_IP = '127.0.0.1'
RECV_SIZE = 1024


#SERVER RESPONSE MSGs
NAME_OKAY_MSG = '331 User name okay, need password.'
BAD_SEQUENCE_MSG = '503 Bad sequence of commands.'
LOG_IN_OKAY_MSG = '230 User logged in, proceed.'
PWD_OKAY_MSG = 'PWD responded'
LOG_IN_FALED_MSG = '430 Invalid username or password.'
MKD_PATH_CREATED = 'path created.'
RMD_PATH_DELETED = 'path deleted.'
LIST_DONE = 'List transfer done.'
CWD_OKAY_MSG = "250 Successful Change."
DL_OKAY_MSG = "Successful Download."
QUIT_OKAY_MSG = "Successful Quit."
OPEN_CONN_MSG = "Can't open data connection."
NOT_AVAILABLE_MSG = "Requested action not taken.File unavailable."

#RESPONSE CODES
NAME_OKAY_CODE = '331'
BAD_SEQUENCE_CODE = '503'
LOG_IN_OKAY_CODE = '230'
LOG_IN_FALED_CODE = '430'
PWD_OKAY = '257'
RMD_OKAY = '250'
LIST_OKAY = '226'
HELP_OKAY = '214'
QUIT_OKAY = '221'
OPEN_CONN_FAIL = '425'
NOT_AVAILABLE_CODE = '550'


PATH = 'path'