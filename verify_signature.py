from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def verify_signature(file_to_verify):
    file_to_verify += '.txt'

    with open('public_key.pem', 'rb') as key_file:
        pem_data = key_file.read()

    with open('signature.bin', 'rb') as signature_file:
        signature_data = signature_file.read()

    with open(file_to_verify, 'rb') as message_file:
        message = message_file.read()

    public_key = serialization.load_pem_public_key(pem_data)
    public_key.verify(
        signature_data,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )