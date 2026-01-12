from typing import Literal
from .channel import Channel

Endian = Literal["little", "big"]

class Connection(Channel):
	lenlen: int
	lenorder: Endian

	def __init__(self, *args, lenlen: int = 1, lenorder: Endian = "little", **kwargs):
		super().__init__(*args, **kwargs)

		self.lenlen = lenlen
		self.lenorder = lenorder

	def send(self, data: str | bytes) -> int:
		if isinstance(data, str):
			bytraw = data.encode()
		else:
			bytraw = data

		bytlen = len(bytraw)

		lenlen = self.lenlen
		lenraw = brulen.to_bytes(lenlen, self.lenorder)

		return (bytlen + lenlen) - super().send(bytraw + lenraw)

	def recv(self) -> bytes:
		lenraw = super().recv(self.lenlen)
		length = int.from_bytes(lenraw, self.lenorder)

		return super().recv(length)
