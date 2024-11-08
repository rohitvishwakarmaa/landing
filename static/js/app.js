document.getElementById("contactForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevents default form submission

    const formData = new FormData(this);

    fetch("/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Displays success message from the server
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

