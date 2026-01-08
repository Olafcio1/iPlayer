import webview
import os

from api import Api

os.chdir("/".join(__file__.replace("\\", "/").split("/")[:-1]))

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

webview.start(ssl=True, debug=True)
