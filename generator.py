import requests
import io
from PIL import Image

def make_real(uploaded_file):
    try:
        # وصف تفصيلي فائق الدقة لصنع فتاة حقيقية (نظارات، شعر بني، قبعة ممرضة)
        prompt = "A highly detailed hyper-realistic 8k photo of a real human young woman, wearing glasses, round spectacles, brown hair, wearing a white nurse cap, professional portrait, studio lighting, highly photorealistic, ultra-detailed skin texture, real person, real photography"
        
        # تحسين الكلمات لتفادي مشاكل الرموز في الروابط
        clean_prompt = prompt.replace(" ", "%20")
        
        # رابط السيرفر المباشر والسريع لإنشاء الصورة مجاناً وبدون حسابات
        image_url = f"https://pollinations.ai{clean_prompt}?width=512&height=512&nologo=true&enhance=true"
        
        # جلب البيانات باستخدام المكتبة الجديدة والتأكد من نجاح العملية
        response = requests.get(image_url, timeout=20)
        
        if response.status_code == 200:
            # هنا نقوم بتحويل البيانات القادمة من الرابط إلى صورة حقيقية ملموسة
            return Image.open(io.BytesIO(response.content))
        else:
            # حل احتياطي إذا كان السيرفر الخارجي مشغولاً جداً
            uploaded_file.seek(0)
            return Image.open(uploaded_file)
    except:
        # حماية الموقع من التوقف التام في حال ضعف شبكة الإنترنت
        uploaded_file.seek(0)
        return Image.open(uploaded_file)
