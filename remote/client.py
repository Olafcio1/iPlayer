import webview
import socket
from .protocol import Command, VERSION, b

class RemoteClient:
	sock: socket.socket

	def __init__(self):
		self.sock = socket.socket()

	def connect(self) -> None:
		self.sock.connect(("127.0.0.1", 44561))

	def get_length(self) -> None:
		lenraw = self.sock.recv(1)
		length = int.from_bytes(lenraw, 'little')

		return length

	def send(self, cmd: Command) -> None:
		self.sock.send(cmd.value)

		status = self.sock.recv(self.get_length())
		probableCause = \
			"protocol version mismatch" \
			if not status.startswith(b("v%d/" % VERSION)) \
			else "server error"

		status = status.partition(b"/")[2]
		if status == b"unr":
			raise RemoteClientError("unrecognized command; " + probableCause)
		elif status == b"bye":
			raise RemoteClientError("unrecognized disconnection; " + probableCause)

	def close(self) -> None:
		self.sock.send(bytes([100]))

		status = self.sock.recv(self.get_length())
		probableCause = \
			"protocol version mismatch" \
			if not status.startswith(b("v%d/" % VERSION)) \
			else "server error"

		status = status.partition(b"/")[2]
		if status == b"unr":
			raise RemoteClientError("failed disconnection: unrecognized command; " + probableCause)
		elif status == b"ok":
			raise RemoteClientError("failed disconnection: processed command; " + probableCause)

		self.sock.close()

class RemoteClientError(BaseException):
	pass
