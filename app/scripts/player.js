const songTitle = document.querySelector("#widget > .left > p");
const songPPbtn = document.querySelector("#widget > .right > i:nth-child(2)");

export class Player {
	audio = new Audio();

	files;
	index = 0;

	constructor(files) {
		this.files = files;
		this.audio.volume = .7;
	}

	next() {
		let song = this.files[this.index++];

		this.audio.src = "file:///" + song;
		this.audio.play();

		songTitle.innerText = song.substring(song.lastIndexOf("/") + 1)
								  .replaceAll("-", " ")
								  .replaceAll("_", " ")
							  .split(" ")
							  .map(word => word[0].toUpperCase() + word.substring(1))
							  .join(" ");
		songPPbtn.className = "facr fa-pause";
	}
}
