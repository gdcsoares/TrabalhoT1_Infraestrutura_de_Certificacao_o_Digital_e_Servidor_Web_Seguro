# scripts/create_root_and_intermediate.py
from cryptography import x509
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime

def write_key(key, path, password=None):
    enc = serialization.BestAvailableEncryption(password.encode()) if password else serialization.NoEncryption()
    with open(path, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=enc
        ))

def write_pem(data, path):
    with open(path, "wb") as f:
        f.write(data.public_bytes(serialization.Encoding.PEM))

# 1) Root CA
root_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
root_name = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"BR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"ES"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Vitoria"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Minha Root CA"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"Minha Root CA")
])
root_cert = (
    x509.CertificateBuilder()
    .subject_name(root_name)
    .issuer_name(root_name)
    .public_key(root_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow() - datetime.timedelta(days=1))
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))  # 10 anos
    .add_extension(x509.BasicConstraints(ca=True, path_length=1), critical=True)
    .add_extension(x509.KeyUsage(digital_signature=True, key_encipherment=False,
                                 content_commitment=False, data_encipherment=False,
                                 key_agreement=False, key_cert_sign=True, crl_sign=True,
                                 encipher_only=False, decipher_only=False), critical=True)
    .sign(root_key, hashes.SHA256())
)

# 2) Intermediária (signed by root)
inter_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
inter_name = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"BR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"ES"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Vitoria"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Minha Inter CA"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"Minha Intermediaria CA")
])
inter_cert = (
    x509.CertificateBuilder()
    .subject_name(inter_name)
    .issuer_name(root_cert.subject)
    .public_key(inter_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow() - datetime.timedelta(days=1))
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))
    .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
    .add_extension(x509.KeyUsage(digital_signature=True, key_encipherment=False,
                                 content_commitment=False, data_encipherment=False,
                                 key_agreement=False, key_cert_sign=True, crl_sign=True,
                                 encipher_only=False, decipher_only=False), critical=True)
    .sign(root_key, hashes.SHA256())
)

# Save keys and certs
open("certs/root.pem","wb").write(root_cert.public_bytes(serialization.Encoding.PEM))
write_key(root_key, "certs/root.key")
open("certs/interm.pem","wb").write(inter_cert.public_bytes(serialization.Encoding.PEM))
write_key(inter_key, "certs/interm.key")

print("Root and Intermediate generated in certs/: root.pem, root.key, interm.pem, interm.key")