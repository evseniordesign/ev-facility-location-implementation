/* Set up button event listener */
window.onload = function() {
	var json_btn = document.getElementById("json-sel");
	var csv_btn = document.getElementById("csv-sel");
	var json_file = document.getElementById("json-file");
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
}