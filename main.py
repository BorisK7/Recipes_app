import flet as ft

# Список рецептов
recipes = {
    "Омлет": {
        "category": "Завтраки",
        "image": "assets\\Omlet.jpg", 
        "ingredients": ["Яйца", "Молоко", "Соль", "Перец"],
        "instructions": ["Взбить яйца с молоком", "Разогреть сковороду", "Влить смесь на сковороду", "Жарить до готовности"],
        "is_favorite": False,
        "tags": ["breakfast"]
    },
    "Борщ": {
        "category": "Обеды",
        "image": "assets\\Borsch.jpg", 
        "ingredients": ["Свекла", "Капуста", "Мясо", "Картофель"],
        "instructions": ["Отварить мясо", "Добавить нарезанную свеклу и капусту", "Варить до готовности"],
        "is_favorite": False,
        "tags": ["dinner"]
    },
    "Яичница": {
        "category": "Завтраки",
        "image": "assets\\Eggs.jpg",  
        "ingredients": ["Яйца", "Молоко", "Соль", "Перец"],
        "instructions": ["Взбить яйца", "Обжарить на сковороде"],
        "is_favorite": False,
        "tags": ["breakfast"]
    },
    "Рис с курицей": {
        "category": "Обеды",
        "image": "assets\\Chiken_with_rice.jpg",  
        "ingredients": ["Рис", "Курица", "Соль", "Перец"],
        "instructions": ["Отварить рис", "Обжарить курицу", "Смешать и подать"],
        "is_favorite": False,
        "tags": ["dinner"]
    }
}


def main(page: ft.Page):
    page.title = "Приложение рецептов"
    page.window_max_width = 360
    page.window_width = 360
    page.window_max_height = 640
    page.window_height = 640
    page.theme = ft.Theme(color_scheme_seed="brown")

    # Функция для обновления избранного
    def toggle_favorite(recipe_name):
        recipes[recipe_name]["is_favorite"] = not recipes[recipe_name]["is_favorite"]
        update_favorite_button(recipe_name)

    # Функция для обновления состояния избранного
    def update_favorite_button(recipe_name):
        if recipes[recipe_name]["is_favorite"]:
            favorite_button.text = "Удалить из избранного"
        else:
            favorite_button.text = "Добавить в избранное"

    # Страница рецепта
    def show_recipe(recipe_name):
        recipe = recipes[recipe_name]
        page.controls.clear()

        # Оборачиваем все в ListView, чтобы добавить прокрутку
        lv = ft.ListView(
            expand=1, 
            spacing=10,
            padding=20,
            auto_scroll=True,
        )

        # Добавляем все элементы в ListView
        lv.controls.append(ft.Text(recipe_name, size=24, weight="bold"))
        lv.controls.append(
            ft.Column(
                [
                    ft.Image(
                        src=recipe["image"], 
                        width=300, 
                        height=200,
                        border_radius=25  
                    )
                ], 
                alignment=ft.alignment.center 
            )
        )
        # Оформление ингредиентов в рамке
        lv.controls.append(
            ft.Container(
                content=ft.Column([ 
                    ft.Text("Ингредиенты:"),
                    ft.Text("\n".join(recipe["ingredients"]))
                ]),
                border=ft.border.all(2,color='brown'),  
                padding=10,  
                border_radius=10  
            )
        )
        # Оформление инструкций в рамке
        lv.controls.append(
            ft.Container(
                content=ft.Column([ 
                    ft.Text("Инструкция:"),
                    ft.Text("\n".join(recipe["instructions"]))
                ]),
                border=ft.border.all(2,color='brown'),  
                padding=10,
                border_radius=10  
            )
        )
        lv.controls.append(
            ft.ElevatedButton(
                text="Вернуться", on_click=lambda _: return_to_home()
            )
        )
        lv.controls.append(
            ft.ElevatedButton(
                text="Добавить в избранное" if not recipe["is_favorite"] else "Удалить из избранного",
                on_click=lambda e: toggle_favorite(recipe_name)
            )
        )

        #+ListView на страницу
        page.add(lv)

    # Страница избранного
    def show_favorites():
        page.controls.clear() 
        favorite_recipes = {name: recipe for name, recipe in recipes.items() if recipe["is_favorite"]}
        if favorite_recipes:
            for recipe_name in favorite_recipes:
                page.add(
                    ft.ElevatedButton(
                        text=recipe_name,
                        on_click=lambda _, name=recipe_name: show_recipe(name)
                    )
                )
        else:
            page.add(ft.Text("Нет избранных рецептов"))
        page.add(ft.ElevatedButton(text="Вернуться", on_click=lambda _: return_to_home()))

    # Главная страница
    def show_home_page():
        page.controls.clear() 
        page.add(
            ft.Column(
                [
                    ft.TextField(label="Поиск рецепта", on_submit=search_recipes),  
                    ft.ElevatedButton(
                        text="Избранное", on_click=lambda _: show_favorites()
                    ),
                    ft.Text("Категории:"),
                    ft.ElevatedButton(
                        text="Завтраки", on_click=lambda _: show_category_recipes("breakfast")
                    ),
                    ft.ElevatedButton(
                        text="Обеды", on_click=lambda _: show_category_recipes("dinner")
                    ),
                    search_results_column  
                ]
            )
        )
        # Сброс состояния поиска 
        search_results_column.controls.clear()

    # Страница рецептов по категориям
    def show_category_recipes(category):
        page.controls.clear()  
        filtered_recipes = {name: recipe for name, recipe in recipes.items() if category in recipe["tags"]}

        if filtered_recipes:
            lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)  

            for recipe_name, recipe in filtered_recipes.items():
                lv.controls.append(
                    ft.Column(
                        [
                            ft.Column(
                                [
                                    ft.Image(
                                        src=recipe["image"], 
                                        width=300, height=200,  
                                        border_radius=25  
                                    )
                                ],
                                alignment=ft.alignment.center  
                            ),
                            ft.Text(recipe_name, weight="bold"),  
                            ft.ElevatedButton(
                                text="Открыть рецепт",
                                on_click=lambda _, name=recipe_name: show_recipe(name)
                            )
                        ]
                    )
                )

            page.add(lv)
        else:
            page.add(ft.Text(f"Нет рецептов в категории {category}"))
        page.add(ft.ElevatedButton(text="Вернуться", on_click=lambda _: return_to_home()))

    # Поиск рецептов (срабатывает при нажатии Enter)
    def search_recipes(e):
        search_query = e.control.value.lower()

        search_results_column.controls.clear()

        # Если запрос не пустой, ищем рецепты
        if search_query:
            filtered_recipes = {name: recipe for name, recipe in recipes.items() if search_query in name.lower()}

            # "Результаты по поиску: запрос"
            search_results_column.controls.append(
                ft.Text(f"Результаты по поиску: {search_query}", size=20, weight="bold")
            )

            if filtered_recipes:
                for recipe_name in filtered_recipes:
                    search_results_column.controls.append(
                        ft.ElevatedButton(
                            text=recipe_name,
                            on_click=lambda _, name=recipe_name: show_recipe(name)
                        )
                    )
            else:
                search_results_column.controls.append(ft.Text("Нет рецептов по запросу"))

        page.update()

    # Колонка для отображения результатов поиска
    search_results_column = ft.Column()  

    # Функция для возврата на главную страницу
    def return_to_home():
        page.controls.clear() 
        show_home_page()

    show_home_page()

ft.app(target=main)
