from PIL import Image
import io
from functions import generate_image_from_text

image_bytes = generate_image_from_text("Soft Anime Style. Two hands shaking in agreement with a city skyline in the background, representing a strong and trustworthy partnership.")

dataBytesIO = io.BytesIO(image_bytes)
img = Image.open(dataBytesIO)
img.save(f"abc.jpg")
