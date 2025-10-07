
# 🔄 ImgPDF - Conversor de Imagens e PDFs

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)]()

API REST simples e eficiente para conversão entre imagens e arquivos PDF, desenvolvida com Flask.

## 📋 Sumário

- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Endpoints da API](#-endpoints-da-api)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Testes](#-testes)
- [Docker](#-docker)
- [Estrutura do Projeto](#-estrutura-do-projeto)

## ✨ Funcionalidades

- 📸 **Imagem para PDF**: Converte imagens (PNG, JPG, JPEG, etc.) para formato PDF
- 📄 **PDF para Imagem**: Converte páginas de PDF em imagens PNG
  - Suporta PDFs com múltiplas páginas (retorna um arquivo ZIP)
  - PDFs de página única retornam uma única imagem PNG
- 🎨 Suporte a diversos formatos de imagem (RGB, RGBA, Palette, etc.)
- ⚡ Processamento rápido em memória (sem arquivos temporários)
- 🔒 Validação de entrada e tratamento de erros

## 🛠 Tecnologias

- **[Flask](https://flask.palletsprojects.com/)** - Framework web minimalista
- **[Pillow (PIL)](https://python-pillow.org/)** - Biblioteca de processamento de imagens
- **[pdf2image](https://github.com/Belval/pdf2image)** - Conversão de PDF para imagens
- **[pytest](https://pytest.org/)** - Framework de testes

## 📦 Requisitos

- Python 3.13+
- pip (gerenciador de pacotes Python)
- virtualenv
- Poppler (necessário para pdf2image)

### Instalação do Poppler

**Linux (Ubuntu/Debian):**
```bash 

sudo apt-get install poppler-utils
```

**macOS:**

```bash 

brew install poppler
```

**Windows:**
Baixe os binários do [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/) e adicione ao PATH.

## 🚀 Instalação

### 1. Clone o repositório

```bash 

git clone <seu-repositorio> cd imgpdf
```

### 2. Crie e ative o ambiente virtual

#### Criar ambiente virtual

```bash

python -m venv .venv
```

#### Ativar ambiente virtual

```bash

source .venv/bin/activate
```

#### Ativar no Windows

```bash

.venv\Scripts\activate
```

### 3. Instale as dependências

```bash 

pip install -r requirements.txt
```

### 3. Execute a aplicação

```bash 

python main.py
```
A aplicação estará disponível em `http://localhost:5000`

## 💻 Como Usar

### Iniciar o servidor

