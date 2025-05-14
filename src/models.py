from sqlalchemy import Column, Integer, String, update

from homework.src.database import Base


class Recipes(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    time_dish = Column(Integer, nullable=False)
    ingredients = Column(String, nullable=False)
    description = Column(String)
    count = Column(Integer, default=0)

    @classmethod
    async def view(cls, session, id):
        async with session.begin():
            query = (
                update(Recipes).where(Recipes.id == id).values(count=Recipes.count + 1)
            )
            await session.execute(query)
