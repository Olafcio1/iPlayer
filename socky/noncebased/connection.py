import time

from typing import Callable
from ..threadsafe.connection import Connection as ThreadedConnection

class Connection(ThreadedConnection):
	_recv_nonce: int
	_send_nonce: int

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self._recv_nonce = 0
		self._send_nonce = 0

	#####################################
	## Methods for incremental sending ##
	#####################################

	def recv(self, **kwargs) -> bytes:
		r = self.recv_msg(self._recv_nonce, **kwargs)
		self._recv_nonce += 1

		return r

	def send(self, data: bytes) -> bytes:
		self.send_msg(self._send_nonce, data)
		self._send_nonce += 1

	##################################
	## Methods for concrete sending ##
	##################################

	def recv_msg(self, nonce: int, *, pollDelay: float = .1) -> bytes:
		value = [None]
		self.on_message(self._listener_for(value))

		while value[0] == None:
			time.sleep(pollDelay)

		return value[0]

	def send_msg(self, nonce: int, data: bytes) -> bytes:
		self.send(self._get_nonce_bytes(nonce) + data)

	####################
	## Helper methods ##
	####################

	def _listener_for(self, arr: list[bytes], nonce: int) -> Callable[[bytes], None]:
		nb = self._get_nonce_bytes(nonce)

		def func(data: bytes):
			nonlocal arr, nb
			if data.startswith(nb):
				arr[0] = data[len(nb):]
				return True

		return func

	def _get_nonce_bytes(self, nonce: int) -> bytes:
		return (nonce + ":").encode()
