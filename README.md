# Image Steganography

This project is a simple demonstration of sending an encoded image over a network, receiving it, and then attempting to decode it using a brute force method.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your machine. The project also uses the following Python libraries:

- PIL (Pillow)
- pycryptodome

You can install these using pip:

```bash
pip install pillow pycryptodome
```
## Running the Project
The project consists of three main Python scripts:

### sender.py:

This script encodes a message into an image and sends it over the network to a specified IP and port.
### receiver_new.py:

This script listens on a specified IP and port for an incoming image, saves it, and attempts to decode the message hidden in the image.
### brute_force_attack.py:

This script attempts to decode a message hidden in an image using a brute force method.
### Group Members:
Muhammad Aleem Siddique Khan
Muhammad Ahmad Raza Khan
