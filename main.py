import webview
import sys
import os

from api import Api

from remote.protocol import Command
from remote.server import RemoteServer
from remote.client import RemoteClient

os.chdir("/".join(__file__.replace("\\", "/").split("/")[:-1]))

args = sys.argv[1:]
nonEmpty = len(args) >= 1
if nonEmpty:
    if args[0] in ("/help", "--help", ":help", "help"):
        print("[-------- iPlayer CLI --------]")
        print("[help] Views this help page")
        print("[debug] Turns on the app with")
        print("        developer tools")
        print("[remote] A command group for")
        print("         managing iPlayer from")
        print("         an external interface")
    elif args[0] in ("/remote", "--remote", ":remote", "remote"):
        if (
                len(args) == 2 and
                (name := args[1]) and
                name.islower() and
                (cmd := Command._member_map_.get(name.upper()))
        ):
            client = RemoteClient()
            client.connect()
            client.send(cmd)
            client.close()

            print("Command '%s' transmitted" % cmd.name)
        else:
            print("[--------- iPlayer CLI ---------]")
            print("[          >> remote            ]")
            print("[pause] Pauses the playback")
            print("[play] Resumes the playback")
            print("[space] Toggles the playback")
            print("[next] Plays the next track")
            print("[prev] Plays the previous track")

    sys.exit(0)

api = Api()
win = webview.create_window(
    url="file:///%s/app/index.html" % os.getcwd(),
    title="iPlayer",
    js_api=api,
    easy_drag=True,
    frameless=True,
    x=40,
    y=40,
    width=250,
    height=10,
    min_size=(250, 10),
    shadow=False,
    confirm_close=True,
    transparent=True,
    on_top=True
)

win.events.loaded += lambda: RemoteServer(win).serve()
webview.start(ssl=True, debug=(
    nonEmpty and
    args[0] in ("/debug", "--debug", ":debug")
))
