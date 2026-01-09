import webview
import socket
from .protocol import Command, VERSION, d

class RemoteServer:
	sock: socket.socket
	win: webview.Window

	def __init__(self, win: webview.Window):
		self.win = win

		self.sock = socket.socket()
		self.sock.bind(("", 44561))
		self.sock.listen(6)

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
				while True:
					command = client.recv(1)
					if command == 100:
						try:
							client.send(d("v%d/bye" % VERSION))
							client.close()
						except: pass
						break
					else:
						try:
							if not self.invoke_command(Command(command)):
								raise Exception()
						except:
							client.send(d("v%d/unr" % VERSION))
						else:
							client.send(d("v%d/ok" % VERSION))
			except (ConnectionError, ConnectionAbortedError, ConnectionResetError):
				print("🚦 client reset: %s" % ip)
			except:
				print("🚦 client panic: %s" % ip)
			else:
				print("🚦 client disconnect: %s" % ip)

	def invoke_command(self, cmd: Command) -> bool:
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
			return False

		return True
