import json


def lambda_handler(event, context):
    """
    Função Lambda de exemplo para processar um arquivo CSV recebido via Step Functions.
    
    O evento recebido contém informações do objeto S3 quando usado com Distributed Map:
    {
        "Key": "2024/01001099999.csv",
        "Size": 48922,
        "ETag": "...",
        "LastModified": "2024-08-03T..."
    }
    """
    print(f"Evento recebido: {json.dumps(event)}")

    # Extrai o nome do arquivo do evento
    arquivo = event.get("Key", "arquivo_desconhecido")

    # Simulação de processamento
    resultado = {
        "arquivo": arquivo,
        "status": "processado",
        "linhas_lidas": 1000,
        "mensagem": f"Arquivo {arquivo} processado com sucesso."
    }

    print(f"Resultado: {json.dumps(resultado)}")
    return resultado
