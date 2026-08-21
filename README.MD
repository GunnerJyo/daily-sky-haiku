# 🌤️ Daily Sky Haiku

> **An autonomous AI creative agent that turns the daily weather into a new haiku every morning.**

🔗 **Live Demo:** [https://daily-sky-haiku-jyothish.netlify.app/](https://daily-sky-haiku-jyothish.netlify.app/)

---

## ✨ What is Daily Sky Haiku?

**Daily Sky Haiku** is an always-on AI creative app built for the AWS Weekend Challenge.

Every morning, the app automatically:

1. 🌦️ Fetches the latest weather for **Kochi, Kerala**
2. 🤖 Sends the weather context to **Amazon Bedrock – Nova Lite**
3. ✍️ Generates an original three-line weather-themed haiku
4. 💾 Stores the generated poem and weather data in **Amazon S3**
5. 🌐 Displays the latest haiku on the public website

No button needs to be clicked. The poem is created automatically every morning.

---

## 🏗️ Architecture

```text
                 ┌─────────────────────┐
                 │   Amazon EventBridge │
                 │   Every Morning      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    AWS Lambda       │
                 │  Daily Sky Haiku    │
                 └──────────┬──────────┘
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
        ┌─────────────────┐   ┌──────────────────┐
        │  Open-Meteo API │   │ Amazon Bedrock   │
        │  Live Weather   │   │    Nova Lite     │
        └────────┬────────┘   └────────┬─────────┘
                 │                     │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │     Amazon S3       │
                 │     latest.json     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │       Netlify       │
                 │   Public Frontend   │
                 └─────────────────────┘
```

---

## 🛠️ AWS Services Used

| Service                | Purpose                                           |
| ---------------------- | ------------------------------------------------- |
| **AWS Lambda**         | Runs the AI creative workflow                     |
| **Amazon EventBridge** | Automatically triggers the Lambda every morning   |
| **Amazon Bedrock**     | Provides generative AI capabilities               |
| **Amazon Nova Lite**   | Generates the weather-themed haiku                |
| **Amazon S3**          | Stores the latest generated poem and weather data |
| **IAM**                | Controls Lambda access to Bedrock and S3          |

### Other Technologies

* **Open-Meteo** — weather data
* **HTML**
* **CSS**
* **JavaScript**
* **Netlify** — frontend hosting
* **GitHub** — source code management

---

## 🤖 How the AI Agent Works

The Lambda function receives the current weather and creates a prompt for Nova Lite.

Example context:

```text
Location: Kochi, Kerala

Temperature: 28.8°C
Humidity: 75%
Precipitation: 0 mm
Cloud cover: ...
```

Nova Lite then creates a three-line poem inspired by those conditions.

Example:

```text
Whispers of the monsoon
Silent rain on Kochi's streets
Silent, soft, and sweet.
```

The result is saved as:

```text
latest.json
```

in Amazon S3.

---

## ⏰ Autonomous Generation

The app uses an Amazon EventBridge schedule:

```text
cron(30 1 * * ? *)
```

This triggers the Lambda every day at:

**7:00 AM IST**

The workflow runs automatically without requiring the user to open the website.

---

## 🌐 Live Website

**Daily Sky Haiku:**
[https://daily-sky-haiku-jyothish.netlify.app/](https://daily-sky-haiku-jyothish.netlify.app/)

The website reads the latest generated data from Amazon S3 and displays:

* 📍 Location
* 🌡️ Temperature
* 💧 Humidity
* ✍️ Today's AI-generated haiku
* 🕐 Generation time

---

## 🔐 Security

The Lambda function uses an IAM execution role rather than storing AWS credentials in the source code.

Required permissions are limited to:

* `bedrock:InvokeModel`
* `s3:GetObject`
* `s3:PutObject`

AWS credentials and environment secrets are excluded from Git using `.gitignore`.

---

## 🎯 Challenge Goal

This project was created for the AWS **"Set Your Creative App Free" Weekend Challenge**.

The key idea is simple:

> **The app creates something new even when nobody is using it.**

Instead of waiting for a user to click **Generate**, Daily Sky Haiku wakes up every morning, looks at the sky, asks AI for a poem, and publishes it for the world to discover.

---

## 🚀 Future Improvements

Possible future features:

* 🌍 Support multiple cities
* 📚 Maintain a historical archive of previous haikus
* 🌧️ Weather-specific visual themes
* 🖼️ Generate an AI background image for each poem
* 📱 Progressive Web App (PWA)
* 📊 Weather and haiku history
* 🔔 Daily notifications

---

## 👨‍💻 Author

**Jyothish Nalinakshan**

AWS Builder Community · Developer · Creator

---

## 📜 License

This project is created for educational and challenge purposes.
