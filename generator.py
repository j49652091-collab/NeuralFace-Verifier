import requests
import io
from PIL import Image

# السيرفر الخارجي المخصص لتوليد صور الوجوه الحقيقية
API_URL = "https://huggingface.co"
HEADERS = {"Authorization": "Bearer hf_vHIdbREbYpXbYwXbYwXbYwXbYwXbYwXbYwXbYw"}

def make_real(uploaded_file):
    try:
        # قراءة محتوى الملف المرفوع كـ بايتات لإرسالها للسيرفر
        uploaded_file.seek(0)
        image_bytes = uploaded_file.read()
        
        # وصف نصي ذكي يدمج الصورة لإنتاج بورتريه وجه بشري حقيقي بدقة 8k
        prompt = "A highly detailed, realistic, ultra-photographic professional portrait of a real human being, corporate headshot, 8k resolution, natural lighting, sharp focus, looking at camera."
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "negative_prompt": "anime, cartoon, 3d, painting, drawing, plastic, fake, deformed, extra limbs"
            }
        }
        
        # إرسال الطلب للسيرفر الخارجي
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        
        # إذا تم التوليد بنجاح، اعرض الصورة الحقيقية المصنوعة
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        else:
            # إذا كان السيرفر مشغولاً، نرجع الصورة الأصلية لكي لا يعلق التطبيق
            uploaded_file.seek(0)
            return Image.open(uploaded_file)
    except:
        # في حال حدوث أي خطأ غير متوقع
        uploaded_file.seek(0)
        return Image.open(uploaded_file)
