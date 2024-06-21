document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed");

    document.getElementById("movieForm").addEventListener("submit", async function (event) {
        event.preventDefault();
        console.log("Form submitted");

        const title = document.getElementById("title").value;
        console.log("Title entered:", title);

        try {
            const response = await fetch(`http://127.0.0.1:5000/recommendations/${encodeURIComponent(title)}`);

            console.log("Response received");

            if (!response.ok) {
                throw new Error("Network response was not ok " + response.statusText);
            }

            const recommendations = await response.json();
            console.log("Recommendations:", recommendations);

            const resultsDiv = document.getElementById("results");
            resultsDiv.innerHTML = "";  // Clear previous results

            for (const id in recommendations.title) {
                const movieDiv = document.createElement("div");
                movieDiv.classList.add("movie");
                movieDiv.innerHTML = `<h3>${recommendations.title[id]}</h3><p>${recommendations.genres[id]}</p>`;
                resultsDiv.appendChild(movieDiv);
                console.log("Added movie:", recommendations.title[id]);
            }
        } catch (error) {
            console.error("Error fetching recommendations:", error);
        }
    });
});
