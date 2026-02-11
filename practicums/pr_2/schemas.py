# Создать Pydantic схему для безопасного вывода информации о минералах в API.
#
# ТРЕБОВАНИЯ:
# - Валидация всех полей модели Mineral
# - Поддержка сериализации из SQLAlchemy объектов
# - Готовность к использованию в FastAPI/Flask endpoints
#
# ЦЕЛЬ: Обеспечить типобезопасность и валидацию при передаче данных о минералах.

class MineralOutput(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    id: int
    name: str
    color: str
    solid: Decimal


mineral = {"id":3, "name": "gold", "color": "yellow", "solid": 1234.43}

resp =MineralOutput.model_validate(mineral)
print(resp)