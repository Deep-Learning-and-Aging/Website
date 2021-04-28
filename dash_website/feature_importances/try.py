from dash_website.utils.aws_loader import load_npy, load_jpg
import numpy as np
from PIL import Image
from io import BytesIO
import base64


dimension, subdimension, sub_subdimension, sex, age_group, aging_rate, sample = (
"Abdomen",
"Liver",
"Raw",
"male",
"young",
"accelerated",
"0",
)

display_mode = ["Raw", "Gradcam", "Saliency"]
images = {}

if "Raw" in display_mode:
    path_to_raw = f"datasets/images/{dimension}/{subdimension}/{sub_subdimension}/Raw/{sex}/{age_group}/{aging_rate}/{side}sample_{sample}.jpg"
    images["Raw"] = load_jpg(path_to_raw)).convert("RGBA")
if "Gradcam" in display_mode:
    path_to_grad_cam = f"datasets/images/{dimension}/{subdimension}/{sub_subdimension}/Gradcam/{sex}/{age_group}/{aging_rate}/{side}sample_{sample}.npy"
    images["Gradcam"] = Image.fromarray(load_npy(path_to_grad_cam).astype(np.uint8)).convert("RGBA")
if "Saliency" in display_mode:
    path_to_saliency = f"datasets/images/{dimension}/{subdimension}/{sub_subdimension}/Saliency/{sex}/{age_group}/{aging_rate}/{side}sample_{sample}.npy"
    images["Saliency"] = Image.fromarray(load_npy(path_to_saliency).astype(np.uint8))

if len(display_mode) == 1:
    image_to_display = images[display_mode[0]]
elif len(display_mode) == 2:
    image_to_display = Image.alpha_composite(images[display_mode[0]], images[display_mode[1]])
else:  # if len(display_mode) == 3:
    composite_image = Image.alpha_composite(images[display_mode[0]], images[display_mode[1]])

    image_to_display = Image.alpha_composite(composite_image, images[display_mode[1]])

buffer = BytesIO()
image_to_display.save(buffer, format="png")

encoded_image = base64.b64encode(buffer.getvalue())

print(f"data:image/png;base64,{encoded_image.decode()}")
