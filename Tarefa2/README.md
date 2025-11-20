# Trabalho de Segurança da Computação - Tarefa 2

Este projeto demonstra a criação completa de uma infraestrutura de
chaves públicas (PKI) usando **OpenSSL**, incluindo:

-   Geração de **Root CA**
-   Geração de **Intermediate CA**
-   Emissão de **certificado de servidor**
-   Geração automática via scripts Shell
-   Ambiente HTTPS usando **Nginx + Docker**
-   Cadeia completa de certificação (server → intermediate → root)

## Estrutura do Projeto

    pki-openssl/
    ├── docker-compose.yml
    ├── nginx/
    │   ├── Dockerfile
    │   ├── default.conf
    │   └── index.html
    ├── scripts/
    │   ├── create_root_ca.sh
    │   ├── create_intermediate_ca.sh
    │   ├── create_server_cert.sh
    │   └── setup_all.sh
    └── certs/
        ├── root/
        │   ├── rootCA.key
        │   └── rootCA.crt
        ├── intermediate/
        │   ├── intermediateCA.key
        │   └── intermediateCA.crt
        └── server/
            ├── server.key
            ├── server.crt
            └── server-chain.crt

## 1. Pré-requisitos

-   **Linux ou WSL**
-   **OpenSSL** instalado
-   **Docker** e **Docker Compose**

## 2. Gerando os Certificados

Os certificados podem ser criados **individualmente** ou
**automaticamente** usando o script principal.

### 2.1 Execução completa:

    chmod +x scripts/*.sh
    ./scripts/setup_all.sh

### 3. Execução Manual

#### 3.1 Criar Root CA

    ./scripts/create_root_ca.sh

#### 3.2 Criar Intermediate CA

    ./scripts/create_intermediate_ca.sh

#### 3.3 Criar Certificado do Servidor

    ./scripts/create_server_cert.sh

## 4. Subindo o Servidor HTTPS com Docker

    docker-compose up --build

Acesse: https://localhost

## 5. Tornando o HTTPS Confiável

Importe:

    certs/root/rootCA.crt

## 6. Finalidade do Projeto

Demonstração de uma PKI completa com OpenSSL + Docker + Nginx.
