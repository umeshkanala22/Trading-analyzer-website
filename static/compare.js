document.addEventListener("DOMContentLoaded", function () {
  var compareForm = document.getElementById("compareForm");
  var plotContainer = document.getElementById("plotContainer");

  compareForm.addEventListener("submit", function (e) {
    e.preventDefault();

    var selectedStocks = Array.from(
      document.getElementById("stocks").selectedOptions
    ).map((option) => option.value);

    console.log(selectedStocks);
    var requestData = {
      stocks: selectedStocks,
      begin: document.getElementById("begin").value,
      end: document.getElementById("end").value,
      criteria: document.getElementById("criteria").value,
    };

    // create a post fetch request to the server

    fetch("/api/compare", {
      method: "POST",
      body: JSON.stringify(requestData),
      headers: {
        "Content-Type": "application/json",
      },
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

        iFrameElement.style.width = "70vw";
        iFrameElement.style.height = "68vh";

        plotContainer.innerHTML = "";
        plotContainer.appendChild(iFrameElement);
      })
      .catch(function (error) {
        console.error("Fetch error:", error);
      });
  });
});
