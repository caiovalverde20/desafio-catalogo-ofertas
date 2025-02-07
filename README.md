# Desafio Catálogo de Ofertas

Este projeto é um catálogo de ofertas de produtos obtidos via web scraping no Mercado Livre. A aplicação permite visualizar e filtrar produtos com base em preço e desconto.

## Tecnologias Utilizadas
- **Django** como framework backend
- **PostgreSQL** como banco de dados (é possivel rodar a aplicação sem um banco de dados graças a um arquivo json que sera utilizado no lugar)
- **Selenium** para web scraping
- **Docker** para facilitar a execução
- **Gunicorn** como servidor WSGI para produção

## Executando o Projeto

### Com Docker
1. Clone este repositório:
   ```sh
   git clone https://github.com/caiovalverde20/desafio-catalogo-ofertas.git
   cd desafio-catalogo-ofertas
   ```

2. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```env
   DB_NAME=desafio_db
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=db
   DB_PORT=5432
   ```

3. Construa e inicie os containers Docker:
   ```sh
   docker-compose up --build
   ```

4. Aplique as migrações do banco de dados:
   ```sh
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
   ```

5. Acesse a aplicação em `http://localhost:8000`

### Sem Docker
1. Clone este repositório:
   ```sh
   git clone https://github.com/seu-usuario/desafio-catalogo-ofertas.git
   cd desafio-catalogo-ofertas
   ```

2. Crie e ative um ambiente virtual Python:
   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` e defina as variáveis do banco de dados (opcional se for usar JSON como fonte de dados):
   ```env
   DB_NAME=desafio_db
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. Aplique as migrações do banco de dados:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Inicie o servidor:
   ```sh
   python manage.py runserver
   ```

7. Acesse a aplicação em `http://localhost:8000`

## Uso do Banco de Dados ou JSON
Caso o banco de dados esteja vazio, o sistema carrega os produtos a partir de um arquivo JSON (`produtos.json`) que foram feitos a partir de uma raspagem, tornando o sistema utilizavel mesmo sem um banco de dados.

Na interface há um **botão de atualização** que vai executar o scraping e salvar os detalhes no banco de dados.

## Rotas Disponíveis
| Rota | Descrição |
|------|-------------|
| `/` | Exibe os produtos disponíveis |
| `/atualizar/` | Realiza o web scraping e atualiza o banco (utilizada no botão na pagina principal) |
| `/listar/` | Lista todos os produtos em JSON |
