async function uploadReceipt() {
	const fileInput = document.getElementById("fileInput");
	const file = fileInput.files[0];

	if (!file) {
		alert("Please Insert A File");
		return;
	}

	const formData = new FormData();
	formData.append("file", file);

	try {
		const res = await fetch("/api/receipts/process", {
			method: "POST",
			body: formData,
		});

		const data = await res.json();
		document.getElementById("result").textContent = JSON.stringify(data, null, 2);
	} catch (err) {
		console.error(err);
		alert("Upload Failed!");	
	}
}
