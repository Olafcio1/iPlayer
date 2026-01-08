import { Collector } from "./scripts/collector.js";
import { Player } from "./scripts/player.js";

const timeout = ms => new Promise(rsv => setTimeout(rsv, ms));

(async () => {
	while (window.pywebview?.api?.get_paths === undefined)
		await timeout(50);

	let collector = new Collector();
	let player = new Player(collector.files);

	collector.add_files();

	while (true) {
		if (player.files.length > 0) {
			player.next();
			break;
		}

		await timeout(300);
	}
})();
