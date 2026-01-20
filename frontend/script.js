const FUNCTION_URL = "https://<YOUR-FUNCTION-APP-NAME>.azurewebsites.net/api/UploadImageFunction";

async function uploadImage() {
    const fileInput = document.getElementById("imageInput");
    const result = document.getElementById("result");

    if (!fileInput.files.length) {
        result.innerText = "Please select an image";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch(FUNCTION_URL, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Upload failed");
        }

        result.innerHTML = `
            <p>${data.message}</p>
            <img src="${data.blobUrl}" width="300" />
        `;

    } catch (err) {
        result.innerText = "Upload failed: " + err.message;
    }
}
