export default class StringUtil {
	static startsWithSimilar({ haystack, needle, rate }) {
		let have = haystack.substring(0, needle.length);
		return this.equalsSimilar({
			"haystack": have,
			needle, rate
		});
	}

	static endsWithSimilar({ haystack, needle, rate }) {
		let have = haystack.substring(haystack.length, haystack.length - needle.length);
		return this.equalsSimilar({
			"haystack": have,
			needle, rate
		});
	}

	static equalsSimilar({ haystack, needle, rate }) {
		let index = 0;
		let array = [...haystack];
		for (let ch of array)
			if (needle[index] == ch)
				index++;

		return (index >= rate);
	}

	static endsWithPattern({ haystack, pattern }) {
		let i = 1;
		for (let ch of pattern) {
			if (ch != "." && haystack[haystack.length - i] != ch)
				return false;

			i--;
		}

		return true;
	}

	static trim(text, characters) {
		text = this.trimStart(text, characters);
		text = this.trimEnd(text, characters);

		return text;
	}

	static trimStart(text, characters) {
		let subFrom = 0;
		for (let i = 0; i < text.length; i++) {
			let ch = text[i];
			if (characters.includes(ch))
				subFrom++;
			else break;
		}

		return text.substring(subFrom);
	}

	static trimEnd(text, characters) {
		let subTo = 0;
		for (let i = text.length - 1; i >= 0; i--) {
			let ch = text[i];
			if (characters.includes(ch))
				subTo++;
			else break;
		}

		return text.substring(0, text.length - subTo);
	}
}
