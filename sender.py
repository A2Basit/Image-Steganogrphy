import socket
from PIL import Image
import random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def aes_encrypt(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return ciphertext


def encode_image(image_path, message):

    #open the image and convert to bytes
    img = Image.open(image_path)
    width, height = img.size
    image_bytes = img.tobytes()

    # Generate a random 128-bit key and an integer n
    key = get_random_bytes(16)
    n = random.randint(2, 9)

    #convert the message to cipher
    message = aes_encrypt(message, key)
    # print("The cipher is = ", message)
    # print("The key is ", key)

    # Convert n, cipher and key to bits for steganography
    n_bits = format(n, "08b")
    key_bits = "".join(format(b, "08b") for b in key)
    message_bits = "".join(format(b, "08b") for b in message)
    # print("The cipher binary is = ", message_bits)
    # print("The key binary is ", key_bits)

    #->CHECKS   
    if len(message_bits) > len(image_bytes) - 8:  # Reserve the first 8 pixels for n
        raise ValueError("Message is too large to be encoded in the image")

    encoded_pixels = bytearray(image_bytes)

    #->ENCODING n
    # Replace the least significant bits of the first 8 pixels with the bits of n
    for i in range(8):
        pixel = image_bytes[i]
        bit = n_bits[i]
        new_pixel = (pixel & 0xFE) | int(bit)
        encoded_pixels[i] = new_pixel

    #->ENCODING MESSAGE
    # after we have embedded the random integer n successfully, we now encode the image with the message we wish to send.
    index = 8
    used_bytes = []
    for m in message_bits:
        pixel = image_bytes[index]
        used_bytes.append(index) #noting down the bytes we have altered
        new_pixel = (pixel & 0xFE) | int(m)
        encoded_pixels[index] = new_pixel
        index += n
    
    #after we are done putting in our message we need to indicate an end to it. "index" is the last place where we put the message, now we put a 11001100 using the same formula
    pixel = image_bytes[index + n]
    used_bytes.append(index)
    new_pixel = 0b11001100
    encoded_pixels[index] = new_pixel
    
    #->ENCODING KEY
    # after we have embedded the random integer n successfully, we now encode the image with the key.
    index = 9
    for k in key_bits:
        if index in used_bytes: #check to ensure that the byte of the image we are about to alter has not already been altered
            index += n
        else:
            pixel = image_bytes[index]
            new_pixel = (pixel & 0xFE) | int(k)
            encoded_pixels[index] = new_pixel
            index += n

    #now we indicate the end of the key with 10101010
    pixel = image_bytes[index + n]
    used_bytes.append(index)
    new_pixel = 0b10101010
    encoded_pixels[index] = new_pixel

    # Create a new image with the encoded pixels
    encoded_image = Image.frombytes("RGB", (width, height), bytes(encoded_pixels))
    return encoded_image

def send_encoded_image(image_path, message, receiver_ip, receiver_port):
    encoded_image = encode_image(image_path, message)
    encoded_image.save("encoded_image.png")

    # Send encoded image over UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        with open("encoded_image.png", "rb") as f:
            data = f.read()
            sock.sendto(data, (receiver_ip, receiver_port))
            print("Encoded image sent to receiver.")

# Example usage:
image_to_send_path = "original.jpg"
message_to_hide = "Hello0000000000000000000!"
receiver_ip = "127.0.0.1"  # IP address of the receiver
receiver_port = 12345  # UDP port of the receiver
send_encoded_image(image_to_send_path, message_to_hide, receiver_ip, receiver_port)