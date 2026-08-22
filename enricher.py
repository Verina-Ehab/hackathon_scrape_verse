import json
import os
import urllib.request
import urllib.error

# ضع مفتاحك هنا
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

def call_gemini_api(prompt, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    with urllib.request.urlopen(req, timeout=30) as response:
        res_body = response.read().decode("utf-8")
        res_json = json.loads(res_body)
        text_content = res_json["candidates"][0]["content"]["parts"][0]["text"]
        return text_content

def enrich_venue_to_jogo_quest(venue):
    venue_name = venue.get("venue_name", "Unknown Venue")
    address = venue.get("neighborhood_and_address", "")
    hours = venue.get("hours", "Standard Operating Hours")
    price = venue.get("price_level", "$$")
    features = venue.get("features", [])
    reviews = venue.get("review_highlights", [])
    
    prompt = f"""
    You are the Lead Game Designer for JOGO, a real-world gamified mobile quest app.
    Given this scraped venue data, generate an enriched JOGO Quest JSON.

    VENUE RAW DATA:
    - Name: {venue_name}
    - Location: {address}
    - Operating Hours: {hours}
    - Price Level: {price}
    - Features: {features}
    - Reviews: {reviews}

    Generate a culturally authentic JOGO Quest with:
    1. "riddle_quest": Witty riddle in LOCAL DIALECT (Egyptian slang if in Egypt/Alexandria, or modern English if Global).
    2. "riddle_answer": Clean answer.
    3. "lens_hunter_target": Specific real-world visual item derived from reviews/features to photograph.
    4. "mega_quest_deal": 20% discount targeted during off-peak dead hours.
    5. "reward_coins": Integer (100 to 500).

    Respond ONLY with a valid raw JSON object (no markdown, no ```json):
    {{
        "riddle_quest": "string",
        "riddle_answer": "string",
        "lens_hunter_target": "string",
        "mega_quest_deal": {{
            "title": "string",
            "discount_percentage": 20,
            "valid_hours": "string (e.g. 1:00 PM - 4:00 PM)",
            "description": "string"
        }},
        "reward_coins": 250
    }}
    """

    try:
        raw_text = call_gemini_api(prompt, GEMINI_API_KEY)
        clean_text = raw_text.replace("```json", "").replace("```", "").strip()
        generated_quest = json.loads(clean_text)
    except Exception as e:
        print(f"⚠️ Fallback for {venue_name}: {e}")
        generated_quest = {
            "riddle_quest": f"مكان مشهور في {address} بيعمل أحلى قهوة وحلويات.. فما هو؟",
            "riddle_answer": venue_name,
            "lens_hunter_target": "Coffee cup or outdoor seating",
            "mega_quest_deal": {
                "title": "20% Off Flash Deal",
                "discount_percentage": 20,
                "valid_hours": "1:00 PM - 4:00 PM",
                "description": "Show active JOGO voucher for 20% off."
            },
            "reward_coins": 200
        }

    return {
        "id": f"jogo_{abs(hash(venue_name)) % 100000:05d}",
        "venue_name": venue_name,
        "address": address,
        "category": venue.get("category", "Cafe"),
        "rating": venue.get("rating", 4.5),
        "review_count": venue.get("review_count", 0),
        "phone": venue.get("phone", "N/A"),
        "hours": hours,
        "features": features,
        "jogo_gameplay": generated_quest
    }

def main():
    input_file = "raw_venues.json"
    output_file = "jogo_quests.json"

    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found!")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        venues = json.load(f)

    print(f"🚀 Processing {len(venues)} venues with Gemini API...")

    enriched_quests = []
    for index, venue in enumerate(venues, 1):
        name = venue.get("venue_name", f"Venue {index}")
        print(f"[{index}/{len(venues)}] 🧠 Enriching: {name}...")
        enriched = enrich_venue_to_jogo_quest(venue)
        enriched_quests.append(enriched)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(enriched_quests, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 SUCCESS! Generated {len(enriched_quests)} quests in: {output_file}")

if __name__ == "__main__":
    main()