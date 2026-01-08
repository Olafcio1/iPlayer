export class Collector {
	files;
	interval;

	constructor() {
		this.files = [];
		this.interval = setInterval(this.add_files.bind(this), 2000);
	}

	async add_files() {
		let extend = await pywebview.api.get_paths();
		if (extend.length === null) {
			clearInterval(this.interval);
			return;
		}

		this.files.push(...extend);
	}
}
