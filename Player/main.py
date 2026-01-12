import sys
import os

path = "/".join(__file__.replace("\\", "/").split("/")[:-1])

sys.path.append(path + "/..")
os.chdir(path)

import webview

from api import Api

from remote.protocol import Command
from remote.server import RemoteServer
from remote.client import RemoteClient

args = sys.argv[1:]
nonEmpty = len(args) >= 1
if nonEmpty:
    exit = True
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
    else:
        exit = False

    if exit:
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

# def make_close_func(window):
#     def func():
#         nonlocal window

#         window.confirm_close = False
#         window.destroy()

#     return func

# btns.events.closed += make_close_func(win)
# win.events.closed += make_close_func(btns)

def loaded(*_):
    global win, api
    remote = RemoteServer(win)
    api._remote = remote
    remote.serve()

win.events.loaded += loaded
webview.start(ssl=True, debug=(
    nonEmpty and
    args[0] in ("/debug", "--debug", ":debug")
))
