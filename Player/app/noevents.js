const nonPassive = { passive: false };

addEventListener("dragstart", ev => ev.preventDefault(), nonPassive);
addEventListener("keydown", ev => {
	if (ev.ctrlKey && ev.code == "KeyP")
		ev.preventDefault();
}, nonPassive);
