from sqlalchemy.orm import Session
from models import Recipe, Tag, RecipeHasTag, RecipeHasIngredient, Ingredient

# Получение всех рецептов
def get_all_recipes(db: Session):
    return db.query(Recipe).all()

# Получение рецепта по имени
def get_recipe_by_name(db: Session, recipe_name: str):
    return db.query(Recipe).filter(Recipe.recipe_nm == recipe_name).first()

# Получение избранных рецептов
def get_favorite_recipes(db: Session):
    return db.query(Recipe).filter(Recipe.is_favorite == True).all()

# Получение рецептов по тегу
def get_recipes_by_tag(db: Session, tag_name: str):
    tag = db.query(Tag).filter(Tag.tag_nm == tag_name).first()
    if tag:
        return db.query(Recipe).join(RecipeHasTag).filter(RecipeHasTag.tag_id == tag.tag_id).all()
    return []

# Получение рецептов по категории
def get_recipes_by_category(db: Session, category_name: str):
    if category_name == "Завтраки":
        return get_recipes_by_tag(db, "Завтраки")
    elif category_name == "Обеды":
        return get_recipes_by_tag(db, "Обеды")
    return []

# Добавление/удаление рецепта в/из избранного
def toggle_favorite(db: Session, recipe_name: str):
    recipe = db.query(Recipe).filter(Recipe.recipe_nm == recipe_name).first()
    if recipe:
        recipe.is_favorite = not recipe.is_favorite
        db.commit()
        db.refresh(recipe)

