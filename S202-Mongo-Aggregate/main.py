from db.database import Database
from helper.WriteAJson import writeAJson
from dataset.produto_database import dataset as dataset_produto
from dataset.pessoa_dataset import dataset as dataset_pessoa

produtos = Database(database="database", collection="produtos", dataset=dataset_produto)
produtos.resetDatabase()

pessoas = Database(database = "database", collection ="pessoas", dataset=dataset_pessoa)
pessoas.resetDatabase()

result2 = produtos.collection.aggregate([
    {"$lookup":
        {
            "from": "pessoas",  # outra colecao
            "localField": "cliente_id",  # chave estrangeira
            "foreignField": "_id",  # id da outra colecao
            "as": "cliente"  # nome da saida
        }
     },
    {"$group": {"_id": "$cliente", "total": {"$sum": "$total"} } }, # formata os documentos
    {"$sort": {"total": 1} }, # order by in SQL, ordenar 
    {"$unwind": '$_id'},
    {"$project": {    # select in SQL, projeta os campos dejesados 
        "_id": 0,
        "nome": "$_id.nome",
        "total":1,
        "desconto": {
            "$cond": {"if": {"$gte": ["$total", 10]}, "then": True, "else": False}
        }
    }},
    
])

writeAJson(result2, "result2")
