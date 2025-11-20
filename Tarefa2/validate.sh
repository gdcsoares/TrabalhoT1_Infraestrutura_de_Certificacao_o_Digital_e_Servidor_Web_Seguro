#!/bin/bash

SERVER_CERT="certs/server/server.crt"
INT_CERT="certs/intermediate/intermediateCA.crt"
ROOT_CERT="certs/root/rootCA.crt"

echo "========================================"
echo " 🔍 VALIDAÇÃO SIMPLIFICADA DA CADEIA"
echo "========================================"
echo

# 1. Validar cadeia completa
echo "1️⃣  Validando a cadeia de certificação..."
openssl verify -CAfile "$ROOT_CERT" -untrusted "$INT_CERT" "$SERVER_CERT"
echo

# 2. Validar assinatura Server → Intermediate
echo "2️⃣  Validando assinatura do servidor pela Intermediate..."
SERVER_ISSUER=$(openssl x509 -in $SERVER_CERT -noout -issuer)
INT_SUBJECT=$(openssl x509 -in $INT_CERT -noout -subject)
echo "Issuer do servidor:   $SERVER_ISSUER"
echo "Subject da interm.:   $INT_SUBJECT"
echo

# 3. Validar assinatura Intermediate → Root
echo "3️⃣  Validando assinatura da Intermediate pela Root..."
INT_ISSUER=$(openssl x509 -in $INT_CERT -noout -issuer)
ROOT_SUBJECT=$(openssl x509 -in $ROOT_CERT -noout -subject)
echo "Issuer da interm.:    $INT_ISSUER"
echo "Subject da root:      $ROOT_SUBJECT"
echo
