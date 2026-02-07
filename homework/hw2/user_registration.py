from pydantic import (
    Field,
    field_validator,
    model_validator,
    BaseModel,
    EmailStr
)


class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0, description="Число, должно быть положительным")


class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(gt=0, lt=120)
    email: EmailStr
    is_employed: bool
    address: Address


    @field_validator('name')
    @classmethod
    def check_name(sls, value: str) -> str:
        if not value.replace(" ", "").isalpha():
            raise ValueError("Имя должно содержать только буквы")
        return value



    @model_validator(mode='after')
    def check_age_and_employment(self):
        if self.is_employed and not (18<= self.age <=65):
            raise ValueError("Если пользователь занят, возраст должен быть от 18 до 65 лет")
        return self


json_input = """{
    "name": "John Doe",
    "age": 18,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

user = User.model_validate_json(json_input)
print(user.model_dump_json(indent=4))