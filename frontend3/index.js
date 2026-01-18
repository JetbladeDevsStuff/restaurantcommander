"use strict";

const BASE_URL = new URL("http://127.0.0.1:8000");

let numChefs = 0;

function loadNumChefs() {
	const element = document.getElementById("numchefs");
	const element2 = document.getElementById("chefCurrent");
	const url = new URL("/user/num", BASE_URL);
	fetch(url).then((v) => {
		if (!v.ok) {
			element.innerText = "Failed";
		} else {
			v.json().then((v) => {
				numChefs = v;
				element.innerText = numChefs;
				element2.innerText = numChefs;
			});
		}
	});
}

function loadRecipeName() {
	const element = document.getElementById("recipe");
	const url = new URL("/recipe", BASE_URL);
	fetch(url).then((v) => {
		if (!v.ok) {
			element.innerText = "Failed";
		} else {
			v.json().then((v) => {
				element.innerText = v["name"]
			});
		}
	})
}

function loadChefDisplay() {
	const element = document.getElementById("chefdisplay");
	if (numChefs == 0) {
		element.innerText = "No chefs added";
		return;
	}
	for (let i = 0; i < numChefs; i++) {
		// TODO: This is wrong
		const url = new URL(`/user/${i}/tasks`, BASE_URL);
		fetch(url).then((v) => {
			if (!v.ok) {
				element.innerText = "Failed";
			} else {
				v.json().then((v) => {
					element.innerHTML = ""
					let text = ""
					for (const e of v) {
						text += e + "<br>";
					}
					element.innerHTML += `Chef ${i}: ${text}<br>`
				});
			}
		});
	}
}

function loadProgress() {
	const element = document.getElementById("progress");
	const url = new URL("/progress", BASE_URL)
	fetch(url).then((v) => {
		if (!v.ok) {
			element.innerText = "Failed";
		} else {
			v.json().then((v) => {
				element.innerText = `Progress: ${v["num"]}/${v["dem"]}`;
			});
		}
	});
}

function pressConfigure() {
	// Make the modal window popup
	const dialog = document.getElementById("dialog");
	dialog.showModal();
	
}

function pressReset() {
}

function decreaseChefs() {
	const deleteUrl = new URL("/user/delete", BASE_URL);
	fetch(deleteUrl, {method: "DELETE"}).then((v) => {
		if (!v.ok) {
			console.log("Failed:", v);
		}
	});
	loadNumChefs();
}

function increaseChefs() {
	const addUrl = new URL("/user/new", BASE_URL);
	fetch(addUrl, {method: "POST"}).then((v) => {
		if (!v.ok) {
			console.log("Failed:", v);
		}
	});
	loadNumChefs();
}

function clearChildren(node) {
	while (node.firstChild) {
		node.removeChild(node.firstChild);
	}
}

let selectedText = {"provider": "", "text": ""};

function finalizeImport() {
	const urlMealdb = new URL("/recipe/set/mealdb", BASE_URL);
	const urlManual = new URL("/recipe/set/manual", BASE_URL);
	const urlAi = new URL("/recipe/set/ai", BASE_URL);
	if (selectedText["provider"] === "mealdb") {
		fetch(urlMealdb, {
			method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({"name": selectedText["text"]})
		}).then((v) => {
			if (!v.ok) {
				console.error("FAIL")
			}
		});
	} else if (selectedText["provider"] === "manual") {
		fetch(urlManual, {
			method: "POST", body: selectedText["text"]
		}).then((v) => {
			if (!v.ok) {
				console.error("FAIL")
			}
		});
	} else if (selectedText["provider"] === "ai") {
		fetch(urlAi, {
			method: "POST", body: JSON.stringify({"description": selectedText["text"]})
		}).then((v) => {
			if (!v.ok) {
				console.error("FAIL")
			}
		});
	}
	document.getElementById("dialog").close();
}

function importMealDb() {
	const node = document.getElementById("content");
	clearChildren(node)
	let input = document.createElement("input");
	input.type = "search";
	input.id = "mealDbInput";
	input.addEventListener("input", () => {
		const text = input.value;
		for (let i = 0; i < 3; i++)
			document.getElementById(`mealDbLi${i}`).innerText = "";
		if (text.length > 3) {
			fetch(`https://www.themealdb.com/api/json/v1/1/search.php?s=${text}`).then((v) => {
				if (!v.ok) {
					document.getElementById("mealDbLi0").innerText = "Failed";
				} else {
					v.json().then((v) => {
						if (v["meals"] === null) {
							document.getElementById("mealDbLi0").innerText = "No results"
							return;
						}
						let maxbound = v["meals"].length < 3 ? v["meals"].length : 3
						for (let i = 0; i < maxbound; i++) {
							document.getElementById(`mealDbLi${i}`).innerText = v["meals"][i]["strMeal"];
						}
					});
				}
			});
		}
	});
	node.appendChild(input);
	let list = document.createElement("div");
	list.id = "mealDbList";
	for (let i = 0; i < 3; i++) {
		let li = document.createElement("div");
		li.id = `mealDbLi${i}`;
		li.addEventListener("click", (v) => {
			for (let i = 0; i < 3; i++)
				document.getElementById(`mealDbLi${i}`).style.backgroundColor = "";
			const element = v.target;
			selectedText = {"provider": "mealdb", "text": element.innerText};
			element.style.backgroundColor = "gray";
		});
		list.appendChild(li);
	}
	node.appendChild(list);
}

function importManual() {
	const node = document.getElementById("context");
	clearChildren(node);
	let input = document.createElement("input");
	input.type = "search";
	input.id = "manualInput";
	
}

document.addEventListener("DOMContentLoaded", () => {
	const configureButton = document.getElementById("configure");
	configureButton.addEventListener("click", pressConfigure);
	const resetButton = document.getElementById("reset");
	resetButton.addEventListener("click", pressReset);

	const chefSubtract = document.getElementById("chefSubtract");
	chefSubtract.addEventListener("click", decreaseChefs);
	const chefAdd = document.getElementById("chefAdd");
	chefAdd.addEventListener("click", increaseChefs);

	const mealDbButton = document.getElementById("mealdbButton");
	mealDbButton.addEventListener("click", importMealDb);

	const submitButton = document.getElementById("submitButton");
	submitButton.addEventListener("click", finalizeImport);

	loadNumChefs();
	loadRecipeName();
	loadChefDisplay();
	loadProgress();

	setTimeout(loadChefDisplay, 1000);
});

