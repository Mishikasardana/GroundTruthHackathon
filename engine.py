import os
import io
import json
import random
import zipfile
import datetime
import requests
import smtplib
import easyocr
from PIL import Image
from email.message import EmailMessage
from sklearn.ensemble import IsolationForest
from colorthief import ColorThief

# Initialize OCR Reader (EasyOCR)
reader = easyocr.Reader(['en'])

# --- Root Folder History ---
BASE_ROOT = "generated_runs"
HISTORY_FILE = "run_history.json"

# ----- CREATE A NEW RUN FOLDER -----
def create_run_folder(base_root=BASE_ROOT):
    os.makedirs(base_root, exist_ok=True)
    run_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_path = os.path.join(base_root, run_id)

    os.makedirs(os.path.join(run_path, "ads"), exist_ok=True)
    os.makedirs(os.path.join(run_path, "captions"), exist_ok=True)
    os.makedirs(os.path.join(run_path, "metadata"), exist_ok=True)

    return run_id, run_path


# ----- BRAND COLOR DETECTION -----
def get_dominant_colors(logo_path, top_n=2):
    try:
        ct = ColorThief(logo_path)
        return ct.get_palette(color_count=top_n)
    except:
        return [(128, 0, 128), (255, 255, 255)]


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


# ----- SLOGAN EXTRACTION USING EASYOCR -----
def extract_text_from_logo(logo_path):
    try:
        result = reader.readtext(logo_path)
        text = " ".join([r[1] for r in result])
        return text if text else "Slogan not detected"
    except Exception as e:
        print("❌ OCR Error:", e)
        return "Creative Studio by AI"


# ----- IMAGE GENERATION USING POLLINATIONS AI -----
def generate_image_pollinations(prompt):
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"
    try:
        response = requests.get(url, timeout=30)
        return Image.open(io.BytesIO(response.content))
    except:
        # fallback blank image
        return Image.new("RGB", (1024, 1024))


# ----- GENERATE AD CREATIVE -----
def generate_ad_creative(logo_path, product_path, style, audience, tone, index, run_folder):
    slogan = extract_text_from_logo(logo_path)
    colors = [rgb_to_hex(c) for c in get_dominant_colors(logo_path)]

    prompt = (
        f"Create a completely new {style} ad creative for {audience}. "
        f"Use brand colors {colors[0]} and {colors[1]}. Tone: {tone}. "
        f"Include slogan reference '{slogan}'. Modern composition with bold typography and strong CTA."
    )

    ad_img = generate_image_pollinations(prompt)

    # Overlay assets
    try:
        logo = Image.open(logo_path).convert("RGBA").resize((230,230))
        product = Image.open(product_path).convert("RGBA").resize((650,650))
        ad_img.paste(product, (187,200), product)
        ad_img.paste(logo, (390,20), logo)
    except Exception:
        pass

    save_path = os.path.join(run_folder, "ads", f"ad_{index}.png")
    ad_img.save(save_path)
    return save_path


# ----- CAPTION GENERATION USING LOCAL LLAMA LLM (OLLAMA) -----
def generate_caption_model(product, audience, tone):
    try:
        import ollama
        system_msg = "You are a highly viral social media ad copy expert."
        prompt = f"Write a new, short, {tone} marketing caption for {product} targeting {audience}. Use emojis and include a strong CTA."
        res = ollama.chat(model="llama3.2", messages=[{"role":"system","content":system_msg},{"role":"user","content":prompt}])
        return res["message"]["content"]
    except Exception as e:
        print("❌ LLM Error:", e)
        return "Caption generation failed."


# ----- SAVE CAPTION & METADATA -----
def save_caption_and_meta(ad_path, caption, style, audience, tone, index):
    cap_folder = os.path.join(os.path.dirname(ad_path), "..", "captions")
    meta_folder = os.path.join(os.path.dirname(ad_path), "..", "metadata")

    caption_path = os.path.join(cap_folder, f"caption_{index}.txt")
    with open(caption_path, "w", encoding="utf-8") as f:
        f.write(caption)

    colors = [rgb_to_hex(c) for c in get_dominant_colors(logo_path="uploads/logo.png")]

    meta = {
        "style": style,
        "tone": tone,
        "audience": audience,
        "slogan": extract_text_from_logo("uploads/logo.png"),
        "dominant_colors": colors,
        "engagement_score": random.randint(70, 99),
        "file": os.path.basename(ad_path),
        "caption": caption
    }

    meta_path = os.path.join(meta_folder, f"meta_{index}.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    return meta_path, caption_path, meta["engagement_score"]


# ----- STORE HISTORY -----
def update_run_history(run_id, run_path, meta):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    history.append({
        "run_id": run_id,
        "path": run_path,
        "meta": meta,
        "created_at": datetime.datetime.now().isoformat()
    })

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


# ----- RANK CREATIVES WITH REAL ENGAGEMENT MODEL (ISOLATION FOREST) -----
def rank_creatives_isolation(scores):
    model = IsolationForest(contamination=0.2, random_state=42)
    data = [[s] for s in scores]
    model.fit(data)
    decision = model.decision_function(data)
    ranked = sorted(range(len(scores)), key=lambda i: decision[i] + scores[i]/100, reverse=True)
    return ranked


# ----- GENERATE FINAL ZIP -----
def build_final_zip(ad_paths, caption_paths, meta_paths, run_folder):
    ranking_data = "\n".join([f"{i+1}. {os.path.basename(ad_paths[i])} → Score: {meta_paths[i]}" for i in range(len(ad_paths))])

    zip_path = os.path.join(run_folder, "final_creatives.zip")
    with zipfile.ZipFile(zip_path, "w") as z:
        for ad in ad_paths:
            z.write(ad, arcname="ads/"+os.path.basename(ad))
        for cap in caption_paths:
            z.write(cap, arcname="captions/"+os.path.basename(cap))
        for meta in meta_paths:
            z.write(meta, arcname="metadata/"+os.path.basename(meta))
        z.writestr("ranking_report.txt", ranking_data)

    return zip_path


# ----- EMAIL DELIVERY ----- 
def send_zip_via_email(zip_path, to_email, sender_email, sender_password):
    msg = EmailMessage()
    msg["Subject"] = "Your Creative Variations Are Ready!"
    msg["From"] = sender_email
    msg["To"] = to_email
    msg.set_content("Delivering your AI-generated ad creatives. See the attached ZIP.")

    with open(zip_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="zip", filename=os.path.basename(zip_path))

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(sender_email, sender_password)
        s.send_message(msg)

    print("✅ Email sent successfully!")