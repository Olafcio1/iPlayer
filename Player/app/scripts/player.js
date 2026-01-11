import StringUtil from "./string-util.js";

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
			this.togglePlaying();
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

	togglePlaying() {
		if (this.active) {
			this.audio.pause();
			songPP.className = "facr fa-play";
		} else {
			this.audio.play();
			songPP.className = "facr fa-pause";
		}

		this.active = !this.active;
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

		songTitle.innerText = this.humanize(song);
		songPP.className = "facr fa-pause";
	}

	humanize(song) {
		// basename
		song = song.substring(
			   	song.lastIndexOf("/") + 1,
				song.lastIndexOf(".")
			   );

		// fs copy mark removal
		// TODO: Optimize to substring at the end
		while (true)
			if (song.endsWith(" - copy"))
				song = song.substring(0, song.length - 7);
			else if (song.endsWith(" - kopia"))
				song = song.substring(0, song.length - 8);
			else if (StringUtil.endsWithPattern({
						"haystack": song,
						"pattern": " (.)"
					}))
				song = song.substring(0, song.length - 4);
			else break;

		// downloader watermark removal
		let prefixes = ["spotifydown.com", "[SPOTDOWNLOADER.COM]", "[SPOTIFY-DOWNLOADER.COM]"];
		for (let prefix of prefixes)
			if (StringUtil.startsWithSimilar({
					"haystack": song,
					"needle": prefix,
					"rate": 13
			}))
				song = song.substring(prefix.length);

		let suffix = "spotdown.app";
		if (StringUtil.endsWithSimilar({
				"haystack": song,
				"needle": suffix,
				"rate": 10
		}))
			song = song.substring(0, song.length - suffix.length);

		// space management
		song = song.replaceAll("-", " ")
				   .replaceAll("_", " ");

		// author name removal  (maybe soon in an additional textbox?)
		if (song.includes("   "))
			song = song.substring(song.indexOf("   ") + 1);

		// trimming
		song = StringUtil.trim(song, " -_");

		// capitalization
		song = song.split(" ")
		    	   .map(word => word.length
		  				? word[0].toUpperCase() + word.substring(1)
		  				: word)
		    	   .join(" ");

 	    return song;
	}
}
