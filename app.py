from engine import (
    generate_ad_creative,
    generate_caption_model,
    save_caption_and_meta,
    rank_creatives_isolation,
    build_final_zip,
    create_run_folder,
    update_run_history,
    extract_text_from_logo,
    get_dominant_colors
)

import os

# Paths
LOGO = "uploads/logo.png"
PRODUCT = "uploads/product.png"

# Creative config
style = "Luxury"
tone = "Funny"
audience = "Gamers"
product_name = "Wireless Earbuds"

ads, captions, metas, scores = [], [], [], []

# ✅ 1. Create a new timestamped folder for this session
run_id, run_folder = create_run_folder()

# ✅ 2. Extract slogan + colors once
slogan = extract_text_from_logo(LOGO)
colors = get_dominant_colors(LOGO)

# ✅ 3. Generate creatives
for i in range(12):
    ad_path = generate_ad_creative(
        LOGO, PRODUCT, style, audience, tone, i+1, run_folder  # ✅ Correct function call now
    )

    ads.append(ad_path)

    # Caption from local LLM
    caption = generate_caption_model(product_name, audience, tone)

    # Save caption + metadata JSON + numeric score
    meta_path, caption_path, score = save_caption_and_meta(
        ad_path, caption, style, audience, tone, i+1
    )

    captions.append(caption_path)
    metas.append(meta_path)
    scores.append(score)

# ✅ 4. Rank
ranked_indexes = rank_creatives_isolation(scores)

# ✅ 5. Save ranking report
rank_report = os.path.join(run_folder, "ranking_report.txt")
with open(rank_report, "w", encoding="utf-8") as f:
    f.write("Creative Engagement Ranking (Predicted):\n\n")
    for rank, idx in enumerate(ranked_indexes):
        f.write(f"{rank+1}. {os.path.basename(ads[idx])} → Score: {scores[idx]}\n")

# ✅ 6. Store history
run_meta = {
    "style": style,
    "tone": tone,
    "audience": audience,
    "slogan": slogan,
    "brand_colors": colors,
    "total_creatives": len(ads),
    "best_score": max(scores)
}

update_run_history(run_id, run_folder, run_meta)

# ✅ 7. Create ZIP
final_zip_path = build_final_zip(ads, captions, metas, run_folder)

print("\n✅ Done! Final ZIP created at:", final_zip_path)
