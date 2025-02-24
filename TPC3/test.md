# EngWeb2025-A104005 - TPC2

# Título
Escola de música

# Data
17 de Fevereiro de 2025

# Autor  
**Nome:** Tomás Araújo Santos 
**Número:** 104005
![Foto do Autor](../extra/foto.jpeg)

# Resumo (`escola-musica.js`)

- Cria um servidor HTTP utilizando Node.js
- Ouve requisições na porta `1234`
- Usa `axios` para consumir a API do `json-server` em `http://localhost:3001`
- Processa requisições `GET` para várias rotas principais:
  - `/` → Retorna a página principal
  - `/alunos` → Retorna uma página HTML com uma lista de alunos
  - `/cursos` → Retorna uma página HTML com uma lista de cursos
  - `/instrumentos` → Retorna uma página HTML com uma lista de instrumentos
  - `/cursos/:id` → Retorna uma página HTML com uma lista de alunos de um curso específico
  - `/instrumentos/:id` → Retorna uma página HTML com uma lista de alunos que tocam um instrumento específico
  - `/alunos/:id` → Retorna uma página HTML com detalhes de um aluno específico
  - `/w3.css` → Retorna o arquivo CSS
  - `/favicon.ico` → Retorna o ícone do site
- Trata erros caso a API esteja indisponível
- Retorna `404 Not Found` para URLs inválidas
- Imprime no terminal o método HTTP e a URL da requisição para debug

# Testes no Browser
- `http://localhost:1234/alunos` → Exibe a lista de alunos
- `http://localhost:1234/cursos` → Exibe a lista de cursos
- `http://localhost:1234/instrumentos` → Exibe a lista de instrumentos

# Lista de Resultados
- [Código-fonte](escola-musica.js)
- [Base de dados](db.json)