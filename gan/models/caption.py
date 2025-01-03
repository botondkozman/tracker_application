from transformers import pipeline
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
# Sourced from: https://huggingface.co/tasks/image-to-text
# Models and images defined
models = ["Salesforce/blip-image-captioning-base", "nlpconnect/vit-gpt2-image-captioning"]
images = ["carrotCat.jpeg", "purpleDog.jpeg"]
## !!CHANGE IMAGE PATH to YOUR /gan/images directory and OS type!!
imgPath = "/home/benedekder/odin/tracker_application/gan/images/"
for image in images: 
    for model in models:
        captioner = pipeline("image-to-text", model)
        generated = captioner(imgPath + image)
        print("Image: {}, Model: {}, caption: {}".format(image, model, generated[0]['generated_text']))



# Runs the noamrot/FuseCap model: https://huggingface.co/noamrot/FuseCap_Image_Captioning
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
processor = BlipProcessor.from_pretrained("noamrot/FuseCap")
model = BlipForConditionalGeneration.from_pretrained("noamrot/FuseCap").to(device)

for image in images: 
    raw_image = Image.open(imgPath + image).convert('RGB')

    text = "a picture of "
    inputs = processor(raw_image, text, return_tensors="pt").to(device)

    out = model.generate(**inputs, num_beams = 3)
    print(processor.decode(out[0], skip_special_tokens=True))

