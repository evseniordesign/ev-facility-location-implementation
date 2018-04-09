/* Set up button event listeners */
window.onload = function() {
	var json_btn = document.getElementById("json-sel");
	var csv_btn = document.getElementById("csv-sel");
	var json_file = document.getElementById("json-label");
	var csv_files = document.getElementById("csv-files");
	json_btn.addEventListener("click", function() {
		csv_btn.blur();
		json_btn.focus();
		csv_files.style.display = "none";
		json_file.style.display = "";
	});
	csv_btn.addEventListener("click", function() {
		json_btn.blur();
		csv_btn.focus();
		json_file.style.display = "none";
		csv_files.style.display = "";
	});

	var input_types = ["json", "facilities", "clients", "power"];
	input_types.forEach(function(name) {
		var input = document.getElementById(name + "-input");
		var label = document.getElementById(name + "-label");
		input.onchange = function() {
			label.innerText = input.value.substring(
				input.value.lastIndexOf("\\") + 1, input.value.length);
		}
	});
}