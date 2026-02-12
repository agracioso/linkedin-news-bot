"""
LinkedIn News Bot - MVP
Bot Python que busca notícias sobre um tópico usando Google News e gera posts
profissionais para LinkedIn usando a API da Anthropic (Claude).
"""

import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import quote
from anthropic import Anthropic
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Validar que a API key está configurada
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY não encontrada. Configure o arquivo .env")


def buscar_noticias(topico, dias=7, max_noticias=5):
    """
    Busca notícias recentes sobre um tópico usando Google News RSS.

    Args:
        topico (str): Tópico para buscar notícias
        dias (int): Número de dias atrás para buscar (padrão: 7) - Nota: RSS não filtra por data
        max_noticias (int): Número máximo de notícias para retornar (padrão: 5)

    Returns:
        list: Lista com as notícias encontradas (título, descrição, url, data)
    """
    print(f"🔍 Buscando notícias sobre '{topico}' no Google News...")

    try:
        # Codificar o tópico para URL
        topico_encoded = quote(topico)

        # URL do RSS do Google News em português do Brasil
        rss_url = f"https://news.google.com/rss/search?q={topico_encoded}&hl=pt-BR&gl=BR&ceid=BR:pt-419"

        # Headers para simular um navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Fazer requisição ao RSS
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse do XML com BeautifulSoup
        soup = BeautifulSoup(response.content, 'xml')

        # Encontrar todos os itens de notícia
        items = soup.find_all('item', limit=max_noticias)

        if not items:
            print(f"❌ Nenhuma notícia encontrada sobre '{topico}'")
            return []

        # Extrair informações de cada notícia
        noticias = []
        for item in items:
            titulo = item.title.text if item.title else 'Sem título'
            link = item.link.text if item.link else ''
            descricao = item.description.text if item.description else 'Sem descrição'
            pub_date = item.pubDate.text if item.pubDate else ''

            # Extrair fonte da descrição (Google News inclui fonte no início)
            fonte = 'Google News'
            if ' - ' in titulo:
                # Muitas vezes a fonte vem no título
                fonte = titulo.split(' - ')[-1]

            noticia = {
                'titulo': titulo,
                'descricao': descricao[:300],  # Limitar descrição
                'url': link,
                'fonte': fonte,
                'data': pub_date
            }
            noticias.append(noticia)

        print(f"✅ Encontradas {len(noticias)} notícias relevantes")
        return noticias

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao buscar notícias no Google News: {e}")
        return []
    except Exception as e:
        print(f"❌ Erro inesperado ao processar notícias: {e}")
        return []


def gerar_post_linkedin(topico, noticias):
    """
    Gera um post profissional para LinkedIn baseado nas notícias encontradas.

    Args:
        topico (str): Tópico das notícias
        noticias (list): Lista de notícias para basear o post

    Returns:
        str: Texto do post gerado ou None se houver erro
    """
    if not noticias:
        print("❌ Não é possível gerar post sem notícias")
        return None

    print(f"✍️  Gerando post LinkedIn sobre '{topico}' com Claude AI...")

    # Formatar contexto com as notícias para enviar ao Claude
    contexto_noticias = "\n\n".join([
        f"Notícia {i+1}:\n"
        f"Título: {n['titulo']}\n"
        f"Descrição: {n['descricao']}\n"
        f"Fonte: {n['fonte']}\n"
        f"URL: {n['url']}"
        for i, n in enumerate(noticias)
    ])

    # Criar prompt para o Claude
    prompt = f"""Você é um especialista em comunicação profissional e criação de conteúdo para LinkedIn.

Baseado nas seguintes notícias recentes sobre "{topico}", crie um post profissional para LinkedIn que:

1. Tenha entre 200-300 palavras
2. Use um tom acadêmico mas acessível e envolvente
3. NÃO seja apenas um resumo das notícias, mas ofereça insights e análise
4. Conecte os pontos entre as diferentes notícias apresentadas
5. Seja relevante para profissionais da área
6. Termine com uma reflexão ou pergunta que gere engajamento
7. Use formatação apropriada para LinkedIn (quebras de linha, emojis moderados se apropriado)
8. Inclua no final as fontes como links

Notícias:
{contexto_noticias}

Gere o post em português do Brasil:"""

    try:
        # Inicializar cliente da Anthropic
        client = Anthropic(api_key=ANTHROPIC_API_KEY)

        # Fazer requisição à API do Claude
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extrair o texto gerado
        post_gerado = message.content[0].text

        print("✅ Post gerado com sucesso!")
        return post_gerado

    except Exception as e:
        print(f"❌ Erro ao gerar post com Claude: {e}")
        return None


def salvar_post(topico, post_texto):
    """
    Salva o post gerado em um arquivo de texto.

    Args:
        topico (str): Tópico do post
        post_texto (str): Texto do post para salvar

    Returns:
        str: Caminho do arquivo salvo ou None se houver erro
    """
    # Criar pasta posts/ se não existir
    os.makedirs('posts', exist_ok=True)

    # Gerar nome do arquivo com timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    topico_limpo = "".join(c for c in topico if c.isalnum() or c in (' ', '-', '_')).strip()
    topico_limpo = topico_limpo.replace(' ', '_')
    nome_arquivo = f"posts/post_{topico_limpo}_{timestamp}.txt"

    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(f"Tópico: {topico}\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            f.write(post_texto)

        print(f"💾 Post salvo em: {nome_arquivo}")
        return nome_arquivo

    except Exception as e:
        print(f"❌ Erro ao salvar post: {e}")
        return None


def gerar_post(topico):
    """
    Função principal que orquestra todo o processo:
    1. Busca notícias sobre o tópico
    2. Gera post LinkedIn com Claude
    3. Exibe o post no terminal
    4. Salva o post em arquivo

    Args:
        topico (str): Tópico para gerar o post
    """
    print("\n" + "=" * 80)
    print(f"LinkedIn News Bot - Gerando post sobre: {topico}")
    print("=" * 80 + "\n")

    # Passo 1: Buscar notícias
    noticias = buscar_noticias(topico, dias=7)

    if not noticias:
        print("\n❌ Não foi possível continuar sem notícias. Tente outro tópico.")
        return

    # Passo 2: Gerar post com Claude
    post_texto = gerar_post_linkedin(topico, noticias)

    if not post_texto:
        print("\n❌ Não foi possível gerar o post.")
        return

    # Passo 3: Exibir post no terminal
    print("\n" + "=" * 80)
    print("📝 POST GERADO:")
    print("=" * 80)
    print(post_texto)
    print("=" * 80 + "\n")

    # Passo 4: Salvar post em arquivo
    salvar_post(topico, post_texto)

    print("\n✅ Processo concluído com sucesso!")


if __name__ == "__main__":
    """
    Bloco de execução principal do script.
    """
    print("\n🤖 LinkedIn News Bot - MVP")
    print("Bot que gera posts LinkedIn baseados em notícias recentes\n")

    # Solicitar tópico ao usuário
    topico = input("Digite o tópico para buscar notícias: ").strip()

    if not topico:
        print("❌ Tópico não pode ser vazio!")
        exit(1)

    # Executar geração do post
    gerar_post(topico)
