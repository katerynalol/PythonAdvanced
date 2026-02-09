from sqlalchemy import (
    create_engine,
    Numeric,
    Integer ,
    String,
    Boolean,
    ForeignKey)

from sqlalchemy.orm import (
    relationship,
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column)

from decimal import Decimal


engine = create_engine(
    url = "sqlite:///:memory:")


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False)


class Product(Base):
    __tablename__ = "products"

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


class Category(Base):
    __tablename__ = "categories"

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True)

    products = relationship(
        "Product",
        back_populates= "category")


Base.metadata.create_all(bind=engine)
print(Base.metadata.tables)


Session = sessionmaker(bind=engine)
session = Session()


category = Category(
    name="Electronics",
    description="Electronic devices")

product = Product(
    name="Laptop",
    price=Decimal("999.99"),
    category=category)

session.add(category)
session.add(product)
session.commit()

products = session.query(Product).all()

for p in products:
    print(
        p.name,
        p.price,
        p.category.name)

session.close()