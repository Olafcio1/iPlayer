const songTitle = document.querySelector("#widget > .left > p");
const [
	songPrev,
	songPP,
	songNext
] = document.querySelectorAll("#widget > .right > i");

export class Player {
	audio = new Audio();
	active = false;

	files;
	index = 0;

	constructor(files) {
		this.files = files;
		this.audio.volume = .7;

		songPP.addEventListener("click", () => {
			if (this.active) {
				this.audio.pause();
				songPP.className = "facr fa-play";
			} else {
				this.audio.play();
				songPP.className = "facr fa-pause";
			}

			this.active = !this.active;
		});

		addEventListener("keydown", ev => {
			if (ev.key === "Enter") {
				let el = [songPrev, songPP, songNext].find(el => el.matches(":focus-within"));
				if (el) {
					ev.preventDefault();
					el.dispatchEvent(new Event("click"));
				}
			}
		});

		songPrev.addEventListener("click", () => this.next(-1));
		songNext.addEventListener("click", () => this.next(1));

		this.setupEvents();
	}

	setupEvents() {
		this.audio.addEventListener("pause", () => {
			songPP.className = "facr fa-play";
			this.active = false;
		});

		this.audio.addEventListener("play", () => {
			songPP.className = "facr fa-pause";
			this.active = true;
		});

		this.audio.addEventListener("ended", () => {
			this.next();
		});
	}

	next(after = 1) {
		let song = this.files[this.index += after];

		this.audio.src = "file:///" + song;
		this.audio.play();

		this.active = true;

		songTitle.innerText = song.substring(song.lastIndexOf("/") + 1)
								  .replaceAll("-", " ")
								  .replaceAll("_", " ")
							  .split(" ")
							  .map(word => word.length
							  				? word[0].toUpperCase() + word.substring(1)
							  				: word)
							  .join(" ");
		songPP.className = "facr fa-pause";
	}
}
