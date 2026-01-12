from typing import TypeVar, Generic, Callable
from threading import Lock, Event

T = TypeVar('T')
class Synchronized(Generic[T]):
	value: T
	lock: Lock
	run: Event

	def __init__(self, value: T):
		self.value = value
		self.lock = Lock()
		self.run = Event()

	def __enter__(self):
		self.lock.__enter__()
		return self.value

	def __exit__(self, *exc):
		self.lock.__exit__()
		self.run.set()
		return False

	def wait(self) -> None:
		self.run.wait()
		self.run.clear()

	def op(self, callback: Callable[T, None]) -> None:
		with self as value:
			callback(value)
