from sqlalchemy import create_engine, Column, String, Text, Boolean, Integer, ForeignKey, Index
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'recipe_tb'
    
    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_nm = Column(Text, nullable=False, index=True)  # Индекс для быстрого поиска по названию
    recipe_image = Column(Text)
    recipe_instructions = Column(Text)
    is_favorite = Column(Boolean)
    cooking_time = Column(Text)
    portion = Column(Text)

class Ingredient(Base):
    __tablename__ = 'ingredient_tb'
    
    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    ingredient_nm = Column(Text, nullable=False, index=True)  # Индекс для быстрого поиска по названию

class Tag(Base):
    __tablename__ = 'tag_tb'
    
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_nm = Column(Text, nullable=False, index=True)  # Индекс для быстрого поиска по названию тега

# Связь многие ко многим между рецептами и тегами
class RecipeHasTag(Base):
    __tablename__ = 'recipe_has_tag'
    
    recipe_id = Column(Integer, ForeignKey('recipe_tb.recipe_id', ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag_tb.tag_id', ondelete="CASCADE"), primary_key=True)

# Связь многие ко многим между рецептами и ингредиентами
class RecipeHasIngredient(Base):
    __tablename__ = 'recipe_has_ingredient'
    
    recipe_id = Column(Integer, ForeignKey('recipe_tb.recipe_id', ondelete="CASCADE"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient_tb.ingredient_id', ondelete="CASCADE"), primary_key=True)
    req_amount = Column(Text)

# Индексы для таблиц
Index('ix_recipe_nm', Recipe.recipe_nm)  # Индекс для поля recipe_nm
Index('ix_tag_nm', Tag.tag_nm)  # Индекс для поля tag_nm
Index('ix_ingredient_nm', Ingredient.ingredient_nm)  # Индекс для поля ingredient_nm

# Подключение к базе данных
DATABASE_URL = "mysql+pymysql://root:BorGser_077@localhost/recipes_data"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


