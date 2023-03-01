from sqlalchemy import create_engine, Column, String, Integer
# from sqlalchemy.orm import sessionmaker, declarative_base
from database import Base, engine, session


# engine = create_engine("sqlite:///orm_python.db", echo=True)    # echo=True - чтобы в консоль писались все запросы
# Session = sessionmaker(bind=engine)
# session = Session()
#
# Base = declarative_base(bind=engine)


class Recept(Base):
    __tablename__ = 'Recepts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True) # зачем на текстовом поле индекс?
    count_views = Column(Integer, default=0)
    time_cook = Column(Integer)
    ingridients = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

    def __repr__(self):
        return f"{self.id}, {self.title}, {self.count_views}"

    # def to_json(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def insert_data():
    recepts = [Recept(title="Пицца", time_cook=90, ingridients="Тесто, колбаса, сыр, помидор", description="Вкусно, но не очень полезно"),
               Recept(title="Суп", time_cook=180, ingridients="Вода, лук, картофель", description="Вкусный суп как у бабушки"),
               Recept(title="Омлет", time_cook=30, ingridients="Яйцо, молоко", description="Быстро и вкусно"),
               Recept(title="Салат Цезарь", time_cook=60, ingridients="Зелень, вареная курица, сыр", description="В честь знаменитой личности"),
               Recept(title="Паста Карбонара", time_cook=60, ingridients="Макароны, соус, бекон", description="Вкусные макароны с беконом и соусом"),
               Recept(title="Гамбургер", time_cook=60, ingridients="Булка, мясо", description="Как в Макдоналдсе"),
               Recept(title="Окрошка", time_cook=120, ingridients="Кефир, зелень, картофель, колбаса", description="Окрошка деревенская"),
               ]

    session.add_all(recepts)
    session.commit()


if __name__ == '__main__':

    Base.metadata.create_all(bind=engine)

    check_exist = session.query(Recept).all()
    if not check_exist:
        insert_data()
