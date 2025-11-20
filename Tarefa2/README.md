# Trabalho de Segurança da Computação - Tarefa 2

Este passo a passo explica como executar o projeto, gerar certificados, subir o ambiente com Docker e validar o funcionamento.

---

##  Estrutura do Projeto

```
pki-openssl/
├── docker-compose.yml
├── nginx/
│   ├── Dockerfile
│   ├── default.conf
│   └── index.html
├── validate.sh
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
```

---

##  1. Pré-requisitos

- **Linux** ou **WSL**
- **OpenSSL** instalado
- **Docker** e **Docker Compose**

---

## 2. Geração dos Certificados

Nesses passos serão gerados os certificados que ficarão salvos no diretório `certs/`

### **2.1 Execução completa**

Desenvolvelmos um script que fará todos os passos, basta executá-lo. No diretório `scripts/`:

```bash
chmod +x *.sh
./setup_all.sh
```

Isso irá:

- Criar Root CA
- Criar Intermediate CA
- Criar certificado do servidor
- Montar `server-chain.crt`

## 3. Subindo o Ambiente com Docker

Na raiz do projeto execute:

```bash
docker-compose up --build
```

Isso fará:

- Construir a imagem do Nginx
- Iniciar o servidor HTTPS local

---

## 4. Acessando o Servidor

Após subir os containers, abra no navegador:

```
https://localhost
```

Você verá a página `index.html` servida **via HTTPS** usando o certificado gerado.

Será possível observar que o navegador estará com uma navegação não segura.

Para tornar segura, será necessário importar o certificado `rootCA.crt` no navegador.

---

## 5. Testes

Você pode testar o certificado no diretório raiz por meio do script de validação:

```bash
chmod +x validate.sh
./validate.sh
```

Isso permite verificar:

- Se a cadeia de certificação é válida
- Se o servidor foi assinado pela Intermediate
- Se a Intermediate foi assinada pela Root

---

## 6. Finalidade do Trabalho

Com isso, nesse projeto foi possível demonstrar:

- Criar uma hierarquia PKI completa manualmente
- Assinar certificados usando Root e Intermediate
- Construir a cadeia de certificação `server-chain.crt`
- Configuração de servidor HTTPS usando Nginx
- Uso de Docker para empacotamento do ambiente
