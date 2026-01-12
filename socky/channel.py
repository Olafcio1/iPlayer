from socket import socket
from typing import TypeVar

C = TypeVar('C', bound="Channel", contravariant=True)

class Channel:
	sock: socket
	on: bool

	clientClass: type[C]

	def __init__(self, sock: socket | None = None, on: bool = False, *, clientClass: type[C] | None = None):
		if sock == None:
			sock = socket()

		self.sock = sock
		self.on = on

		self.clientClass = Channel \
						   if clientClass is None \
						   else clientClass

	def connect(self, host: str, port: int) -> None:
		self.sock.connect((host, port))

	def accept(self) -> tuple[C, ...]:
		sock, addr = self.sock.accept()
		return (
			self.clientClass(sock, True),
			addr
		)

	def bind(self, host: str, port: int) -> None:
		self.sock.bind((host, port))

	def listen(self, mode: int) -> None:
		self.sock.listen(mode)
		self.on = True

	def send(self, data: bytes) -> int:
		try:
			return self.sock.send(data)
		except:
			self.on = False
			raise

	def recv(self, length: int) -> bytes:
		try:
			return self.sock.recv(length)
		except:
			self.on = False
			raise

	def close(self) -> None:
		self.sock.close()
		self.on = False

	def detach(self) -> None:
		self.sock.detach()
