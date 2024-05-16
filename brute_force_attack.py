import time
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def aes_decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode('utf-8')

def extract_bits(image_bytes, start_index, stop_byte):
    bits = []
    for i in range(start_index, len(image_bytes)):
        if image_bytes[i] == stop_byte:
            break
        bits.append(str(image_bytes[i] & 1))
    return bits

def brute_force_decode(image_path):
    img = Image.open(image_path)
    image_bytes = img.tobytes()

    successful_attempts = []

    start_time = time.time()

    try:
        stop_byte_for_cipher = 204
        stop_byte_for_key = 170
        total_attempts = 2^len(image_bytes)
        progress_interval = total_attempts // 1000  # Print progress every 10% of total attempts

        # Attempt to extract the key and the cipher from the image
        numberList=[2,3,4,5,6,7,8,9]
        for number in numberList:
            for index, _ in enumerate(image_bytes):
                if index % progress_interval == 0:
                    progress = (index / total_attempts) * 100
                    print(f"Progress: {progress:.2f}%")

                key_bits = extract_bits(image_bytes, index + number, stop_byte_for_key)
                if len(key_bits) != 128:
                    continue

                cipher_bits = extract_bits(image_bytes, index+ number, stop_byte_for_cipher)
                if len(cipher_bits) % 8 != 0:
                    continue

                # Convert key and cipher bits to bytes
                key_bytes = bytes(int(''.join(key_bits[i:i+8]), 2) for i in range(0, len(key_bits), 8))
                cipher_bytes = bytes(int(''.join(cipher_bits[i:i+8]), 2) for i in range(0, len(cipher_bits), 8))

            # Decrypt the cipher using the key
                message = aes_decrypt(cipher_bytes, key_bytes)
                successful_attempts.append(message)
                print(f"Successfully decoded: {message}")

    except Exception as e:
        print(f"Failed attempt with: {str(e)}")

    end_time = time.time()
    print(f"Brute force attack completed in {end_time - start_time} seconds")
    print(f"Successful attempts: {successful_attempts}")

# Example usage:
received_image_path = "encoded_image.png"
brute_force_decode(received_image_path)
