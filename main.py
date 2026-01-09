import webview
import sys
import os

from api import Api

os.chdir("/".join(__file__.replace("\\", "/").split("/")[:-1]))

if "--help" in sys.argv:
    print("[------- iPlayer CLI -------]")
    print("[help] Views this help page")
    print("[debug] Turns on the app with\n")
    print("        developer tools")

    sys.exit(0)

api = Api()
webview.create_window(
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

webview.start(ssl=True, debug="--debug" in sys.argv)
