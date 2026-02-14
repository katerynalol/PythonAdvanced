from sqlalchemy import (Table,
                        Column,
                        BigInteger,
                        String,
                        SmallInteger)

from sqlalchemy.orm import registry



Register = registry()

user_table = Table(
    "users",
    Register.metadata,
    Column(
        "id",
        BigInteger,
        primary_key=True,
        autoincrement=True,
        unique=True),
    Column(
        "name",
        String(25)),
    Column(
        "age",
        SmallInteger,
        nullable=True),
)


class User:
    def __init__(self, name: str, age: int | None = None):
        self.name = name
        self.age = age


Register.map_imperatively(User, user_table)

