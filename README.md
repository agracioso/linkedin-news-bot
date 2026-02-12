# LinkedIn News Bot - MVP

Bot Python que busca notícias recentes sobre um tópico e gera posts profissionais para LinkedIn usando inteligência artificial.

## 📋 O que o projeto faz

Este bot automatiza o processo de criação de conteúdo para LinkedIn:

1. **Pergunta o assunto** - Script interativo que solicita o tópico de interesse
2. **Busca notícias** - Utiliza o Google News para encontrar as notícias mais relevantes e recentes sobre o tópico
3. **Analisa conteúdo** - Envia as notícias para a API da Anthropic (Claude AI)
4. **Gera post profissional** - Claude cria um post de 200-300 palavras com:
   - Tom acadêmico mas acessível
   - Insights e análise (não apenas resumo)
   - Conexões entre diferentes notícias
   - Reflexão final para gerar engajamento
5. **Salva automaticamente** - O post é exibido no terminal e salvo em arquivo .txt com timestamp

## 🔑 Obtendo a API Key

### Anthropic API Key (Claude)

1. Acesse [https://console.anthropic.com](https://console.anthropic.com)
2. Faça login ou crie uma conta
3. Navegue até "API Keys"
4. Crie uma nova API key
5. Copie a key (ela começa com `sk-ant-api03-...`)

⚠️ **Importante**: Mantenha sua API key em segredo! Nunca a compartilhe ou faça commit dela no Git.

### Por que não preciso de API key do Google News?

Este bot usa a biblioteca **GNews** que faz scraping público do Google News, não requerendo API key ou cadastro. É totalmente gratuito e sem limites de requisições (dentro do uso razoável).

## ⚙️ Configuração

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd linkedin-news-bot
```

### 2. Configure a variável de ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e adicione sua API key
nano .env  # ou use seu editor preferido
```

O arquivo `.env` deve ficar assim:

```
ANTHROPIC_API_KEY=sk-ant-api03-sua_chave_anthropic_aqui
```

### 3. Instale as dependências

```bash
# Recomendado: criar um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## 🚀 Como executar

### Execução básica

```bash
python main.py
```

O script solicitará que você digite um tópico:

```
Digite o tópico para buscar notícias: inteligência artificial
```

### Fluxo de execução

1. Script pergunta qual o assunto desejado
2. Bot busca notícias dos últimos 7 dias no Google News sobre o tópico
3. Encontra as 5 notícias mais relevantes
4. Envia para Claude AI gerar o post
5. Exibe o post no terminal
6. Salva automaticamente em `posts/post_TOPICO_YYYYMMDD_HHMMSS.txt`

## 📝 Exemplo de uso

```bash
$ python main.py

🤖 LinkedIn News Bot - MVP
Bot que gera posts LinkedIn baseados em notícias recentes

Digite o tópico para buscar notícias: computação quântica

================================================================================
LinkedIn News Bot - Gerando post sobre: computação quântica
================================================================================

🔍 Buscando notícias sobre 'computação quântica' no Google News (últimos 7 dias)...
✅ Encontradas 5 notícias relevantes
✍️  Gerando post LinkedIn sobre 'computação quântica' com Claude AI...
✅ Post gerado com sucesso!

================================================================================
📝 POST GERADO:
================================================================================

[Post gerado aparece aqui...]

================================================================================

💾 Post salvo em: posts/post_computacao_quantica_20260212_143022.txt

✅ Processo concluído com sucesso!
```

## 📁 Estrutura do projeto

```
linkedin-news-bot/
├── main.py              # Script principal do bot
├── requirements.txt     # Dependências Python
├── .env.example        # Template de variáveis de ambiente
├── .env                # Suas API keys (NÃO versionar!)
├── .gitignore          # Arquivos ignorados pelo Git
├── README.md           # Esta documentação
└── posts/              # Posts gerados são salvos aqui
    ├── .gitkeep
    └── post_topico_20260212_143022.txt
```

## 🛠️ Requisitos técnicos

- **Python**: 3.9 ou superior
- **Bibliotecas**:
  - `gnews`: Para buscar notícias do Google News (sem necessidade de API key)
  - `anthropic`: SDK oficial da Anthropic para Claude AI
  - `python-dotenv`: Gerenciamento de variáveis de ambiente

## 🔍 Funcionalidades principais

### `buscar_noticias(topico, dias=7, max_noticias=5)`
- Busca notícias recentes no Google News
- Configura para idioma português e país Brasil
- Filtra por período (últimos 7 dias por padrão)
- Retorna até 5 notícias mais relevantes
- Não requer API key ou autenticação

### `gerar_post_linkedin(topico, noticias)`
- Formata contexto com as notícias
- Cria prompt otimizado para Claude
- Gera post de 200-300 palavras
- Retorna texto formatado para LinkedIn

### `salvar_post(topico, post_texto)`
- Cria pasta `posts/` se não existir
- Gera nome de arquivo com timestamp
- Salva post com metadados (tópico, data)

### `gerar_post(topico)`
- Função principal que orquestra todo o processo
- Combina busca + geração + exibição + salvamento

## ⚡ Tratamento de erros

O bot possui tratamento de erros para:
- API key não configurada
- Falhas ao buscar notícias no Google News
- Nenhuma notícia encontrada sobre o tópico
- Erros ao gerar posts com Claude AI
- Erros ao salvar posts em arquivo

## 🚧 Limitações do MVP

Este é um MVP (Produto Mínimo Viável). Funcionalidades NÃO incluídas:

- ❌ Upload automático para LinkedIn
- ❌ Interface gráfica (GUI)
- ❌ Banco de dados para histórico
- ❌ Agendamento automático de posts
- ❌ Upload para Google Drive

Estas funcionalidades podem ser adicionadas em versões futuras.

## 📄 Licença

Projeto de código aberto para fins educacionais.

## 🤝 Contribuindo

Este é um projeto MVP. Sugestões e melhorias são bem-vindas!

## 📞 Suporte

Em caso de problemas:
1. Verifique se a API key da Anthropic está correta no arquivo `.env`
2. Confirme que instalou todas as dependências: `pip install -r requirements.txt`
3. Verifique sua conexão com a internet
4. Consulte a documentação:
   - [GNews GitHub](https://github.com/ranahaani/GNews)
   - [Anthropic API Docs](https://docs.anthropic.com)

---

**Desenvolvido com Python e Claude AI** 🤖✨
