from django.http import JsonResponse
from .scraper import buscar_ofertas
from .models import Produto

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
        }
        for produto in produtos
    ]
    return JsonResponse({"produtos": produtos_serializados})