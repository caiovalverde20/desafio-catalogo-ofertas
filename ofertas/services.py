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
        parcelamento_novo = oferta.get("parcelamento", "")
        preco_sem_desconto_novo = oferta.get("preco_sem_desconto", None)
        tipo_entrega_novo = oferta.get("tipo_entrega", "normal")
        frete_gratis_novo = oferta.get("frete_gratis", False)

        produto_existente = produtos_existentes.get(id_oferta)

        if produto_existente:
            preco_atual = round(float(produto_existente.preco), 2)
            imagem_atual = produto_existente.imagem
            nome_atual = normalizar_nome(produto_existente.nome)
            parcelamento_atual = produto_existente.parcelamento
            preco_sem_desconto_atual = produto_existente.preco_sem_desconto
            tipo_entrega_atual = produto_existente.tipo_entrega
            frete_gratis_atual = produto_existente.frete_gratis

            if (
                preco_diferente(preco_atual, preco_novo)
                or imagem_atual != imagem_nova
                or nome_atual != nome_normalizado
                or parcelamento_atual != parcelamento_novo
                or preco_sem_desconto_atual != preco_sem_desconto_novo
                or tipo_entrega_atual != tipo_entrega_novo
                or frete_gratis_atual != frete_gratis_novo
            ):
                produto_existente.preco = preco_novo
                produto_existente.imagem = imagem_nova
                produto_existente.nome = nome_normalizado
                produto_existente.parcelamento = parcelamento_novo
                produto_existente.preco_sem_desconto = preco_sem_desconto_novo
                produto_existente.tipo_entrega = tipo_entrega_novo
                produto_existente.frete_gratis = frete_gratis_novo
                produto_existente.save()
                print(f"Produto atualizado: {produto_existente.nome}")

        else:
            Produto.objects.create(
                nome=nome_normalizado,
                preco=preco_novo,
                imagem=imagem_nova,
                link=link,
                parcelamento=parcelamento_novo,
                preco_sem_desconto=preco_sem_desconto_novo,
                tipo_entrega=tipo_entrega_novo,
                frete_gratis=frete_gratis_novo
            )
            print(f"Produto adicionado: {oferta['nome']}")
