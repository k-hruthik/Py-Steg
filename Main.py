from PIL import Image

def embed_data(image_path, output_path, data):
    # Open the image
    image = Image.open(image_path)
    # Convert the image to RGBA mode if it's not already in that mode
    image = image.convert("RGBA")
    
    # Create a new image to store the modified pixels
    new_image = image.copy()
    pixels = new_image.load()
    
    # Convert the data to binary
    binary_data = ''.join(format(ord(i), '08b') for i in data)
    binary_data += '1111111111111110'  # Delimiter to mark the end of the hidden data
    
    data_index = 0
    binary_len = len(binary_data)
    
    for y in range(image.height):
        for x in range(image.width):
            if data_index < binary_len:
                r, g, b, a = image.getpixel((x, y))
                # Modify the least significant bit of each color channel
                new_r = (r & ~1) | int(binary_data[data_index])
                new_g = (g & ~1) | int(binary_data[data_index + 1])
                new_b = (b & ~1) | int(binary_data[data_index + 2])
                pixels[x, y] = (new_r, new_g, new_b, a)
                data_index += 3
            else:
                break
    
    new_image.save(output_path)
    print("Data embedded and image saved to", output_path)

def extract_data(image_path):
    # Open the image
    image = Image.open(image_path)
    pixels = image.load()
    
    binary_data = ""
    
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = image.getpixel((x, y))
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)
    
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-2:] == "~~":  # End of message delimiter
            break
    
    return decoded_data[:-2]

# Example usage
embed_data('input_image.png', 'output_image.png', 'Hello, this is a hidden message~~')
extracted_message = extract_data('output_image.png')
print("Extracted message:", extracted_message)
