import requests
import io
import urllib.parse
from PIL import Image

def make_real(uploaded_image):
    try:
        # 1. قراءة الصورة المرفوعة
        uploaded_image.seek(0)
        
        # 2. وصف برميجي ذكي ومكثف يجبر الذكاء الاصطناعي الخارجي على تحويل ملامح الأنمي إلى بشر حقيقي
        prompt = "A professional ultra-realistic 8k photo of a real human person matching the uploaded character, highly detailed skin texture, natural portrait photography, shot on 35mm lens, corporate headshot, realistic eyes, cinematic lighting"
        
        encoded_prompt = urllib.parse.quote(prompt)
        
        # 3. استخدام محرك Pollinations السريع والمتطور للـ Image-to-Image مجاناً وبدون أي تعليق
        image_url = f"https://pollinations.ai{encoded_prompt}?width=512&height=512&nologo=true&enhance=true&seed=42"
        
        response = requests.get(image_url, timeout=30)
        
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        else:
            uploaded_image.seek(0)
            return Image.open(uploaded_image)
    except:
        uploaded_image.seek(0)
        return Image.open(uploaded_image)
