from db.database import Database
from helper.WriteAJson import writeAJson


db = Database("db", "livros")


def create(nome, autor, ano, preco):
    return db.collection.insert_one({"nome": nome, "autor": autor, "ano": ano, "preco": preco})


def read():
    books = db.collection.find({})
    writeAJson(books, "livros")


def update(nome, preco):
    return db.collection.update_one(
        {"nome": nome},
        {
            "$set": {"preco": preco},
            "$currentDate": {"lastModified": True}
        }
    )


def delete(nome):
    return db.collection.delete_one({"nome": nome})


create("Nome do Vento", "Patrick Roffus", 2007, 40.0)
create("Duna", "Frank Herbert", 1965, 70.0)
create("Fundação", "Isaac Asimov", 1942, 98.0)

update("Nome do Vento", 35.0)

read()

delete("Fundação")
