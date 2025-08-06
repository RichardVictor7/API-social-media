# 📚 Documentação da API Social Media

## 🎯 Visão Geral

Esta API REST foi construída com **Django** e **Django REST Framework** para gerenciamento de posts de rede social. Ela fornece endpoints completos para operações CRUD (Create, Read, Update, Delete) de posts.

---

## 🌐 Informações da API

- **Base URL**: `http://127.0.0.1:8000`
- **Content-Type**: `application/json`
- **Paginação**: Automática (20 itens por página)
- **Formato de Resposta**: JSON
- **Upload de Imagens**: Suportado (multipart/form-data)

---

## 📋 Estrutura de Dados

### Post Object
```typescript
interface Post {
  id: number;
  nome: string;           // Máximo 50 caracteres
  imagem: string | null;  // URL da imagem ou null
  cor: string;           // Código de cor (ex: "#FF5733")
  comentario: string;    // Texto do post
  data_criacao: string;  // ISO 8601 timestamp
}
```

### Paginated Response
```typescript
interface PaginatedResponse<T> {
  count: number;         // Total de itens
  next: string | null;   // URL da próxima página
  previous: string | null; // URL da página anterior
  results: T[];          // Array de itens
}
```

---

## 🔗 Endpoints da API

### 1. 📄 Feed de Posts
**Obter todos os posts com paginação**

- **URL**: `GET /posts/feed/`
- **Descrição**: Retorna todos os posts paginados
- **Autenticação**: Não requerida
- **Paginação**: Sim (20 itens por página)

#### Request
```typescript
// Sem parâmetros obrigatórios
const response = await fetch('http://127.0.0.1:8000/posts/feed/');

// Com parâmetros de paginação
const response = await fetch('http://127.0.0.1:8000/posts/feed/?page=2');
```

#### Response (200 OK)
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/posts/feed/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "nome": "Meu Primeiro Post",
      "imagem": "http://127.0.0.1:8000/media/posts/imagem.jpg",
      "cor": "#FF5733",
      "comentario": "Este é um comentário de exemplo",
      "data_criacao": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Exemplo React/TypeScript
```typescript
interface Post {
  id: number;
  nome: string;
  imagem: string | null;
  cor: string;
  comentario: string;
  data_criacao: string;
}

interface FeedResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Post[];
}

const fetchFeed = async (page: number = 1): Promise<FeedResponse> => {
  const response = await fetch(`http://127.0.0.1:8000/posts/feed/?page=${page}`);
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
};

// Uso no componente
const [posts, setPosts] = useState<Post[]>([]);
const [loading, setLoading] = useState(false);

useEffect(() => {
  const loadPosts = async () => {
    setLoading(true);
    try {
      const data = await fetchFeed(1);
      setPosts(data.results);
    } catch (error) {
      console.error('Erro ao carregar posts:', error);
    } finally {
      setLoading(false);
    }
  };
  
  loadPosts();
}, []);
```

---

### 2. ➕ Criar Post
**Criar um novo post**

- **URL**: `POST /posts/`
- **Descrição**: Cria um novo post no sistema
- **Autenticação**: Não requerida
- **Content-Type**: `application/json` ou `multipart/form-data`

#### Request (JSON)
```typescript
// Dados obrigatórios
const postData = {
  nome: "Título do Post",      // Obrigatório (max 50 chars)
  cor: "#FF5733",             // Obrigatório
  comentario: "Texto do post"  // Obrigatório
};

const response = await fetch('http://127.0.0.1:8000/posts/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(postData)
});
```

#### Request (com Imagem)
```typescript
// Com upload de imagem
const formData = new FormData();
formData.append('nome', 'Post com Imagem');
formData.append('cor', '#FF5733');
formData.append('comentario', 'Texto do post');
formData.append('imagem', file); // File object

const response = await fetch('http://127.0.0.1:8000/posts/', {
  method: 'POST',
  body: formData // Não incluir Content-Type header
});
```

#### Response (201 Created)
```json
{
  "id": 5,
  "nome": "Título do Post",
  "imagem": "http://127.0.0.1:8000/media/posts/imagem.jpg",
  "cor": "#FF5733",
  "comentario": "Texto do post",
  "data_criacao": "2024-01-15T10:35:00Z"
}
```

#### Response (400 Bad Request)
```json
{
  "nome": ["Este campo é obrigatório."],
  "cor": ["Este campo é obrigatório."],
  "comentario": ["Este campo é obrigatório."]
}
```

#### Exemplo React/TypeScript
```typescript
interface CreatePostData {
  nome: string;
  cor: string;
  comentario: string;
  imagem?: File;
}

const createPost = async (data: CreatePostData): Promise<Post> => {
  let body: string | FormData;
  let headers: HeadersInit = {};
  
  if (data.imagem) {
    // Upload com imagem
    const formData = new FormData();
    formData.append('nome', data.nome);
    formData.append('cor', data.cor);
    formData.append('comentario', data.comentario);
    formData.append('imagem', data.imagem);
    body = formData;
  } else {
    // Upload sem imagem
    headers['Content-Type'] = 'application/json';
    body = JSON.stringify({
      nome: data.nome,
      cor: data.cor,
      comentario: data.comentario
    });
  }
  
  const response = await fetch('http://127.0.0.1:8000/posts/', {
    method: 'POST',
    headers,
    body
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(JSON.stringify(errorData));
  }
  
  return response.json();
};

// Uso no componente
const handleSubmit = async (formData: CreatePostData) => {
  try {
    const newPost = await createPost(formData);
    // Atualizar lista de posts
    setPosts(prev => [newPost, ...prev]);
  } catch (error) {
    console.error('Erro ao criar post:', error);
  }
};
```

---

### 3. 👁️ Obter Post Específico
**Obter detalhes de um post específico**

- **URL**: `GET /posts/{id}/detail/`
- **Descrição**: Retorna os detalhes completos de um post específico
- **Autenticação**: Não requerida
- **Parâmetros**: `id` (number) - ID do post

#### Request
```typescript
const postId = 5;
const response = await fetch(`http://127.0.0.1:8000/posts/${postId}/detail/`);
```

#### Response (200 OK)
```json
{
  "id": 5,
  "nome": "Título do Post",
  "imagem": "http://127.0.0.1:8000/media/posts/imagem.jpg",
  "cor": "#FF5733",
  "comentario": "Texto do post",
  "data_criacao": "2024-01-15T10:35:00Z"
}
```

#### Response (404 Not Found)
```json
{
  "detail": "Não encontrado."
}
```

#### Exemplo React/TypeScript
```typescript
const fetchPost = async (id: number): Promise<Post> => {
  const response = await fetch(`http://127.0.0.1:8000/posts/${id}/detail/`);
  
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Post não encontrado');
    }
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
};

// Uso no componente
const [post, setPost] = useState<Post | null>(null);
const [loading, setLoading] = useState(false);

useEffect(() => {
  const loadPost = async () => {
    setLoading(true);
    try {
      const data = await fetchPost(postId);
      setPost(data);
    } catch (error) {
      console.error('Erro ao carregar post:', error);
    } finally {
      setLoading(false);
    }
  };
  
  if (postId) {
    loadPost();
  }
}, [postId]);
```

---

### 4. ✏️ Atualizar Post
**Atualizar um post existente**

- **URL**: `PUT /posts/{id}/`
- **Descrição**: Atualiza um post existente (campos parciais)
- **Autenticação**: Não requerida
- **Content-Type**: `application/json`
- **Parâmetros**: `id` (number) - ID do post

#### Request
```typescript
const postId = 5;
const updateData = {
  nome: "Título Atualizado",
  comentario: "Texto atualizado"
  // Campos não incluídos permanecem inalterados
};

const response = await fetch(`http://127.0.0.1:8000/posts/${postId}/`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(updateData)
});
```

#### Response (200 OK)
```json
{
  "id": 5,
  "nome": "Título Atualizado",
  "imagem": "http://127.0.0.1:8000/media/posts/imagem.jpg",
  "cor": "#FF5733",
  "comentario": "Texto atualizado",
  "data_criacao": "2024-01-15T10:35:00Z"
}
```

#### Response (404 Not Found)
```json
{
  "detail": "Não encontrado."
}
```

#### Response (400 Bad Request)
```json
{
  "nome": ["Este campo é obrigatório."]
}
```

#### Exemplo React/TypeScript
```typescript
interface UpdatePostData {
  nome?: string;
  cor?: string;
  comentario?: string;
}

const updatePost = async (id: number, data: UpdatePostData): Promise<Post> => {
  const response = await fetch(`http://127.0.0.1:8000/posts/${id}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  });
  
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Post não encontrado');
    }
    const errorData = await response.json();
    throw new Error(JSON.stringify(errorData));
  }
  
  return response.json();
};

// Uso no componente
const handleUpdate = async (id: number, updateData: UpdatePostData) => {
  try {
    const updatedPost = await updatePost(id, updateData);
    // Atualizar post na lista
    setPosts(prev => prev.map(post => 
      post.id === id ? updatedPost : post
    ));
  } catch (error) {
    console.error('Erro ao atualizar post:', error);
  }
};
```

---

### 5. 🗑️ Deletar Post
**Remover um post do sistema**

- **URL**: `DELETE /posts/{id}/`
- **Descrição**: Remove permanentemente um post
- **Autenticação**: Não requerida
- **Parâmetros**: `id` (number) - ID do post

#### Request
```typescript
const postId = 5;
const response = await fetch(`http://127.0.0.1:8000/posts/${postId}/`, {
  method: 'DELETE'
});
```

#### Response (204 No Content)
- Resposta vazia, apenas status 204 indica sucesso

#### Response (404 Not Found)
```json
{
  "detail": "Não encontrado."
}
```

#### Exemplo React/TypeScript
```typescript
const deletePost = async (id: number): Promise<void> => {
  const response = await fetch(`http://127.0.0.1:8000/posts/${id}/`, {
    method: 'DELETE'
  });
  
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Post não encontrado');
    }
    throw new Error(`HTTP error! status: ${response.status}`);
  }
};

// Uso no componente
const handleDelete = async (id: number) => {
  try {
    await deletePost(id);
    // Remover post da lista
    setPosts(prev => prev.filter(post => post.id !== id));
  } catch (error) {
    console.error('Erro ao deletar post:', error);
  }
};
```

---

## 🔧 Configuração para React/TypeScript

### 1. Configuração de CORS
Para desenvolvimento local, adicione ao `settings.py`:

```python
INSTALLED_APPS = [
    # ... outras apps
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ... outros middlewares
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React default
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite default
    "http://127.0.0.1:5173",
]
```

### 2. Cliente HTTP (Axios)
```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para tratamento de erros
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data);
    return Promise.reject(error);
  }
);

export default api;
```

### 3. Hooks Customizados
```typescript
// hooks/usePosts.ts
import { useState, useEffect } from 'react';
import api from '../services/api';

export const usePosts = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPosts = async (page: number = 1) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.get(`/posts/feed/?page=${page}`);
      setPosts(response.data.results);
    } catch (err) {
      setError('Erro ao carregar posts');
    } finally {
      setLoading(false);
    }
  };

  const createPost = async (data: CreatePostData) => {
    try {
      const response = await api.post('/posts/', data);
      setPosts(prev => [response.data, ...prev]);
      return response.data;
    } catch (err) {
      throw err;
    }
  };

  const updatePost = async (id: number, data: UpdatePostData) => {
    try {
      const response = await api.put(`/posts/${id}/`, data);
      setPosts(prev => prev.map(post => 
        post.id === id ? response.data : post
      ));
      return response.data;
    } catch (err) {
      throw err;
    }
  };

  const deletePost = async (id: number) => {
    try {
      await api.delete(`/posts/${id}/`);
      setPosts(prev => prev.filter(post => post.id !== id));
    } catch (err) {
      throw err;
    }
  };

  return {
    posts,
    loading,
    error,
    fetchPosts,
    createPost,
    updatePost,
    deletePost,
  };
};
```

---

## 🚨 Códigos de Status HTTP

| Código | Significado | Descrição |
|--------|-------------|-----------|
| 200 | OK | Requisição bem-sucedida |
| 201 | Created | Recurso criado com sucesso |
| 204 | No Content | Requisição bem-sucedida, sem conteúdo |
| 400 | Bad Request | Dados inválidos enviados |
| 404 | Not Found | Recurso não encontrado |
| 500 | Internal Server Error | Erro interno do servidor |

---

## 📝 Exemplos de Uso Completo

### Componente de Lista de Posts
```typescript
import React, { useEffect } from 'react';
import { usePosts } from '../hooks/usePosts';

const PostList: React.FC = () => {
  const { posts, loading, error, fetchPosts } = usePosts();

  useEffect(() => {
    fetchPosts();
  }, []);

  if (loading) return <div>Carregando...</div>;
  if (error) return <div>Erro: {error}</div>;

  return (
    <div>
      {posts.map(post => (
        <div key={post.id} style={{ backgroundColor: post.cor }}>
          <h3>{post.nome}</h3>
          <p>{post.comentario}</p>
          {post.imagem && <img src={post.imagem} alt={post.nome} />}
          <small>{new Date(post.data_criacao).toLocaleDateString()}</small>
        </div>
      ))}
    </div>
  );
};
```

### Componente de Criação de Post
```typescript
import React, { useState } from 'react';
import { usePosts } from '../hooks/usePosts';

const CreatePost: React.FC = () => {
  const { createPost } = usePosts();
  const [formData, setFormData] = useState({
    nome: '',
    cor: '#FF5733',
    comentario: '',
    imagem: null as File | null
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const data = formData.imagem 
        ? new FormData() // Para upload de imagem
        : formData; // Para dados JSON
      
      await createPost(data);
      setFormData({ nome: '', cor: '#FF5733', comentario: '', imagem: null });
    } catch (error) {
      console.error('Erro ao criar post:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Nome do post"
        value={formData.nome}
        onChange={e => setFormData(prev => ({ ...prev, nome: e.target.value }))}
        required
      />
      <input
        type="color"
        value={formData.cor}
        onChange={e => setFormData(prev => ({ ...prev, cor: e.target.value }))}
      />
      <textarea
        placeholder="Comentário"
        value={formData.comentario}
        onChange={e => setFormData(prev => ({ ...prev, comentario: e.target.value }))}
        required
      />
      <input
        type="file"
        accept="image/*"
        onChange={e => setFormData(prev => ({ 
          ...prev, 
          imagem: e.target.files?.[0] || null 
        }))}
      />
      <button type="submit">Criar Post</button>
    </form>
  );
};
```

---

## 🔍 Debugging e Troubleshooting

### 1. Verificar se a API está rodando
```bash
curl http://127.0.0.1:8000/posts/feed/
```

### 2. Verificar logs do Django
```bash
# No terminal onde o servidor está rodando
# Os logs aparecem automaticamente
```

### 3. Testar endpoints individualmente
```bash
# Testar criação
curl -X POST http://127.0.0.1:8000/posts/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"Teste","cor":"#FF5733","comentario":"Teste"}'
```

### 4. Verificar CORS
- Certifique-se de que o CORS está configurado corretamente
- Verifique se a URL do frontend está na lista de `CORS_ALLOWED_ORIGINS`

---

## 📚 Recursos Adicionais

- **Django REST Framework**: https://www.django-rest-framework.org/
- **CORS Headers**: https://github.com/adamchainz/django-cors-headers
- **React Query**: Para cache e gerenciamento de estado
- **Axios**: Cliente HTTP robusto para React

---

## 🎯 Próximos Passos

1. **Implementar autenticação** (JWT, OAuth)
2. **Adicionar validações** mais robustas
3. **Implementar cache** (Redis)
4. **Adicionar testes** automatizados
5. **Configurar CI/CD**
6. **Deploy em produção**

---

*Esta documentação foi criada especificamente para integração com React/TypeScript. Para dúvidas ou sugestões, consulte a documentação oficial do Django REST Framework.* 