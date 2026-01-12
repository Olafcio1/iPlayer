import webview

from socky.threadsafe import Connection
from .protocol import Command, Notification, Close, VERSION

class RemoteClient:
	sock: Connection

	def __init__(self):
		self.sock = Connection()

	def connect(self) -> None:
		self.sock.connect("127.0.0.1", 44561)

	def send(self, cmd: Command) -> None:
		self.sock.send(cmd.value)

		status = self.sock.recv_msg(nonce)
		probableCause = \
			"protocol version mismatch" \
			if not status.startswith(b("v%d/" % VERSION)) \
			else "server error"

		status = status.partition(b"/")[2]
		if status == b"unr":
			raise RemoteClientError("unrecognized command; " + probableCause)
		elif status == b"bye":
			raise RemoteClientError("unrecognized disconnection; " + probableCause)

	def read(self) -> Notification:
		return self.sock.recv_msg(-1)

	def close(self) -> None:
		self.sock.send(Close)

		status = self.sock.recv()
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
