"""
LinkedIn News Bot - DEMO
Versão de demonstração com notícias de exemplo
"""

import os
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY não encontrada. Configure o arquivo .env")


def buscar_noticias_demo(topico):
    """
    Retorna notícias de exemplo para demonstração.
    """
    print(f"🔍 [MODO DEMO] Buscando notícias sobre '{topico}'...")

    # Notícias de exemplo
    noticias_exemplo = {
        "inteligência artificial": [
            {
                'titulo': 'IA generativa transforma mercado de trabalho brasileiro',
                'descricao': 'Empresas brasileiras estão adotando ferramentas de IA generativa como ChatGPT e Claude para aumentar produtividade. Especialistas preveem mudanças significativas nas próximas décadas.',
                'url': 'https://example.com/ia-mercado',
                'fonte': 'TechBrasil',
                'data': '2026-02-10'
            },
            {
                'titulo': 'Google lança novo modelo de IA com capacidades avançadas',
                'descricao': 'O Google anunciou seu mais recente modelo de IA, prometendo maior precisão e velocidade no processamento de linguagem natural.',
                'url': 'https://example.com/google-ia',
                'fonte': 'TechCrunch',
                'data': '2026-02-09'
            },
            {
                'titulo': 'Regulamentação de IA avança no Congresso Nacional',
                'descricao': 'Projeto de lei que estabelece diretrizes para uso de inteligência artificial no Brasil está em fase final de votação.',
                'url': 'https://example.com/regulamentacao-ia',
                'fonte': 'Senado Federal',
                'data': '2026-02-08'
            }
        ]
    }

    # Usar notícias genéricas se tópico não estiver na lista
    if topico.lower() not in noticias_exemplo:
        noticias = [
            {
                'titulo': f'Novidades sobre {topico} ganham destaque',
                'descricao': f'Especialistas discutem os impactos recentes relacionados a {topico} no mercado brasileiro.',
                'url': 'https://example.com/noticia1',
                'fonte': 'Portal de Notícias',
                'data': '2026-02-10'
            },
            {
                'titulo': f'{topico.title()} em alta: veja as tendências',
                'descricao': f'Análise aprofundada sobre as principais tendências de {topico} para 2026.',
                'url': 'https://example.com/noticia2',
                'fonte': 'Revista Tecnologia',
                'data': '2026-02-09'
            }
        ]
    else:
        noticias = noticias_exemplo[topico.lower()]

    print(f"✅ [DEMO] Encontradas {len(noticias)} notícias de exemplo")
    return noticias


def gerar_post_linkedin(topico, noticias):
    """Gera post LinkedIn com Claude AI."""
    print(f"✍️  Gerando post LinkedIn sobre '{topico}' com Claude AI...")

    contexto_noticias = "\n\n".join([
        f"Notícia {i+1}:\n"
        f"Título: {n['titulo']}\n"
        f"Descrição: {n['descricao']}\n"
        f"Fonte: {n['fonte']}\n"
        f"URL: {n['url']}"
        for i, n in enumerate(noticias)
    ])

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
        client = Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        post_gerado = message.content[0].text
        print("✅ Post gerado com sucesso!")
        return post_gerado

    except Exception as e:
        print(f"❌ Erro ao gerar post com Claude: {e}")
        return None


def salvar_post(topico, post_texto):
    """Salva o post em arquivo."""
    os.makedirs('posts', exist_ok=True)

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


def main():
    """Função principal - versão demo."""
    print("\n🤖 LinkedIn News Bot - DEMO MODE")
    print("Bot que gera posts LinkedIn baseados em notícias")
    print("⚠️  MODO DEMONSTRAÇÃO - Usando notícias de exemplo\n")

    topico = input("Digite o tópico para buscar notícias: ").strip()

    if not topico:
        print("❌ Tópico não pode ser vazio!")
        return

    print("\n" + "=" * 80)
    print(f"LinkedIn News Bot - Gerando post sobre: {topico}")
    print("=" * 80 + "\n")

    # Buscar notícias (demo)
    noticias = buscar_noticias_demo(topico)

    # Gerar post com Claude
    post_texto = gerar_post_linkedin(topico, noticias)

    if not post_texto:
        print("\n❌ Não foi possível gerar o post.")
        return

    # Exibir post
    print("\n" + "=" * 80)
    print("📝 POST GERADO:")
    print("=" * 80)
    print(post_texto)
    print("=" * 80 + "\n")

    # Salvar post
    salvar_post(topico, post_texto)

    print("\n✅ Processo concluído com sucesso!")
    print("\n💡 Dica: Em ambiente com internet, o bot buscará notícias reais do Google News")


if __name__ == "__main__":
    main()
