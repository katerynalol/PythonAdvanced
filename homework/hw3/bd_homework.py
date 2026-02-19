from sqlalchemy import (
    create_engine,
    Numeric,
    Integer ,
    String,
    Boolean,
    ForeignKey,
    select,
    func)

from sqlalchemy.orm import (
    relationship,
    DeclarativeBase,
    Mapped,
    mapped_column, joinedload)

from decimal import Decimal

from homework.hw3.db_connector import DBConnector


engine = create_engine(
    url = "sqlite:///:memory:")


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True)



class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False)

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True)

    products = relationship(
        "Product",
        back_populates= "category")



class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False)

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False)

    in_stock: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true")


    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id"))

    category = relationship(
        "Category",
        back_populates= "products")


Base.metadata.create_all(bind=engine)


with DBConnector(engine) as session:
    data_of_categories = ({"name": "Электроника", "description": "Гаджеты и устройства."},
            {"name": "Книги", "description": "Печатные книги и электронные книги."},
            {"name": "Одежда", "description": "Одежда для мужчин и женщин."})

    new_category = [Category(**data) for data in data_of_categories]
    session.add_all(new_category)

    data_of_products = ({"name": "Смартфон", "price": 299.99, "category_id": 1},
                        {"name": "Ноутбук", "price": 499.99, "category_id": 1},
                        {"name": "Научно-фантастический роман", "price": 15.99, "category_id": 2},
                        {"name": "Джинсы", "price": 40.50, "category_id": 3},
                        {"name": "Футболка", "price": 20.00, "category_id": 3})

    new_products = [Product (**data) for data in data_of_products]
    session.add_all(new_products)
    session.commit()



    all_categorys = (
        select(Category)
        .join(Product, Category.id == Product.category_id )
        .options(joinedload(Category.products))
    )

    response = session.execute(all_categorys).unique().scalars()
    for category in response:
        print(f"Категория: {category.name} ")
        if category.products:
            for product in category.products:
                print(f"\t - Продукт: {product.name}, Цена: {product.price}")



    update_product = (
        select(Product)
        .where(Product.name == "Смартфон")
    )

    result = session.execute(update_product).scalars().first()
    if result:
        result.price = 349.99
        session.commit()
        print(result.name, result.price)



    count_products_in_category = (
        select(Category.name ,
               func.count(Product.id).label("product_count")
               )
        .join(Product)
        .group_by(Category.name)
        .having(func.count(Product.id) > 1)
    )
    result = session.execute(count_products_in_category).all()

    for row in result:
        print(f"Категория: {row.name}, Количество продуктов: {row.product_count}")