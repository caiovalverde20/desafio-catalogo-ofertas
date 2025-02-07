from django.http import JsonResponse
from .scraper import buscar_ofertas

def atualizar_produtos(request):
    try:
        buscar_ofertas()
        return JsonResponse({"mensagem": "Produtos atualizados com sucesso!"}, status=200)
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao atualizar produtos", "erro": str(e)}, status=500)
