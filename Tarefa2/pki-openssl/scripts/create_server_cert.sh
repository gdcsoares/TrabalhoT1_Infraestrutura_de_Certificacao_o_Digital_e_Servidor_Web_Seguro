#!/bin/bash
echo "🔐 Criando Certificado do Servidor..."
mkdir -p ../certs/server
cd ../certs/server

# Gerar chave
openssl genrsa -out server.key 4096

# Criar CSR
openssl req -new -key server.key -out server.csr -subj "/C=BR/ST=ES/L=Vitoria/O=UFES/OU=DI/CN=localhost"

# Criar arquivo de configuração
cat > server.cnf << EOF
basicConstraints=critical,CA:FALSE
keyUsage=digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid,issuer
subjectAltName=DNS:localhost,DNS:127.0.0.1
EOF

# Assinar com extensions
openssl x509 -req -in server.csr -CA ../intermediate/intermediateCA.crt -CAkey ../intermediate/intermediateCA.key -CAcreateserial -out server.crt -days 365 -sha256 -extfile server.cnf

# Criar certificado combinado
cat server.crt ../intermediate/intermediateCA.crt > server-chain.crt

# Limpar
rm server.csr server.cnf ../intermediate/intermediateCA.srl

echo "✅ Certificado do servidor criado:"
echo "   - server.key"
echo "   - server.crt" 
echo "   - server-chain.crt (cadeia completa)"
cd ../..