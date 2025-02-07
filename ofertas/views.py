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
            "tipo_entrega": produto.tipo_entrega,
            "frete_gratis": produto.frete_gratis,
        }
        for produto in produtos
    ]
    return JsonResponse({"produtos": produtos_serializados})

def exibir_produtos(request):
    produtos = Produto.objects.all()
    return render(request, "ofertas/produtos.html", {"produtos": produtos})