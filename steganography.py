from PIL import Image

def encode_image(image_path, message, output_path):
    img = Image.open(image_path)
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')
    
    binary_msg = ''.join(format(ord(c), '08b') for c in message) + '1111111111111110'
    
    if len(binary_msg) > img.width * img.height * 3:
        raise ValueError("Message too large for image!")
    
    pixels = list(img.getdata())
    new_pixels = []
    msg_index = 0
    
    for pixel in pixels:
        if msg_index < len(binary_msg):
            new_pixel = list(pixel)
            for i in range(3):
                if msg_index < len(binary_msg):
                    new_pixel[i] = new_pixel[i] & ~1 | int(binary_msg[msg_index])
                    msg_index += 1
            new_pixels.append(tuple(new_pixel))
        else:
            new_pixels.append(pixel)
    
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    new_img.save(output_path, format='PNG')


def decode_image(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary_msg = ""
    
    for pixel in pixels:
        for channel in pixel[:3]:  # R, G, B channels
            binary_msg += str(channel & 1)
    
    delimiter = '1111111111111110'
    if delimiter in binary_msg:
        msg_bits = binary_msg.split(delimiter)[0]
        message = ""
        for i in range(0, len(msg_bits), 8):
            byte = msg_bits[i:i+8]
            message += chr(int(byte, 2))
        return message
    return "No hidden message found"
