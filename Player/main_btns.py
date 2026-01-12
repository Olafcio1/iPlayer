import sys
import os

path = "/".join(__file__.replace("\\", "/").split("/")[:-1])

sys.path.append(path + "/..")
os.chdir(path)

import webview

from remote.client import RemoteClient
from remote.protocol import Command

path = "/".join(__file__.replace("\\", "/").split("/")[:-1])

sys.path.append(path + "/..")
os.chdir(path)

class Api:
    _client: RemoteClient

    def command(self, name: str) -> None:
        self._client.send(Command[name.upper()])

    def next_event(self) -> str:
        return self._client.sock.recv_msg(-1).decode()

api = Api()

# Magic numbers ong frfr
# Most of them are from the css, like the gap, padding-right, etc.
# But the 25 and 20 are fucking magic (guess what, random ones that fit n' worked)

btnswidth = 4*2 + 23*3
btns = api._btns = webview.create_window(
    url="file:///%s/app/buttons.html" % os.getcwd(),
    title="iPlayer",
    js_api=api,
    easy_drag=True,
    frameless=True,
    x=40 + 250-8 - btnswidth-25,
    y=40,
    width=btnswidth+20,
    height=10,
    min_size=(btnswidth, 10),
    shadow=False,
    confirm_close=True,
    transparent=False,
    on_top=True
)

client = api._client = RemoteClient()
client.connect()

webview.start()
