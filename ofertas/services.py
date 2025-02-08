from decimal import Decimal
import re
from ofertas.models import Produto

def extrair_id_mercadolivre(url):
    match = re.search(r'MLB-\d+', url)
    return match.group(0) if match else None

def normalizar_nome(nome):
    return nome.strip().lower()

def preco_diferente(preco1, preco2):
    return abs(Decimal(preco1) - Decimal(preco2)) > Decimal("0.01")

def calcular_percentual_desconto(preco, preco_sem_desconto):
    return round(((preco_sem_desconto - preco) / preco_sem_desconto) * 100, 2) if preco_sem_desconto and preco else None

def precisa_atualizar(produto, novos_dados):
    return any([
        preco_diferente(produto.preco, novos_dados['preco']),
        produto.imagem != novos_dados['imagem'],
        normalizar_nome(produto.nome) != novos_dados['nome'],
        produto.parcelamento != novos_dados['parcelamento'],
        produto.preco_sem_desconto != novos_dados['preco_sem_desconto'],
        produto.percentual_desconto != novos_dados['percentual_desconto'],
        produto.tipo_entrega != novos_dados['tipo_entrega'],
        produto.frete_gratis != novos_dados['frete_gratis'],
    ])

def atualizar_produto(produto, novos_dados):
    for chave, valor in novos_dados.items():
        setattr(produto, chave, valor)
    produto.save()
    print(f"Produto atualizado: {produto.nome}")

def processar_oferta(oferta, produtos_existentes):
    id_oferta = extrair_id_mercadolivre(oferta["link"])
    if not id_oferta:
        return
    
    novos_dados = {
        'nome': normalizar_nome(oferta["nome"]),
        'preco': oferta["preco"],
        'imagem': oferta["imagem"],
        'link': oferta["link"],
        'parcelamento': oferta.get("parcelamento", ""),
        'preco_sem_desconto': oferta.get("preco_sem_desconto", None),
        'percentual_desconto': calcular_percentual_desconto(
            oferta["preco"], oferta.get("preco_sem_desconto", None)
        ),
        'tipo_entrega': oferta.get("tipo_entrega", "normal"),
        'frete_gratis': oferta.get("frete_gratis", False),
    }
    
    produto_existente = produtos_existentes.get(id_oferta)
    
    if produto_existente:
        if precisa_atualizar(produto_existente, novos_dados):
            atualizar_produto(produto_existente, novos_dados)
    else:
        Produto.objects.create(**novos_dados)
        print(f"Produto adicionado: {oferta['nome']}")

def atualizar_ofertas(ofertas):
    ids_novos = {extrair_id_mercadolivre(oferta["link"]) for oferta in ofertas}
    produtos_existentes = {extrair_id_mercadolivre(p.link): p for p in Produto.objects.all()}
    
    for id_produto, produto in produtos_existentes.items():
        if id_produto not in ids_novos:
            produto.delete()
            print(f"Produto removido: {produto.nome}")
    
    for oferta in ofertas:
        processar_oferta(oferta, produtos_existentes)