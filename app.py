import flet as ft
from functions import get_all_recipes, get_recipe_by_name, get_favorite_recipes, toggle_favorite,get_recipes_by_tag
from models import SessionLocal
from models import RecipeHasIngredient, Ingredient, Tag, RecipeHasTag,Recipe

# Объявление search_results_column в глобальной области видимости
search_results_column = ft.Column()  # Это будет использоваться для отображения результатов поиска

def show_home_page(page: ft.Page, db):
    print("show_home_page вызван")
    page.controls.clear()

    # Create ListView for the main page
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    
    # Create a Container for search row with proper styling
    search_row = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextField(
                    label="Поиск рецепта",
                    expand=True,
                    border_radius=10,
                    border_color="brown",
                    text_size=16,
                    on_submit=lambda e: search_recipes(e, db, page)
                ),
                ft.Container(
                    content=ft.Dropdown(
                        width=50,
                        text_style=ft.TextStyle(
                            size=13,
                            color="Black",
                            weight='bold',
                        ),
                    
                        icon=ft.icons.FILTER_ALT,
                        border_color="transparent",
                        label="",
                        options=[
                            ft.dropdown.Option(tag[0]) 
                            for tag in db.query(Tag.tag_nm).distinct().all()
                        ],
                        on_change=lambda e: show_category_recipes(page, db, e.data) if e.data else None
                    ),
                    border_radius=10,
                    padding=ft.padding.only(left=7),
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=ft.colors.WHITE,
        padding=10,
        border_radius=10,
    )
    
    lv.controls.append(search_row)
    
    # Favorites button with improved styling
    lv.controls.append(
        ft.Container(
            content=ft.ElevatedButton(
                text="Избранное",
                on_click=lambda _: show_favorites(page, db),
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BROWN,
                    color=ft.colors.WHITE,
                    padding=15,
                    shadow_color=ft.colors.BROWN_200,
                ),
                width=page.window_width - 40,  # Full width minus padding
            ),
            padding=ft.padding.only(top=10, bottom=10),
        )
    )

    # Categories section with improved styling
    lv.controls.append(
        ft.Container(
            content=ft.Text(
                "Популярные категории:",
                weight="bold",
                size=20,
                color=ft.colors.BROWN_900,
            ),
            padding=ft.padding.only(top=20, bottom=10),
        )
    )

    # Category buttons with consistent styling
    for category in ["Завтраки", "Обеды"]:
        lv.controls.append(
            ft.Container(
                content=ft.ElevatedButton(
                    text=category,
                    on_click=lambda _, c=category: show_category_recipes(page, db, c),
                    style=ft.ButtonStyle(
                        bgcolor=ft.colors.BROWN,
                        color=ft.colors.WHITE,
                        padding=15,
                        shadow_color=ft.colors.BROWN_200,
                    ),
                    width=page.window_width - 40,
                ),
                padding=ft.padding.only(bottom=10),
            )
        )

    page.add(lv)
    print("Home page отображен")

def search_recipes(e, db, page):
    search_query = e.control.value.lower()
    page.controls.clear()  # Clear the current page
    
    # Create a new ListView for search results
    lv = ft.ListView(expand=1, spacing=20, padding=20, auto_scroll=True)
    
    if search_query:
        # Get filtered recipes
        filtered_recipes = [
            recipe for recipe in get_all_recipes(db) 
            if search_query in recipe.recipe_nm.lower()
        ]
        
        # Add search results header
        lv.controls.append(ft.Text("Результаты поиска:", size=24, weight="bold"))
        
        if filtered_recipes:
            # Add each recipe card
            for recipe in filtered_recipes:
                recipe_card = ft.Column(
                    controls=[
                        ft.Image(
                            src=recipe.recipe_image,
                            width=300,
                            height=200,
                            border_radius=10,
                            fit=ft.ImageFit.COVER
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.icons.LIGHTBULB_OUTLINE_ROUNDED, color="brown"),
                                            ft.Text(f"{recipe.portion}", size=16),
                                        ],
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.icons.ACCESS_TIME, color="brown"),
                                            ft.Text(f"{recipe.cooking_time}", size=16),
                                        ],
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            padding=10,
                            bgcolor=ft.colors.WHITE,
                            border_radius=10,
                        ),
                        ft.Text(recipe.recipe_nm, size=20, weight="bold"),
                        ft.ElevatedButton(
                            text="Открыть рецепт",
                            on_click=lambda _, name=recipe.recipe_nm: show_recipe(page, db, name),
                            style=ft.ButtonStyle(
                                bgcolor="brown",
                                color="white",
                            )
                        ),
                    ],
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
                
                lv.controls.append(
                    ft.Container(
                        content=recipe_card,
                        padding=15,
                        border_radius=10,
                        bgcolor=ft.colors.WHITE,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=4,
                            color=ft.colors.GREY_300,
                        ),
                        margin=ft.margin.only(bottom=20),
                    )
                )
        else:
            lv.controls.append(ft.Text("Нет рецептов по запросу", size=16))
    
    # Add return button centered
    lv.controls.append(
        ft.Container(
            content=ft.ElevatedButton(
                text="Вернуться",
                on_click=lambda _: return_to_home(page),
                style=ft.ButtonStyle(
                    bgcolor="brown",
                    color="white",
                )
            ),
            alignment=ft.alignment.center,
        )
    )
    
    page.add(lv)
    page.update()



def show_favorites(page, db):
    print("show_favorites вызван")
    page.controls.clear()
    favorite_recipes = get_favorite_recipes(db)
    
    lv = ft.ListView(expand=1, spacing=20, padding=20, auto_scroll=True)
    lv.controls.append(ft.Text("Избранные рецепты", size=24, weight="bold"))
    
    if favorite_recipes:
        for recipe in favorite_recipes:
            recipe_card = ft.Column(
                controls=[
                    ft.Image(
                        src=recipe.recipe_image,
                        width=300,
                        height=200,
                        border_radius=10,
                        fit=ft.ImageFit.COVER
                    ),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.icons.LIGHTBULB_OUTLINE_ROUNDED, color="brown"),
                                        ft.Text(f"{recipe.portion}", size=16),
                                    ],
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.icons.ACCESS_TIME, color="brown"),
                                        ft.Text(f"{recipe.cooking_time} мин", size=16),
                                    ],
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        padding=10,
                        bgcolor=ft.colors.WHITE,
                        border_radius=10,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=4,
                            color=ft.colors.GREY_300,
                        )
                    ),
                    ft.Text(recipe.recipe_nm, size=20, weight="bold"),
                    ft.ElevatedButton(
                        text="Открыть рецепт",
                        on_click=lambda _, name=recipe.recipe_nm: show_recipe(page, db, name),
                        style=ft.ButtonStyle(
                            bgcolor="brown",
                            color="white",
                        )
                    ),
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            
            lv.controls.append(
                ft.Container(
                    content=recipe_card,
                    padding=15,
                    border_radius=10,
                    bgcolor=ft.colors.WHITE,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=4,
                        color=ft.colors.GREY_300,
                    ),
                    margin=ft.margin.only(bottom=20),
                )
            )
    else:
        lv.controls.append(ft.Text("Нет избранных рецептов"))
    
    lv.controls.append(
        ft.ElevatedButton(
            text="Вернуться",
            on_click=lambda _: return_to_home(page),
            style=ft.ButtonStyle(
                bgcolor="brown",
                color="white",
            )
        )
    )
    page.add(lv)

def show_recipe(page, db, recipe_name):
    page.controls.clear()
    recipe = get_recipe_by_name(db, recipe_name)

    if not recipe:
        page.add(ft.Text("Рецепт не найден"))
        return

    lv = ft.ListView(expand=1, spacing=15, padding=20, auto_scroll=True)

    # Заголовок и изображение
    lv.controls.append(
        ft.Container(
            content=ft.Column([
                ft.Text(recipe_name, size=24, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Image(
                    src=recipe.recipe_image,
                    width=300,
                    height=200,
                    border_radius=25,
                    fit=ft.ImageFit.COVER
                ),
            ]),
            alignment=ft.alignment.center,
        )
    )

    # Информация о времени готовки и порциях
    if recipe.cooking_time is not None:
        lv.controls.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(name=ft.icons.ACCESS_TIME, color="brown"),
                                ft.Text(f"{recipe.cooking_time}", size=16),
                            ]),
                            padding=10,
                            border_radius=10,
                            bgcolor=ft.colors.BROWN_50,
                        ),
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(name=ft.icons.PEOPLE, color="brown"),
                                ft.Text(f"{recipe.portion}", size=16),
                            ]),
                            padding=10,
                            border_radius=10,
                            bgcolor=ft.colors.BROWN_50,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                margin=ft.margin.only(top=10, bottom=10),
            )
        )

    # Ингредиенты
    ingredients_list = ft.Column(controls=[], spacing=5)
    for recipe_ingredient in db.query(RecipeHasIngredient).filter(RecipeHasIngredient.recipe_id == recipe.recipe_id).all():
        ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == recipe_ingredient.ingredient_id).first()
        if ingredient:
            ingredients_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(name=ft.icons.CIRCLE, size=8, color="brown"),
                            ft.Text(f"{ingredient.ingredient_nm}: {recipe_ingredient.req_amount}", size=16),
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.only(left=10),
                )
            )

    lv.controls.append(
        ft.Container(
            content=ft.Column([
                ft.Text("Ингредиенты", size=20, weight="bold"),
                ingredients_list,
            ]),
            border=ft.border.all(2, color="brown"),
            border_radius=10,
            padding=15,
            bgcolor=ft.colors.WHITE,
        )
    )

    # Инструкции
    lv.controls.append(
        ft.Container(
            content=ft.Column([
                ft.Text("Инструкция", size=20, weight="bold"),
                ft.Text(recipe.recipe_instructions, size=16),
            ]),
            border=ft.border.all(2, color="brown"),
            border_radius=10,
            padding=15,
            bgcolor=ft.colors.WHITE,
        )
    )

    # Кнопки действий
    favorite_button = ft.ElevatedButton(
        text="Добавить в избранное" if not recipe.is_favorite else "Удалить из избранного",
        style=ft.ButtonStyle(
            bgcolor="brown",
            color="white",
        ),
    )

    def handle_favorite_click(_):
        toggle_favorite(db, recipe_name)
        recipe.is_favorite = not recipe.is_favorite
        favorite_button.text = "Удалить из избранного" if recipe.is_favorite else "Добавить в избранное"
        page.update()

    favorite_button.on_click = handle_favorite_click

    lv.controls.append(
        ft.Container(
            content=ft.Column([
                favorite_button,
                ft.ElevatedButton(
                    text="Вернуться",
                    on_click=lambda _: return_to_home(page),
                    style=ft.ButtonStyle(
                        bgcolor="brown",
                        color="white",
                    ),
                ),
            ]),
            padding=10,
            alignment=ft.alignment.center,
        )
    )

    page.add(lv)



def show_category_recipes(page, db, category):
    page.controls.clear()
    
    # Получаем рецепты по тегу (категории)
    filtered_recipes = get_recipes_by_tag(db, category)
    if filtered_recipes:
        lv = ft.ListView(expand=1, spacing=20, padding=20, auto_scroll=True)
        
        # Добавляем заголовок категории
        lv.controls.append(ft.Text(f"Категория: {category}", size=24, weight="bold"))
        for recipe in filtered_recipes:
            # Создаем карточку рецепта
            recipe_card = ft.Column(
                controls=[
                    # Изображение рецепта
                    ft.Image(
                        src=recipe.recipe_image,
                        width=300,
                        height=200,
                        border_radius=10,
                        fit=ft.ImageFit.COVER
                    ),
                    
                    # Информация о приготовлении
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(f" ", size=10),
                                        ft.Icon(name=ft.icons.LIGHTBULB_OUTLINE_ROUNDED, color="brown"),
                                        ft.Text(f"{recipe.portion}", size=16),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.icons.ACCESS_TIME, color="brown"),
                                        ft.Text(f"{recipe.cooking_time}   ", size=16),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            spacing=20,
                        ),
                        padding=10,
                        margin=ft.margin.only(top=10, bottom=10),
                        bgcolor=ft.colors.WHITE,
                        border_radius=10,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=4,
                            color=ft.colors.GREY_300,
                        )
                    ),
                    
                    # Название рецепта
                    ft.Text(recipe.recipe_nm, size=20, weight="bold"),
                    
                    # Кнопка открытия рецепта
                    ft.ElevatedButton(
                        text="Открыть рецепт",
                        on_click=lambda _, name=recipe.recipe_nm: show_recipe(page, db, name),
                        style=ft.ButtonStyle(
                            bgcolor="brown",
                            color="white",
                        )
                    ),
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            
            # Добавляем карточку в контейнер с отступами и границей
            lv.controls.append(
                ft.Container(
                    content=recipe_card,
                    padding=15,
                    border_radius=10,
                    bgcolor=ft.colors.WHITE,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=4,
                        color=ft.colors.GREY_300,
                    ),
                    margin=ft.margin.only(bottom=20),
                )
            )
        
        page.add(lv)
    else:
        page.add(ft.Text(f"Нет рецептов в категории {category}"))
    
    # Кнопка возврата
    page.add(
        ft.ElevatedButton(
            text="Вернуться",
            on_click=lambda _: return_to_home(page),
            style=ft.ButtonStyle(
                bgcolor="brown",
                color="white",
            )
        )
    )

# Возврат на главную страницу
def return_to_home(page):
    page.controls.clear()
    db = SessionLocal()  # Создаем сессию базы данных
    show_home_page(page, db)
    db.close()  # Закрываем сессию после использования

# Основной метод
def main(page: ft.Page):
    print("main вызван")  # Отладочное сообщение
    page.title = "Приложение рецептов"
    page.window_max_width = 360
    page.window_width = 360
    page.window_max_height = 640
    page.window_height = 640
    page.theme = ft.Theme(color_scheme_seed="brown")

    db = SessionLocal()  # Создаем сессию базы данных
    show_home_page(page, db)
    db.close()  # Закрываем сессию после использования

# Запуск приложения
ft.app(target=main)
