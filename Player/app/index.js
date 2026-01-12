import { Collector } from "./scripts/collector.js";
import { Player } from "./scripts/player.js";

const timeout = ms => new Promise(rsv => setTimeout(rsv, ms));

window.iPlayer = {};

(async () => {
	while (window.pywebview?.api?.get_paths === undefined)
		await timeout(150);

	let collector = new Collector();
	let player = new Player(collector.files);

	iPlayer.collector = collector;
	iPlayer.player = player;

	collector.add_files();

	while (true) {
		if (player.files.length > 0) {
			player.next(0);
			break;
		}

		await timeout(300);
	}
})();
