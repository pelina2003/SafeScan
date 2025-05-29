from torchvision import transforms
from PIL import Image
import torch
from models.analysis_result import AnalysisResult

# Φόρτωση προεκπαιδευμένου μοντέλου
from torchvision.models import resnet18, ResNet18_Weights

weights = ResNet18_Weights.DEFAULT
model = resnet18(weights=weights)
model.eval()


# Προεπεξεργασία εικόνας (όπως απαιτείται από το resnet)
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Dummy mapping (κανονικά θα βάζαμε ImageNet labels ή custom δικές σου)
acceptable_keywords = ["fire", "emergency", "disaster", "smoke", "accident", "volcano"]
unacceptable_keywords = ["meme", "cartoon", "person", "nude", "naked", "dog", "cat"]

def classify_image(image_path):
    image = Image.open(image_path).convert("RGB")
    input_tensor = preprocess(image).unsqueeze(0)  # batch size = 1

    with torch.no_grad():
        output = model(input_tensor)
        predicted_idx = torch.argmax(output[0]).item()

    # Κατέβασε τα labels (μόνο την 1η φορά — ή τοποθέτησέ τα τοπικά)
    from urllib.request import urlopen
    labels_url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    with urlopen(labels_url) as f:
        categories = [line.strip().decode("utf-8") for line in f.readlines()]

    label = categories[predicted_idx]
    return label.lower()

def analyze_images(image_paths):
    for path in image_paths:
        label = classify_image(path)
        print(f"📷 Ανάλυση εικόνας: {path} → '{label}'")

        if any(bad in label for bad in unacceptable_keywords):
            return AnalysisResult(relevant=False, confidence=0.9, summary=label)  # high confidence, rejected

        if any(good in label for good in acceptable_keywords):
            continue  # keep checking next images

        # άγνωστη κατηγορία = απόρριψη με χαμηλή εμπιστοσύνη
        return AnalysisResult(relevant=False, confidence=0.3, summary=label)

    # αν όλες οι εικόνες είναι αποδεκτές
    return AnalysisResult(relevant=True, confidence=1.0, summary="valid_images")