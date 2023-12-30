import requests, os
from PIL import Image
from openai import OpenAI

if "OPENAI_API_KEY" not in os.environ:
    raise Exception("OPENAI_API_KEY environment variable not set")

client = OpenAI()
default_model = "dall-e-3"
default_quality = "standard"
n = 1

custom_instructions = """
Custom instructions:
    - the images generated should be 1-bit black and white
    - should be minimal enough to be displayed on a tiny 128x32 OLED screen
"""

def generate_1bit_image(prompt,
                        size=None,
                        model=default_model,
                        quality=default_quality,
                        n=n):

    prompt = custom_instructions + "\n---\n" + prompt
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        n=n,
    )

    image_url = response.data[0].url
    return Image.open(requests.get(image_url, stream=True).raw)


# if __name__ == "__main__":
    # prompt = "generate a face of a small kitten"
    # generate_1bit_image(prompt, size="1024x1024").show()

    # img = Image.open("/Users/arjunmahishi/Downloads/1bit.png")
    # resize_image(img, (128, 32)).show()
