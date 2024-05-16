import socket
import sys
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def aes_decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode('utf-8')

def decode_image(image_path):
    img = Image.open(image_path)
    image_bytes = img.tobytes()

    # Extract n from the first 8 pixels
    n_bits = [str(image_bytes[i] & 1) for i in range(8)]
    n = int(''.join(n_bits), 2)

    # Extract the key and the cipher from the image
    key_bits = []
    cipher_bits = []

    #the 8th index will have the first cipher bit and 9th will have the first key bit
    #first we get the cipher
    index = 8
    cipher_bits.append(str(image_bytes[index] & 1))
    for i in range(8, len(image_bytes)):
        if image_bytes[index + n] == 204:
            break
        else:
            cipher_bits.append(str(image_bytes[index + n] & 1))
            index += n
    
    #now we get the key
    index = 9
    key_bits.append(str(image_bytes[index] & 1))
    for i in range(9, len(image_bytes)):
        if image_bytes[index + n] == 170:
            break
        else:
            key_bits.append(str(image_bytes[index + n] & 1))
            index += n

    # Convert key and cipher bits to bytes
    key_bytes = bytes(int(''.join(key_bits[i:i+8]), 2) for i in range(0, len(key_bits), 8))
    cipher_bytes = bytes(int(''.join(cipher_bits[i:i+8]), 2) for i in range(0, len(cipher_bits), 8))

    # Decrypt the cipher using the key
    message = aes_decrypt(cipher_bytes, key_bytes)

    return message
    
def receive_encoded_image(output_image_path, listen_ip, listen_port):
    # Receive encoded image over UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((listen_ip, listen_port))
        print("Waiting to receive encoded image...")

        data, addr = sock.recvfrom(65536)  # Use a larger buffer size (e.g., 65536)
        with open(output_image_path, "wb") as f:
            f.write(data)

        print("Encoded image received successfully.")

        # Decode the received image to extract the hidden message
        decoded_message = decode_image(output_image_path)
        print("Decoded message:", decoded_message)

        # Exit the script
        sys.exit(0)

# Example usage:
received_image_path = "received_image.png"
listen_ip = "0.0.0.0"  # Listen on all available interfaces
listen_port = 12345  # UDP port to listen on
receive_encoded_image(received_image_path, listen_ip, listen_port)