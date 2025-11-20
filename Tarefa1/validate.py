import ssl
import socket
import pprint

SERVER = "localhost"
PORT = 8443
CAFILE = "certs/root.pem"        
CHAINFILE = "certs/chain.pem"    

context = ssl.create_default_context(
    purpose=ssl.Purpose.SERVER_AUTH,
    cafile=CAFILE
)

context.load_verify_locations(cafile=CHAINFILE)

with socket.create_connection((SERVER, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=SERVER) as ssock:
        print("\n=== Conexão Estabelecida ===")
        print(f"Protocolo: {ssock.version()}")
        
        print("\n=== Certificado do Servidor ===")
        pprint.pprint(ssock.getpeercert())

        print("\n=== ✓ Cadeia de certificação validada com sucesso ===")
