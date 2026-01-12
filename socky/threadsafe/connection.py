import time

from typing import Callable
from threading import Thread

from .threads import Synchronized
from ..connection import Connection as NonsafeConnection

class Connection(NonsafeConnection):
	receiving: Synchronized[list[Callable[[bytes], None]]]
	receiving_listeners: Synchronized[list[Callable[[bytes], None]]]

	sending: Synchronized[list[bytes]]

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def connect(self, host: str, port: int) -> None:
		"""
		Connects a thread-safe `Connection` to the provided address.
		This is supposed to be run on the main thread.
		"""

		super().connect(host, port)

		self.receiving = Synchronized([])
		self.receiving_listeners = Synchronized([])

		self.sending = Synchronized([])

		Thread(target=self.receiver).start()
		Thread(target=self.sender).start()

	def receiver(self) -> None:
		while True:
			msg = super().recv()

			with self.receiving.lock:
				array = self.receiving.value
				length = len(array)
				if length > 0:
					i = 0
					while i < length:
						array[i](msg)
						i += 1

					array.clear()

			with self.receiving_listeners.lock:
				array = self.receiving_listeners.value
				length = len(array)
				if length > 0:
					i = 0
					while i < length:
						if array[i](msg) == True:
							array.pop(i)
						else:
							i += 1

	def sender(self) -> None:
		while self.on:
			self.sending.wait()

			with self.sending.lock:
				for msg in self.sending:
					super.send(msg)

	def recv(self, *, pollDelay: float = .1) -> bytes:
		value: bytes = None
		with self.receiving as array:
			array.append(lambda new: (value := new))

		while value == None:
			time.sleep(pollDelay)

		return value

	def send(self, data: bytes) -> bytes:
		with self.sending as array:
			array.append(data)

	def on_message(self, listener: Callable[[bytes], None]) -> None:
		with self.receiving_listeners as array:
			array.append(listener)
