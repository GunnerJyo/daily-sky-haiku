const DATA_URL =
    "https://daily-sky-haiku-jyothish-2026.s3.us-east-1.amazonaws.com/latest.json";


async function loadHaiku() {

    try {

        const response = await fetch(
            DATA_URL + "?t=" + Date.now()
        );

        if (!response.ok) {
            throw new Error("Could not load latest haiku");
        }

        const data = await response.json();

        document.getElementById("location").textContent =
            `📍 ${data.city}, ${data.country}`;

        document.getElementById("haiku").innerHTML =
            data.haiku.replace(/\n/g, "<br>");

        document.getElementById("temperature").textContent =
            `${data.weather.temperature_2m}°C`;

        document.getElementById("humidity").textContent =
            `${data.weather.relative_humidity_2m}% humidity`;

        const generated =
            new Date(data.generated_at);

        document.getElementById("date").textContent =
            `Generated ${generated.toLocaleString()}`;

    } catch (error) {

        console.error(error);

        document.getElementById("location").textContent =
            "📍 Kochi, India";

        document.getElementById("haiku").innerHTML =
            "The sky is quiet today.<br>Check back soon<br>for a new poem.";

        document.getElementById("date").textContent =
            "Unable to load today's haiku";

    }

}


loadHaiku();