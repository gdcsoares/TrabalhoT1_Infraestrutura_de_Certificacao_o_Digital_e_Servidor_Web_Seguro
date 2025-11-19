#!/bin/bash
echo "🏗️  Iniciando configuração completa da PKI..."
echo "================================================"

# Dar permissão de execução aos scripts
chmod +x *.sh

# Executar na ordem
echo "📝 Etapa 1: Criando CA Raiz..."
./create_root_ca.sh

echo "📝 Etapa 2: Criando CA Intermediária..."
./create_intermediate_ca.sh

echo "📝 Etapa 3: Criando Certificado do Servidor..."
./create_server_cert.sh

echo ""
echo "🔍 Validando certificados..."
echo "----------------------------"

# Validar CA Intermediária
echo "✅ Validando CA Intermediária:"
openssl verify -CAfile ../certs/root/rootCA.crt ../certs/intermediate/intermediateCA.crt

# Validar certificado do servidor
echo "✅ Validando Certificado do Servidor:"
openssl verify -CAfile ../certs/root/rootCA.crt -untrusted ../certs/intermediate/intermediateCA.crt ../certs/server/server.crt

echo ""
echo "🎉 Configuração completa!"
echo "📁 Certificados criados em: ../certs/"
echo "🚀 Para iniciar o servidor: sudo docker-compose up --build"
echo "🌐 Acesse: https://localhost:8443"