#!/bin/bash
echo "🔐 Criando CA Raiz..."
mkdir -p ../certs/root
cd ../certs/root

openssl genrsa -out rootCA.key 4096
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.crt -subj "/C=BR/ST=ES/L=Vitoria/O=UFES/OU=DI/CN=Root CA"

echo "✅ CA Raiz criada: rootCA.key e rootCA.crt"
cd ../..