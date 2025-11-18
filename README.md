# Classificador Inteligente de E-mails

Sistema de análise e classificação automática de e-mails do setor financeiro usando Inteligência Artificial. A aplicação classifica e-mails entre produtivos e improdutivos, além de sugerir respostas automáticas.

## Funcionalidades

- **Classificação Inteligente**: Classifica e-mails automaticamente em duas categorias:
  - **PRODUTIVO**: E-mails que requerem ação ou resposta (solicitações, dúvidas, reclamações)
  - **IMPRODUTIVO**: E-mails informativos ou de cortesia (agradecimentos, felicitações)

- **Sugestão de Respostas**: Gera automaticamente respostas profissionais e personalizadas com base no conteúdo do e-mail

- **Múltiplos Formatos**: Aceita entrada de texto direto ou upload de arquivos (.txt e .pdf)

- **Interface Moderna**: Interface web responsiva com modo claro/escuro

- **Indicador de Confiança**: Mostra o nível de confiança da análise realizada pela IA

## Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e de alta performance
- **OpenAI GPT-3.5**: Modelo de linguagem para classificação e geração de respostas
- **PyPDF2**: Extração de texto de arquivos PDF
- **Uvicorn**: Servidor ASGI de alta performance
- **Python-dotenv**: Gerenciamento de variáveis de ambiente

### Frontend
- **HTML5/CSS3**: Estrutura e estilização
- **JavaScript (Vanilla)**: Lógica da interface
- **Bootstrap 5**: Framework CSS para design responsivo
- **Font Awesome**: Ícones vetoriais

## Pré-requisitos

- Python 3.8 ou superior
- Conta na OpenAI com API Key
- Git (para versionamento)

## Instalação e Configuração Local

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/classificador-inteligente-email.git
cd classificador-inteligente-email
```

### 2. Crie e ative um ambiente virtual

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua_chave_api_aqui
```

### 5. Execute a aplicação

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Acesse a aplicação em: `http://localhost:8000`

## Estrutura do Projeto

```
classificador-inteligente-email/
│
├── app.py                 # Backend FastAPI
├── index.html            # Interface do usuário
├── index.css             # Estilos da aplicação
├── requirements.txt      # Dependências Python
├── .env                  # Variáveis de ambiente (não commitado)
├── .gitignore           # Arquivos ignorados pelo Git
└── README.md            # Documentação do projeto
```

## API Endpoints

### POST `/analise`

Analisa um e-mail e retorna a classificação com resposta sugerida.

**Parâmetros** (FormData):
- `email_content` (opcional): Texto do e-mail
- `email_file` (opcional): Arquivo .txt ou .pdf

**Resposta**:
```json
{
  "categoria": "PRODUTIVO",
  "resposta_sugerida": "Prezado(a)...",
  "confianca": "Alta"
}
```

### GET `/health`

Verifica o status da API.

**Resposta**:
```json
{
  "status": "ok",
  "message": "API funcionando corretamente"
}
```

### GET `/`

Retorna a página principal da aplicação.

## Como Usar

1. **Entrada de Texto**: Digite ou cole o conteúdo do e-mail no campo de texto
2. **Upload de Arquivo**: Arraste e solte ou selecione um arquivo (.txt ou .pdf)
3. **Analisar**: Clique no botão "Analisar E-mail"
4. **Resultados**: Visualize a categoria, confiança e resposta sugerida
5. **Ações**: Copie a resposta para a área de transferência ou baixe como arquivo

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Autor

Lucas Licurgo

## Contato

Para dúvidas ou sugestões, abra uma issue no GitHub.

---

Desenvolvido com FastAPI e OpenAI GPT-3.5
