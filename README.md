# GroundTruthHackathon
# AdForge Studio: The AI Creative Engine H-003

Tagline: A Generative AI–powered creative studio that converts brand logos and product images into 10+ unique, high-resolution ad creatives, tailored captions, engagement rankings, and platform-optimized assets—packaged into a production-ready ZIP in under 30 seconds.

## 1. The Problem (Real World Scenario)

Context:
In the marketing and AdTech world, businesses spend weeks creating creative variations of the same product image and hours rewriting captions for different audiences.

The Pain Point:

Manual designing is slow and repetitive

Caption writing drains creative energy

No real feedback on what might perform best

Social platform formats require extra editing time

## My Solution:
I built AdForge Studio, an Auto-Creative Engine that eliminates manual effort.
Just upload your brand logo + product image, select your creative preferences—and within 30 seconds, you get:

10+ visually distinct, high-resolution ad creatives
Personalized captions written uniquely for target audiences
AI-generated creative ranking by predicted engagement
Auto-formatted assets for multiple social platforms
Everything bundled into one downloadable ZIP

## 2. Expected End Result
For the User

Input: Upload

A brand logo

A product image

Action: Configure preferences → click Generate
Output: A professional ZIP containing:

10+ High-Resolution Ad Creatives

10+ Matching Captions (1:1 mapped)

Engagement ranking report

Metadata JSON files per creative including:

chosen style, tone, audience, platform suggestion

engagement score position

Platform-optimized creative formats for:

Instagram posts and reels (9:16)

LinkedIn banners

Pinterest pins

Digital posters

## 3. Technical Approach

This was built as a scalable, robust creative automation studio, not just a simple script.

### System Workflow
#### Stage	Implementation

Language: Python 3.11

Image Generation: Stable Diffusion XL (local via AUTOMATIC1111 API or diffusers library)

LLM (Captions & Narratives): Llama 3.2 3B (local via Ollama) , Mistral 7B / Gemma 2 9B / Falcon 7B optional (all free open-weight models)

Engagement Scoring & Ranking: LLM-simulated scoring + Scikit-Learn (if extended, Isolation Forest for future anomaly/style outlier detection)

Image Processing & Logo Overlay: Pillow

Social Media Asset Formatting: Pillow (resizing for Instagram post/reel, LinkedIn banner, Pinterest pin, Poster 9:16)

Metadata Storage: JSON (generated per creative)

Packaging & Export: Python zipfile module

Deployment: Streamlit Cloud / Docker + Docker Compose (optional containerization for production demo)

#### Captions & insights are generated using free local models:

Llama 3.2 3B

Mistral 7B

Falcon 7B

Gemma 2 9B

Free Image Model Used

Stable Diffusion XL

(All models run locally with no paid API dependency.)

## 4. Tech Stack
Category	Technology
Language	Python 3.11
Frontend UI	React + Custom CSS
Image Generation	Stable Diffusion XL
Text AI (Captions & Narratives)	Llama 3.2 3B, Mistral 7B, Falcon 7B, Gemma 2 9B
Engagement Scoring	Free local LLM engagement simulation
Social Media Formatting	Pillow image resizing
Packaging & Export	Python ZIP utilities
Deployment	Docker
## 5. Challenges & Learnings
### Challenge 1: Ensuring Visual Uniqueness

#### Issue: Ads looked too similar initially.

#### Learning & Fix:
I designed a prompt variation engine that forces AI to change:

layout, lighting, typography, background and composition
while preserving logo + product identity.

### Challenge 2: Caption Repetition

#### Issue: Captions lacked tone variation across scale.

#### Solution:
Implemented multi-tone prompt templates + audience-aware hooks so every caption feels fresh, emotional and target-aligned.

### Challenge 3: Multi-Platform Formatting

#### Learning:
Automated creative resizing for all popular social media and poster formats instead of making users manually edit dimensions.

## 6. Added Innovation Modules (7 Extra Features)
### Extra Feature	Description
1. AI Style Selector	Choose themes like Minimal, Neon, Luxury, Vintage, 3D, Hand-drawn, Futuristic, Watercolor
2. Multi-Tone Caption Engine	Generate captions that sound Funny, Emotional, Luxury, Gen Z, Elegant, or Professional
3. Audience Targeting	Copies adapt automatically for Parents, Gamers, Athletes, Gen Z, or Working Professionals
4. Engagement Scorer & Ranker	AI evaluates each creative + caption pair and ranks them by predicted engagement
5. Metadata JSON Generator	Every ad gets a JSON containing style, tone, audience, best-fit platform, and rank position
6. Live Creative Preview UI Grid	Interactive grid view with hover animation and click-to-regenerate specific creatives
7. Social Media Export Formatter	One-click auto-format for Instagram posts/reels, LinkedIn banners, Pinterest pins, and 9:16 posters

These 7 modules make the system feel like a true Marketing Automation Product, adding personalization and usability for real businesses.

## 7. How to Run
### 1. Clone Repository
git clone https://github.com/Mishikasardana/GroundTruthHackathon.git

### 2. Install Backend Dependencies
pip install -r requirements.txt

### 3. Start Backend
python app.py

### 4. Start Frontend
cd frontend
npm install
npm start

### 5. Generate Creatives
Upload your logo + product, configure your preferences, and download ZIP

## Summary

AdForge Studio is an end-to-end Generative AI Creative Studio built to solve real marketing inefficiencies, offering creative control, personalization, ranking, and ready-to-post assets, powered 100% using free and open-weight AI models.


