#!/bin/bash
echo "🔐 Criando CA Intermediária..."
mkdir -p ../certs/intermediate
cd ../certs/intermediate

# Gerar chave
openssl genrsa -out intermediateCA.key 4096

# Criar CSR
openssl req -new -key intermediateCA.key -out intermediateCA.csr -subj "/C=BR/ST=ES/L=Vitoria/O=UFES/OU=DI/CN=Intermediate CA"

# Criar arquivo de configuração
cat > intermediate.cnf << EOF
basicConstraints=critical,CA:TRUE
keyUsage=critical,keyCertSign,cRLSign
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid:always,issuer
EOF

# Assinar com extensions
openssl x509 -req -in intermediateCA.csr -CA ../root/rootCA.crt -CAkey ../root/rootCA.key -CAcreateserial -out intermediateCA.crt -days 730 -sha256 -extfile intermediate.cnf

# Limpar
rm intermediateCA.csr intermediate.cnf ../root/rootCA.srl

echo "✅ CA Intermediária criada: intermediateCA.key e intermediateCA.crt"
cd ../..