import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

# استدعاء نموذج خفيف ومثبت مسبقاً بديل لـ Facenet
model = models.mobilenet_v3_small(pretrained=True)
model.eval()

# تجهيز وتحويل الصور لتناسب نموذج الذكاء الاصطناعي
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# ----------------------------
# Extract face embedding
# ----------------------------
def get_embedding(image_path):
    try:
        image = Image.open(image_path).convert('RGB')
        tensor = transform(image).unsqueeze(0)
        with torch.no_grad():
            # استخراج ميزات الوجه (Embedding)
            embedding = model(tensor).flatten().numpy()
        return embedding
    except:
        return np.zeros(576) # مصفوفة صفرية في حال حدوث خطأ

# ----------------------------
# Compare two faces
# ----------------------------
def compare_faces(img1, img2):
    emb1 = get_embedding(img1)
    emb2 = get_embedding(img2)

    # حساب المسافة الإقليدية تماماً كما في كودك الأصلي
    distance = np.linalg.norm(emb1 - emb2)

    # تحويل المسافة إلى نسبة مئوية للتشابه
    similarity = max(0, 1 - distance / 100)

    return round(similarity * 100, 2)
