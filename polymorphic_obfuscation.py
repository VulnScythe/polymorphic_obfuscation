import base64
import random
import bz2

def generate_polymorphic_payload(original_payload):
    try:
        compressed_payload = bz2.compress(original_payload.encode())
        encoded_payload = base64.b64encode(compressed_payload).decode()

        decryption_key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))

        encrypted_payload = ''.join([chr(ord(c) ^ ord(k)) for c, k in zip(encoded_payload, decryption_key * (len(encoded_payload) // len(decryption_key) + 1))])

        polymorphic_payload = f'''
import base64
import bz2

def decrypt_payload(encrypted_payload, key):
    decrypted = ''.join([chr(ord(c) ^ ord(k)) for c, k in zip(encrypted_payload, key * (len(encrypted_payload) // len(key) + 1))])
    decoded = base64.b64decode(decrypted)
    return bz2.decompress(decoded).decode()

exec(decrypt_payload({encrypted_payload!r}, {decryption_key!r}))
'''

        return polymorphic_payload

    except Exception as e:
        print(f"Error generating polymorphic payload: {e}")
        return None

original_payload = """
def harmless_function():
    print("Hello from the polymorphic demo!")

harmless_function()
"""

polymorphic_payload = generate_polymorphic_payload(original_payload)

if polymorphic_payload:
    with open('polymorphic_obfuscated.py', 'w') as f:
        f.write(polymorphic_payload)

    exec(polymorphic_payload)
else:
    print("Failed to generate polymorphic payload.")