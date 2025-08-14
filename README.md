# API Social Media

Uma API REST completa para gerenciamento de posts de rede social, construída com Django e Django REST Framework.

## 📋 Descrição

Esta API permite criar, visualizar, atualizar e deletar posts de uma rede social. Cada post contém:
- **Nome**: Identificação do post
- **Imagem**: Upload de imagem (opcional)
- **Cor**: Cor associada ao post
- **Comentário**: Texto do post
- **Data de Criação**: Timestamp automático

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip

### Passos para instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd API-social-media
```

2. **Crie e ative um ambiente virtual**
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**
```bash
cd api
python manage.py migrate
```

5. **Crie um superusuário (opcional)**
```bash
python api/manage.py createsuperuser
```

6. **Execute o servidor**
```bash
python api/manage.py runserver
```

O servidor estará rodando em `http://127.0.0.1:8000/`

## 📚 Documentação da API

### Base URL
```
http://127.0.0.1:8000/
```

### Endpoints

#### 1. **Feed de Posts**
**GET** `/posts/feed/`

Retorna todos os posts com paginação.

**Resposta:**
```json
{
  "count": 10,
  "next": "http://127.0.0.1:8000/posts/feed/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "nome": "Meu Post",
      "imagem": "http://127.0.0.1:8000/media/posts/imagem.jpg",
      "cor": "#FF5733",
      "comentario": "Este é um comentário de exemplo",
      "data_criacao": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### 2. **Criar Post**
**POST** `/posts/`

Cria um novo post.

**Body (multipart/form-data):**
```json
{
  "nome": "Novo Post",
  "imagem": "[arquivo de imagem]",
  "cor": "#FF5733",
  "comentario": "Conteúdo do post"
}
```

**Resposta (201 Created):**
```json
{
  "id": 2,
  "nome": "Novo Post",
  "imagem": "http://127.0.0.1:8000/media/posts/nova_imagem.jpg",
  "cor": "#FF5733",
  "comentario": "Conteúdo do post",
  "data_criacao": "2024-01-15T10:35:00Z"
}
```

#### 3. **Obter Post Específico**
**GET** `/posts/{id}/detail/`

Retorna um post específico pelo ID.

**Resposta:**
```json
{
  "id": 1,
  "nome": "Meu Post",
  "imagem": "http://127.0.0.1:8000/media/posts/imagem.jpg",
  "cor": "#FF5733",
  "comentario": "Este é um comentário de exemplo",
  "data_criacao": "2024-01-15T10:30:00Z"
}
```

#### 4. **Atualizar Post**
**PUT** `/posts/{id}/`

Atualiza um post existente (campos parciais).

**Body:**
```json
{
  "nome": "Post Atualizado",
  "comentario": "Comentário atualizado"
}
```

**Resposta:**
```json
{
  "id": 1,
  "nome": "Post Atualizado",
  "imagem": "http://127.0.0.1:8000/media/posts/imagem.jpg",
  "cor": "#FF5733",
  "comentario": "Comentário atualizado",
  "data_criacao": "2024-01-15T10:30:00Z"
}
```

#### 5. **Deletar Post**
**DELETE** `/posts/{id}/`

Remove um post do sistema.

**Resposta:** `204 No Content`


## 📝 Estrutura do Projeto

```
API-social-media/
├── api/                    # Backend Django
│   ├── api/               # Configurações do projeto
│   │   ├── settings.py    # Configurações Django
│   │   ├── urls.py        # URLs principais
│   │   └── wsgi.py        # WSGI
│   ├── posts/             # App de posts
│   │   ├── models.py      # Modelo Post
│   │   ├── views.py       # Views da API
│   │   ├── serializers.py # Serializers
│   │   └── urls.py        # URLs dos posts
│   ├── manage.py          # Script Django
│   └── db.sqlite3         # Banco de dados
├── requirements.txt        # Dependências Python
└── README.md              # Documentação
```



## 🛠 Visualizando o Banco de Dados

### Ativar o Django Admin:
Criar um superusuário
```bash
python manage.py createsuperuser
```
Preencha nome, e-mail e senha.

Acessar o painel
```bash
http://127.0.0.1:8000/admin/
```
Entre com seu usuário e senha de superusuário que voce criou.

## 📄 Licença

Este projeto está sob a licença MIT.