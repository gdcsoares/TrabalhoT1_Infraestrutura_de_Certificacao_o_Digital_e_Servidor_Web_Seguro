# Trabalho de Segurança da Computação - Tarefa 1

Este passo a passo explica como executar o projeto, gerar certificados, subir o ambiente com Docker e validar o funcionamento.

---

##  Estrutura do Projeto

```
Trab Seg Comp/
├── docker-compose.yml
├── nginx/
│   ├── Dockerfile
│   ├── default.conf
│   └── html/
│       └── index.html
├── validate.py
├── scripts/
│   ├── create_root_and_intermediate.py
│   └── issue_server_cert.py
└── certs/
    ├── root.pem / root.key
    ├── interm.pem / interm.key
    ├── server.crt / server.key
    └── chain.pem
```

---

##  1. Pré-requisitos

- **Docker** instalado
- **Docker Compose** instalado
- **Python 3.8+** (somente se for regenerar certificados)

---

##  2. Configurando o Ambiente

Antes de gerar certificados ou executar qualquer script, configure o ambiente Python.

### **2.1 Criar o ambiente virtual**

Na pasta raiz do projeto:

```bash
python3 -m venv venv
```

### **2.2 Ativar o ambiente virtual**

**Linux / macOS**:

```bash
source venv/bin/activate
```

**Windows (PowerShell)**:

```powershell
venv\Scripts\activate
```

### **2.3 Instalar as bibliotecas necessárias**

O projeto utiliza a biblioteca `cryptography` para gerar certificados:

```bash
pip install cryptography
```

---

## 3. Geração dos Certificados

Nesses passos serão gerados os certificados que ficarão salvos no diretório `certs/`

### **2.1 Criar Root CA e Intermediate CA**

Dentro da pasta `scripts/` execute:

```bash
python3 create_root_and_intermediate.py
```

Isso irá gerar:

- `root.pem`, `root.key`
- `interm.pem`, `interm.key`

### **2.2 Emitir o certificado do servidor**

Execute:

```bash
python3 issue_server_cert.py
```

Isso irá gerar:

- `server.crt`, `server.key`
- `chain.pem` (root + intermediate)

---

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

Para tornar segura, será necessário importar o certificado `root.pem` no navegador.

---

## 5. Testes

Você pode testar o certificado no diretório raiz por meio do script de validação:

```bash
python3 validate.py
```

Isso permite verificar:

- Certificado do servidor
- Cadeia de certificação

---

## 6. Finalidade do Trabalho

Com isso, nesse projeto foi possível demonstrar:

- Criação de hierarquia de certificados (Root, Intermediate e Server) em Python
- Configuração de servidor HTTPS usando Nginx
- Uso de Docker para empacotamento do ambiente

