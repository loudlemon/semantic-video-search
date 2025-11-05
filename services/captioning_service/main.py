import io
import uvicorn
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

app = FastAPI(title="Captioning Service", version="0.1.0")
device = "cuda"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(device)


@app.post("/caption")
async def caption(image: UploadFile = File(...)):
    content = await image.read()
    img = Image.open(io.BytesIO(content)).convert("RGB")
    inputs = processor(images=img, return_tensors="pt").to(device)
    out = model.generate(**inputs, max_new_tokens=30)
    text = processor.decode(out[0], skip_special_tokens=True)
    return {"caption": text}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
