import os
import webview

from remote.server import RemoteServer
from remote.protocol import Notification

from typing import ClassVar
from threading import Thread, Lock

class Api:
    _paths: list[str]
    _pthreads: list[Thread]
    _ptremove: list[Thread]
    _plock: Lock

    _directories: ClassVar[list[str]] = [
        "$USERPROFILE/Downloads",
        "$USERPROFILE/Music",
        "$USERPROFILE/OneDrive/Downloads",
        "$USERPROFILE/OneDrive/Music"
    ]

    _remote: RemoteServer

    def __init__(self) -> None:
        self._paths = []

        self._pthreads = []
        self._ptremove = []

        self._plock = Lock()
        self._path_collection()

    def _path_collection(self) -> None:
        for path in Api._directories:
            expanded = os.path.expandvars(path)
            if not os.path.exists(expanded):
                continue

            (t := Thread(target=self._path_thread, args=(
                expanded,
            ))).start()

            self._pthreads.append(t)

    def _path_thread(self, path: str) -> None:
        files = os.listdir(path)
        for fn in files:
            sub = path + "/" + fn
            if os.path.isdir(sub):
                self._path_thread(sub)
            elif sub.endswith((".mp3", ".wav", ".flac")):
                # os.path.isfile check skipped; please
                # don't create device files :sob:

                with self._plock:
                    self._paths.append(sub)

    def _remove_all(self) -> None:
        for thread in self._ptremove:
            self._pthreads.remove(thread)

        self._ptremove.clear()

    def get_paths(self) -> list[Thread] | None:
        if len(self._pthreads) > 0:
            for thread in self._pthreads:
                if not thread.is_alive:
                    self._ptremove.add(thread)

            self._remove_all()

            with self._plock:
                pcopy = self._paths.copy()
                self._paths.clear()

            return pcopy
        else:
            return None

    def paused(self) -> None:
        self._remote.notify(Notification.PAUSE)

    def played(self) -> None:
        self._remote.notify(Notification.PLAY)
