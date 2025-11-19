# scripts/issue_server_cert.py
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
from cryptography.x509 import DNSName, SubjectAlternativeName

# carregar chave/cert da CA intermediária
with open("certs/interm.key","rb") as f:
    interm_key = serialization.load_pem_private_key(f.read(), password=None)
with open("certs/interm.pem","rb") as f:
    interm_cert = x509.load_pem_x509_certificate(f.read())

# gerar server key
server_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
open("certs/server.key","wb").write(server_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
))

# construir CSR (opcional) ou construir cert direto
subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"BR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"ES"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Vitoria"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Servidor Local"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"localhost")
])

csr = x509.CertificateSigningRequestBuilder().subject_name(subject).add_extension(
    SubjectAlternativeName([DNSName(u"localhost"), DNSName(u"127.0.0.1")]), critical=False
).sign(server_key, hashes.SHA256())

# emitir certificado assinado pela intermediária
server_cert = (
    x509.CertificateBuilder()
    .subject_name(csr.subject)
    .issuer_name(interm_cert.subject)
    .public_key(csr.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow() - datetime.timedelta(days=1))
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=825))
    .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
    .add_extension(x509.KeyUsage(digital_signature=True, key_encipherment=True,
                                 content_commitment=False, data_encipherment=False,
                                 key_agreement=False, key_cert_sign=False, crl_sign=False,
                                 encipher_only=False, decipher_only=False), critical=True)
    .add_extension(SubjectAlternativeName([DNSName(u"localhost"), DNSName(u"127.0.0.1")]), critical=False)
    .sign(interm_key, hashes.SHA256())
)

open("certs/server.crt","wb").write(server_cert.public_bytes(serialization.Encoding.PEM))

# chain: server.crt + interm.pem
with open("certs/chain.pem","wb") as f:
    f.write(server_cert.public_bytes(serialization.Encoding.PEM))
    f.write(open("certs/interm.pem","rb").read())

print("Server cert generated: certs/server.key, certs/server.crt, certs/chain.pem")
