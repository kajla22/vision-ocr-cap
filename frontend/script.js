async function uploadImage() {
  const fileInput = document.getElementById("fileInput");
  const status = document.getElementById("status");

  if (!fileInput.files.length) {
    alert("Select an image first");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  status.innerText = "Uploading...";

  try {
    const response = await fetch(
      "http://localhost:7071/api/UploadImageFunction",
      {
        method: "POST",
        body: formData
      }
    );

    if (!response.ok) {
      const text = await response.text();
      throw new Error(text);
    }

    const result = await response.json();
    status.innerText = "Upload successful ✅";
    console.log(result);

    window.location.href = `result.html?id=${result.imageName}`;

  } catch (err) {
    console.error(err);
    status.innerText = "Upload failed ❌";
  }
}
