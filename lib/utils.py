# from io import BytesIO
# from PIL import Image

import asyncio


# def image_to_binary(image):
#     with BytesIO() as buffer:
#         image.save(buffer, format='PNG')
#         return buffer.getvalue()


def create_loop_async():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop
