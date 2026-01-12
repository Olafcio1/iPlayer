import StringUtil from "./string-util.js";

const songTitle = document.querySelector("#widget > .left > p");

export class Player {
	audio = new Audio();
	active = false;

	files;
	index = 0;

	constructor(files) {
		this.files = files;
		this.audio.volume = .7;
		this.setupEvents();
	}

	togglePlaying() {
		if (this.active) {
			this.audio.pause();
			pywebview.api.paused();
		} else {
			this.audio.play();
			pywebview.api.played();
		}

		this.active = !this.active;
	}

	setupEvents() {
		this.audio.addEventListener("pause", () => {
			pywebview.api.paused();
			this.active = false;
		});

		this.audio.addEventListener("play", () => {
			pywebview.api.played();
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
		prefixes.sort((a, b) => b.length - a.length);

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
