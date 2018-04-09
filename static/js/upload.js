/* Set up button event listener */
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

	var json_input = document.getElementById("json-input");
	var json_label = document.getElementById("json-label");
	json_input.addEventListener("change", function() {
		json_label.innerText = json_input.value.substring(
			json_input.value.lastIndexOf("\\") + 1, json_input.value.length);
	});

	var facilities_input = document.getElementById("facilities-input");
	var facilities_label = document.getElementById("facilities-label");
	facilities_input.addEventListener("change", function() {
		facilities_label.innerText = facilities_input.value.substring(
			facilities_input.value.lastIndexOf("\\") + 1, facilities_input.value.length);
	});

	var clients_input = document.getElementById("clients-input");
	var clients_label = document.getElementById("clients-label");
	clients_input.addEventListener("change", function() {
		clients_label.innerText = clients_input.value.substring(
			clients_input.value.lastIndexOf("\\") + 1, clients_input.value.length);
	});

	var power_input = document.getElementById("power-input");
	var power_label = document.getElementById("power-label");
	power_input.addEventListener("change", function() {
		power_label.innerText = power_input.value.substring(
			power_input.value.lastIndexOf("\\") + 1, power_input.value.length);
	});
}