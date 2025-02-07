import json
from pathlib import Path
from django.http import JsonResponse
from .scraper import buscar_ofertas
from .models import Produto
from django.shortcuts import render

def atualizar_produtos(request):
    try:
        buscar_ofertas()
        return JsonResponse({"mensagem": "Produtos atualizados com sucesso!"}, status=200)
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao atualizar produtos", "erro": str(e)}, status=500)

def listar_produtos(request):
    produtos = Produto.objects.all()
    produtos_serializados = [
        {
            "nome": produto.nome,
            "preco": produto.preco,
            "imagem": produto.imagem,
            "link": produto.link,
            "parcelamento": produto.parcelamento,
            "preco_sem_desconto": produto.preco_sem_desconto,
            "percentual_desconto": produto.percentual_desconto,
            "tipo_entrega": produto.tipo_entrega,
            "frete_gratis": produto.frete_gratis,
        }
        for produto in produtos
    ]
    return JsonResponse({"produtos": produtos_serializados})

def listar_maior_preco(request):
    produtos = Produto.objects.order_by('-preco')
    return render(request, "ofertas/produtos.html", {"produtos": produtos})

def listar_menor_preco(request):
    produtos = Produto.objects.order_by('preco')
    return render(request, "ofertas/produtos.html", {"produtos": produtos})

def listar_maior_desconto(request):
    produtos = Produto.objects.order_by('-percentual_desconto')
    return render(request, "ofertas/produtos.html", {"produtos": produtos})

def exibir_produtos(request):
    produtos = Produto.objects.all()

    if not produtos.exists():
        caminho_arquivo = "./ofertas/produtos.json"

        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            json_produtos = json.load(arquivo)

        for produto_data in json_produtos["produtos"]:
            Produto.objects.create(
                nome=produto_data["nome"],
                preco=float(produto_data["preco"]),
                imagem=produto_data["imagem"],
                link=produto_data["link"],
                parcelamento=produto_data["parcelamento"],
                preco_sem_desconto=float(produto_data["preco_sem_desconto"]) if produto_data.get("preco_sem_desconto") else None,
                percentual_desconto=float(produto_data["percentual_desconto"]) if produto_data.get("percentual_desconto") else None,
                tipo_entrega=produto_data["tipo_entrega"],
                frete_gratis=produto_data["frete_gratis"],
            )

        produtos = Produto.objects.all()

    produto_maior_preco = produtos.order_by('-preco').first()
    produto_menor_preco = produtos.order_by('preco').first()
    
    produtos_com_desconto = produtos.exclude(percentual_desconto__isnull=True).exclude(percentual_desconto=0)

    produto_maior_desconto = produtos_com_desconto.order_by('-percentual_desconto').first()

    return render(request, "ofertas/produtos.html", {
        "produtos": produtos,
        "produto_maior_preco": produto_maior_preco,
        "produto_menor_preco": produto_menor_preco,
        "produto_maior_desconto": produto_maior_desconto,
    })
