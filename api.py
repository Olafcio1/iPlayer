import os

from typing import ClassVar
from threading import Thread, Lock

class Api:
    paths: list[str]
    pthreads: list[Thread]
    ptremove: list[Thread]
    plock: Lock

    directories: ClassVar[list[str]] = [
        "$USERPROFILE/Downloads",
        "$USERPROFILE/Music",
        "$USERPROFILE/OneDrive/Downloads",
        "$USERPROFILE/OneDrive/Music"
    ]

    def __init__(self) -> None:
        self.paths = []

        self.pthreads = []
        self.ptremove = []

        self.plock = Lock()
        self._path_collection()

    def _path_collection(self) -> None:
        for path in Api.directories:
            expanded = os.path.expandvars(path)
            if not os.path.exists(expanded):
                continue

            (t := Thread(target=self._path_thread, args=(
                expanded,
            ))).start()

            self.pthreads.append(t)

    def _path_thread(self, path: str) -> None:
        files = os.listdir(path)
        for fn in files:
            sub = path + "/" + fn
            if os.path.isdir(sub):
                self._path_thread(sub)
            elif sub.endswith((".mp3", ".wav", ".flac")):
                # os.path.isfile check skipped; please
                # don't create device files :sob:

                with self.plock:
                    self.paths.append(sub)

    def _remove_all(self) -> None:
        for thread in self.ptremove:
            self.pthreads.remove(thread)

        self.ptremove.clear()

    def get_paths(self) -> list[Thread] | None:
        if len(self.pthreads) > 0:
            for thread in self.pthreads:
                if not thread.is_alive:
                    self.ptremove.add(thread)

            self._remove_all()

            with self.plock:
                pcopy = self.paths.copy()
                self.paths.clear()

            return pcopy
        else:
            return None
