import json
import os
import urllib.request
import urllib.error
import time
import uuid

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

def call_gemini_batch(venues_batch, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    prompt = f"""
    You are the Lead Game Designer for JOGO. Given this list of {len(venues_batch)} cafes/venues, generate culturally authentic JOGO Quests matching our treasures schema requirements.

    VENUES INPUT:
    {json.dumps(venues_batch, ensure_ascii=False)}

    FOR EACH VENUE, generate the following fields:
    1. "title_ar": Arabic name of the venue (e.g. "تريانون" for "trianon").
    2. "category": Must be exactly one of: 'cultural', 'food', 'hidden_gem', 'entertainment', 'history'. Choose based on the venue's reviews and features.
    3. "clue_en": A witty riddle in English.
    4. "clue_ar": A witty riddle in Egyptian Alexandrian Arabic slang.
    5. "riddle_answer_ar": Clean answer in Arabic.
    6. "target_object_prompt": Specific visual item/decor from reviews/features to photograph (in English, e.g. "historic wall paintings").
    7. "target_object_prompt_ar": Specific visual item/decor from reviews/features to photograph (in Arabic, e.g. "اللوحات الجدارية التاريخية").
    8. "description_en": A brief engaging description of the venue in English.
    9. "description_ar": A brief engaging description of the venue in Arabic.
    10. "reward_coins": Integer (250-400).
    11. "difficulty": One of: "Easy", "Medium", "Hard".
    12. "tips_en": JSON array of 2 helpful hints/clues in English.
    13. "tips_ar": JSON array of 2 helpful hints/clues in Arabic.

    Respond ONLY with a JSON array of objects matching the input order:
    [
      {{
        "venue_name": "exact name from input",
        "title_ar": "...",
        "category": "...",
        "clue_en": "...",
        "clue_ar": "...",
        "riddle_answer_ar": "...",
        "target_object_prompt": "...",
        "target_object_prompt_ar": "...",
        "description_en": "...",
        "description_ar": "...",
        "reward_coins": 300,
        "difficulty": "Medium",
        "tips_en": ["...", "..."],
        "tips_ar": ["...", "..."]
      }}
    ]
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    max_retries = 6
    backoff_factor = 2
    delay = 5.0
    
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                raw_text = res_json["candidates"][0]["content"]["parts"][0]["text"]
                clean_text = raw_text.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_text)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < max_retries - 1:
                print(f"⚠️ API returned {e.code}. Retrying batch in {delay}s...")
                time.sleep(delay)
                delay *= backoff_factor
            else:
                raise e

def main():
    input_file = "raw_venues.json"
    output_file = "jogo_quests.json"

    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found!")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        venues = json.load(f)

    print(f"🚀 Processing {len(venues)} venues in smart batches of 5 with gemini-3.5-flash...")

    enriched_quests = []
    batch_size = 5

    for i in range(0, len(venues), batch_size):
        batch = venues[i:i + batch_size]
        print(f"🧠 Processing batch {i//batch_size + 1}/{(len(venues) + batch_size - 1)//batch_size}...")
        
        try:
            generated_batch = call_gemini_batch(batch, GEMINI_API_KEY)
            
            for venue, gen in zip(batch, generated_batch):
                venue_name = venue.get("venue_name", "Unknown Venue")
                title_ar = gen.get("title_ar", venue_name)
                clue_ar = gen.get("clue_ar", "")
                clue_en = gen.get("clue_en", "")
                riddle_answer_ar = gen.get("riddle_answer_ar", "")
                target_object_prompt = gen.get("target_object_prompt", "")
                target_object_prompt_ar = gen.get("target_object_prompt_ar", "")

                enriched_quests.append({
                    "id": str(uuid.uuid4()),
                    "title": venue_name,
                    "location": venue.get("neighborhood_and_address", ""),
                    "lat": None,
                    "lng": None,
                    "reward_coins": gen.get("reward_coins", 300),
                    "clue": clue_ar,
                    "align_x": None,
                    "align_y": None,
                    "type_icon": "cafe",
                    "rating": float(venue.get("rating", 4.5)),
                    "distance": None,
                    "is_active": True,
                    "difficulty": gen.get("difficulty", "Medium"),
                    "title_en": venue_name,
                    "title_ar": title_ar,
                    "clue_en": clue_en,
                    "clue_ar": clue_ar,
                    "riddle_answer": venue_name,
                    "riddle_answer_ar": riddle_answer_ar,
                    "riddle_accepted_answers": [venue_name.lower(), title_ar],
                    "created_at": None,
                    "qr_code": None,
                    "initial_reward": None,
                    "min_reward": None,
                    "decay_rate_per_hour": None,
                    "is_todays_gem": False,
                    "is_squad": False,
                    "required_squad_size": 1,
                    "estimate_time": "30 mins",
                    "image_url": "https://images.unsplash.com/photo-1519451241324-20b4ea2c4220?q=80&w=1000&auto=format&fit=crop",
                    "tips_en": gen.get("tips_en", []),
                    "tips_ar": gen.get("tips_ar", []),
                    "activated_at": None,
                    "is_mega": False,
                    "expires_at": None,
                    "brand_id": None,
                    "special_instruction": None,
                    "special_instruction_ar": None,
                    "max_claims_capacity": None,
                    "hero_image_url": None,
                    "banner_image_url": None,
                    "banner_title_en": None,
                    "banner_title_ar": None,
                    "banner_bg_color": None,
                    "sponsor_name": None,
                    "sponsor_logo_url": None,
                    "merchant_cta_url": None,
                    "merchant_cta_text": None,
                    "merchant_cta_text_ar": None,
                    "mega_type": None,
                    "starts_at": None,
                    "requires_photo_proof": True,
                    "photo_instructions": f"Take a clear photo of: {target_object_prompt}" if target_object_prompt else None,
                    "photo_instructions_ar": f"صوّر صورة واضحة لـ: {target_object_prompt_ar}" if target_object_prompt_ar else None,
                    "secret_menu_title": None,
                    "secret_menu_duration_mins": None,
                    "is_pulse_radar": False,
                    "is_lens_hunter": True,
                    "is_jogo_spy": False,
                    "target_object_prompt": target_object_prompt,
                    "target_object_prompt_ar": target_object_prompt_ar,
                    "game_mode": "lens_hunter",
                    "notification_radius_meters": 200,
                    "created_by": None,
                    "created_by_user_id": None,
                    "description_en": gen.get("description_en", ""),
                    "description_ar": gen.get("description_ar", ""),
                    "category": gen.get("category", "food"),
                    "city": "Alexandria",
                    "max_squad_size": 5,
                    "squad_split_reward": False,
                    "geofence_radius_meters": 70,
                    "radar_found_radius_meters": 15,
                    "cooldown_hours_per_user": 168,
                    "max_daily_attempts_per_user": 5,
                    "badge_label_en": "Mega Quest",
                    "badge_label_ar": "مهمة كبرى"
                })
        except Exception as e:
            print(f"⚠️ Batch error: {e}, using safe mapping...")
            for venue in batch:
                venue_name = venue.get("venue_name", "Unknown")
                enriched_quests.append({
                    "id": str(uuid.uuid4()),
                    "title": venue_name,
                    "location": venue.get("neighborhood_and_address", ""),
                    "lat": None,
                    "lng": None,
                    "reward_coins": 250,
                    "clue": "مكان في الإسكندرية معروف بأحلى قهوة وديكور.. تفتكر مين؟",
                    "align_x": None,
                    "align_y": None,
                    "type_icon": "cafe",
                    "rating": float(venue.get("rating", 4.5)),
                    "distance": None,
                    "is_active": True,
                    "difficulty": "Medium",
                    "title_en": venue_name,
                    "title_ar": venue_name,
                    "clue_en": f"A famous place in {venue.get('neighborhood_and_address', '')} known for great coffee and vibe. What is it?",
                    "clue_ar": "مكان في الإسكندرية معروف بأحلى قهوة وديكور.. تفتكر مين؟",
                    "riddle_answer": venue_name,
                    "riddle_answer_ar": venue_name,
                    "riddle_accepted_answers": [venue_name.lower()],
                    "created_at": None,
                    "qr_code": None,
                    "initial_reward": None,
                    "min_reward": None,
                    "decay_rate_per_hour": None,
                    "is_todays_gem": False,
                    "is_squad": False,
                    "required_squad_size": 1,
                    "estimate_time": "30 mins",
                    "image_url": "https://images.unsplash.com/photo-1519451241324-20b4ea2c4220?q=80&w=1000&auto=format&fit=crop",
                    "tips_en": ["Look for a popular cafe in this area."],
                    "tips_ar": ["ابحث عن مقهى مشهور في هذه المنطقة."],
                    "activated_at": None,
                    "is_mega": False,
                    "expires_at": None,
                    "brand_id": None,
                    "special_instruction": None,
                    "special_instruction_ar": None,
                    "max_claims_capacity": None,
                    "hero_image_url": None,
                    "banner_image_url": None,
                    "banner_title_en": None,
                    "banner_title_ar": None,
                    "banner_bg_color": None,
                    "sponsor_name": None,
                    "sponsor_logo_url": None,
                    "merchant_cta_url": None,
                    "merchant_cta_text": None,
                    "merchant_cta_text_ar": None,
                    "mega_type": None,
                    "starts_at": None,
                    "requires_photo_proof": True,
                    "photo_instructions": "Take a clear photo of the coffee cup or outdoor seating",
                    "photo_instructions_ar": "صوّر صورة واضحة لفنجان القهوة أو الجلسة الخارجية",
                    "secret_menu_title": None,
                    "secret_menu_duration_mins": None,
                    "is_pulse_radar": False,
                    "is_lens_hunter": True,
                    "is_jogo_spy": False,
                    "target_object_prompt": "Coffee cup or outdoor seating",
                    "target_object_prompt_ar": "فنجان قهوة أو جلسة خارجية",
                    "game_mode": "lens_hunter",
                    "notification_radius_meters": 200,
                    "created_by": None,
                    "created_by_user_id": None,
                    "description_en": "A charming neighborhood spot.",
                    "description_ar": "مكان مميز وجذاب في الحي.",
                    "category": "food",
                    "city": "Alexandria",
                    "max_squad_size": 5,
                    "squad_split_reward": False,
                    "geofence_radius_meters": 70,
                    "radar_found_radius_meters": 15,
                    "cooldown_hours_per_user": 168,
                    "max_daily_attempts_per_user": 5,
                    "badge_label_en": "Mega Quest",
                    "badge_label_ar": "مهمة كبرى"
                })
        
        time.sleep(2)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(enriched_quests, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 SUCCESS! Generated {len(enriched_quests)} JOGO Quests in: {output_file}")

if __name__ == "__main__":
    main()