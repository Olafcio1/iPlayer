import webview

from socky import Connection
from socky.threadsafe import Connection as ThreadedConnection
from socky.noncebased import Connection as NoncebasedConnection

from threading import Thread
from .protocol import Command, Notification, Close, VERSION

class HandledClient:
	sock: NoncebasedConnection
	server: "RemoteServer"

	def __init__(self, sock: ThreadedConnection, server: "RemoteServer"):
		self.sock = NoncebasedConnection(sock)
		self.server = server

	def receiver(self) -> None:
		while True:
			command = self.sock.recv_msg()
			if command == Close:
				self.send("v%d/bye" % VERSION)
				self.close()

				break
			else:
				try:
					self.server.invoke_command(Command(command))
				except:
					self.send("v%d/unr" % VERSION)
				else:
					self.send("v%d/ok" % VERSION)

	def sender(self) -> None:
		while self.sock.on:
			self.messages.wait()

			with self.messages.lock:
				for msg in self.messages:
					self.sock.send(msg)

class RemoteServer:
	sock: Connection
	win: webview.Window

	_clients: list[HandledClient]

	def __init__(self, win: webview.Window):
		self.win = win

		self.sock = Connection(clientClass=NoncebasedConnection)
		self.sock.bind("", 44561)
		self.sock.listen(6)

		self._clients = []

	def serve(self) -> None:
		while True:
			ip = "<unknown>"
			try:
				client, addr = self.sock.accept()
				if addr[0] not in ("localhost", "127.0.0.1", "::1"):
					client.close()
					continue

				ip = addr[0]

				print("🚦 client connect: %s" % ip)
				Thread(target=self.handle, args=(client,)).start()
			except (ConnectionError, ConnectionAbortedError, ConnectionResetError):
				print("🚦 client reset: %s" % ip)
			except:
				print("🚦 client panic: %s" % ip)
			else:
				print("🚦 client disconnect: %s" % ip)

	def handle(self, client: Connection) -> None:
		obj = HandledClient(client, self)
		self._clients.append(obj)
		Thread(target=obj.receiver).start()
		obj.sender()

	def notify(self, msg: Notification) -> None:
		for cl in self._clients:
			cl.send_msg(-1, msg.value[0])

	def invoke_command(self, cmd: Command) -> None:
		if cmd == Command.PAUSE:
			self.win.evaluate_js("iPlayer.player.audio.pause()");
		elif cmd == Command.PLAY:
			self.win.evaluate_js("iPlayer.player.audio.play()");
		elif cmd == Command.SPACE:
			self.win.evaluate_js("iPlayer.player.togglePlaying()");
		elif cmd == Command.NEXT:
			self.win.evaluate_js("iPlayer.player.next(1)");
		elif cmd == Command.PREV:
			self.win.evaluate_js("iPlayer.player.next(-1)");
		else:
			raise ValueError("What the fuh is that?!")
