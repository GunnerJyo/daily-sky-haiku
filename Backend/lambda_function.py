import json
import urllib.request
import boto3
from datetime import datetime, timezone

# AWS clients
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")

# Configuration
BUCKET_NAME = "daily-sky-haiku-jyothish-2026"
MODEL_ID = "amazon.nova-lite-v1:0"

# Kochi coordinates
LATITUDE = 9.9312
LONGITUDE = 76.2673


def get_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}"
        f"&longitude={LONGITUDE}"
        "&current=temperature_2m,relative_humidity_2m,"
        "precipitation,weather_code,cloud_cover"
        "&timezone=Asia%2FKolkata"
    )

    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode())


def generate_haiku(weather):
    current = weather["current"]

    prompt = f"""
You are a creative haiku poet.

Write exactly ONE original weather-themed haiku
inspired by the current weather in Kochi, Kerala.

Weather:
Temperature: {current["temperature_2m"]}°C
Humidity: {current["relative_humidity_2m"]}%
Precipitation: {current["precipitation"]} mm
Cloud cover: {current["cloud_cover"]}%

Rules:
- Exactly 3 lines.
- Keep it poetic and natural.
- Mention or evoke Kochi, Kerala, or its atmosphere.
- Do not use a title.
- Do not add explanations.
- Return ONLY the three lines of the haiku.
"""

    request_body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 150,
            "temperature": 0.8
        }
    }

    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=request_body["messages"],
        inferenceConfig=request_body["inferenceConfig"]
    )

    haiku = response["output"]["message"]["content"][0]["text"].strip()

    return haiku


def save_to_s3(haiku, weather):
    data = {
        "city": "Kochi",
        "country": "India",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "haiku": haiku,
        "weather": weather["current"]
    }

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key="latest.json",
        Body=json.dumps(data, indent=2),
        ContentType="application/json",
        CacheControl="no-cache"
    )

    return data


def lambda_handler(event, context):

    print("Daily Sky Haiku agent started.")

    try:

        # 1. Get weather
        weather = get_weather()

        print("Weather retrieved:")
        print(weather["current"])

        # 2. Generate haiku
        haiku = generate_haiku(weather)

        print("Generated haiku:")
        print(haiku)

        # 3. Save to S3
        result = save_to_s3(haiku, weather)

        print("Saved latest.json to S3.")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Daily Sky Haiku generated successfully.",
                "haiku": haiku,
                "city": "Kochi"
            })
        }

    except Exception as e:

        print("ERROR:", str(e))

        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }