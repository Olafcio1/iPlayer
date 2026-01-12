from enum import Enum

class Command(Enum):
	PAUSE = b"\x00"
	PLAY = b"\x01"
	SPACE = b"\x02"
	NEXT = b"\x03"
	PREV = b"\x04"

class Notification(Enum):
	PLAY = b"\x00"
	PAUSE = b"\x01"

Close = b"\xff"
VERSION = 2
