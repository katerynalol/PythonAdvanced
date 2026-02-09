#                           Типы связей таблиц

from sqlalchemy import (
    create_engine,
    BigInteger,
    String,
    SmallInteger,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship)

from pathlib import Path


BASE_DIR = Path(__file__).parents[1]

engine = create_engine(
    url="sqlite:///:memory:")


class Base(DeclarativeBase):
    __abstract__ = True        #фудамент

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,         #сама создаёт счётчик +1
        unique=True)

# Many to Many
class UsersCourses(Base):
    __tablename__ = 'users_courses'

    course_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('courses.id'))

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id'))



class User(Base):
    __tablename__ = "users"          #название таблицы на стороне бд


    name: Mapped[str] = mapped_column(
        String(25),             #VARCHAR(25) | кол-во символов
        nullable=False)          #NOT NULL

    surname: Mapped[str] = mapped_column(
        String(30),
        nullable=True)

    username: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
        unique=True,
        index=True)

    age: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=True)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,             # сторона ORM и python
        server_default="true")    # сторона базы данных


    # FK keys
    addres_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("adresses.id")
    )

    # relationships
    # One to Many
    address = relationship(
        "Adress",
        back_populates="users"
    )
    # One to One
    profile = relationship(
        'UserProfile',
        back_populates='user',
        uselist=False
    )
    # Many to Many
    courses = relationship(
        'Course',
        secondary='UsersCourses',
        back_populates='users'
    )

# Many to Many
class Course(Base):
    __tablename__ = "courses"

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False)

    # relationships
    users = relationship(
        'User',
        secondary='UsersCourses',
        back_populates='courses')


# One to One
class UserProfile(Base):
    __tablename__ = 'user_profiles'

    avatar: Mapped[str] = mapped_column(
        String(255),
        nullable=True)

    # FK keys
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id'),
        unique=True)

    # relationships
    user = relationship(
        'User',
        back_populates='profile',
        uselist=False)            #один объект (не список)






class Adress(Base):
    __tablename__ = "adresses"

    city: Mapped[str] = mapped_column(
        String(25),
        nullable=False)

    # relationships
    users = relationship(
        "User",
        back_populates="address")


    # example
    # <field_name> = relationship(
    #     '<class Name>',
    #     back_populates='<class Name> -> <field name>'
    # )


# user = User()
#
# user.address
#
# address = Address()
# address.users