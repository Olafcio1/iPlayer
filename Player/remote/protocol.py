from enum import Enum

class Command(Enum):
	PAUSE = b"\x00"
	PLAY = b"\x01"
	SPACE = b"\x02"
	NEXT = b"\x03"
	PREV = b"\x04"

VERSION = 1
b = lambda string: string.encode()

def d(string):
	raw = b(string)
	return len(raw).to_bytes(1, 'little') + raw
