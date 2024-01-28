document.addEventListener("DOMContentLoaded", function () {
  var plotForm = document.getElementById("plotForm");
  var plotContainer = document.getElementById("plotContainer");

  plotForm.addEventListener("submit", function (e) {
    e.preventDefault();

    var requestData = {
      stock: document.getElementById("stock").value,
      begin: document.getElementById("begin").value,
      end: document.getElementById("end").value,
      criteria: document.getElementById("criteria").value,
    };

    var params = new URLSearchParams(requestData);

    // create a fetch request to the server
    fetch("/api/plot?" + params, {
      method: "GET",
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json(); // Parse the response as JSON and return the promise
      })
      .then(function (jsonData) {
        console.log("JSON Data from server:", jsonData);

        var iFrameElement = document.createElement("iframe");
        iFrameElement.src = jsonData.image_path;

        iFrameElement.style.width = "80vw"
        iFrameElement.style.height = "80vh"

        plotContainer.innerHTML = "";
        plotContainer.appendChild(iFrameElement);
        // Now you can use jsonData as needed in your application
      })
      .catch(function (error) {
        console.error("Fetch error:", error);
      });
  });
});
