import re
from ofertas.models import Produto

def extrair_id_mercadolivre(url):
    match = re.search(r'MLB-\d+', url)
    return match.group(0) if match else None

def normalizar_nome(nome):
    return nome.strip().lower()

def preco_diferente(preco1, preco2):
    return abs(preco1 - preco2) > 0.01

def atualizar_ofertas(ofertas):
    ids_novos = {extrair_id_mercadolivre(oferta["link"]) for oferta in ofertas}
    produtos_existentes = {extrair_id_mercadolivre(p.link): p for p in Produto.objects.all()}

    for id_produto, produto in produtos_existentes.items():
        if id_produto not in ids_novos:
            produto.delete()
            print(f"Produto removido: {produto.nome}")

    for oferta in ofertas:
        id_oferta = extrair_id_mercadolivre(oferta["link"])
        if not id_oferta:
            continue

        nome_normalizado = normalizar_nome(oferta["nome"])
        preco_novo = round(float(oferta["preco"]), 2)
        imagem_nova = oferta["imagem"]
        link = oferta["link"]

        produto_existente = produtos_existentes.get(id_oferta)

        if produto_existente:
            preco_atual = round(float(produto_existente.preco), 2)
            imagem_atual = produto_existente.imagem
            nome_atual = normalizar_nome(produto_existente.nome)

            if (
                preco_diferente(preco_atual, preco_novo)
                or imagem_atual != imagem_nova
                or nome_atual != nome_normalizado
            ):
                produto_existente.preco = preco_novo
                produto_existente.imagem = imagem_nova
                produto_existente.nome = nome_normalizado
                produto_existente.save()
                print(f"Produto atualizado: {produto_existente.nome}")
        else:
            Produto.objects.create(
                nome=nome_normalizado,
                preco=preco_novo,
                imagem=imagem_nova,
                link=link
            )
            print(f"Produto adicionado: {oferta['nome']}")
