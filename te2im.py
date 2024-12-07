#%%
# THIS IS THE WORKING ONE
from huggingface_hub import InferenceClient
client = InferenceClient("black-forest-labs/FLUX.1-dev", token="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")

# information regarding the inference limits: https://huggingface.co/docs/api-inference/rate-limits
# output is a PIL.Image object
image = client.text_to_image("Astronaut riding a horse")
image.show()

#%%
# AND ALSO THIS
import requests

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content
image_bytes = query({
	"inputs": "Astronaut riding a horse",
})

# You can access the image with PIL.Image for example
import io
from PIL import Image
image = Image.open(io.BytesIO(image_bytes))