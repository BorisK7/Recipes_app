from flet import * 
import flet as fl


def main(page: fl.Page):
    page.title ="App"

    class Searcherc(UserControl):
        def __init__(self):
            super().__init__()
            self.text_fld = Container(
                TextField(label='Search',bgcolor='#FFFFFF',border_radius=20,border_width=3,width=250),
                
                padding=padding.all(5),
            )
            self.search_btn = Container(
                IconButton(icon=icons.SEARCH,icon_size=30,icon_color='black',bgcolor='white'),
                padding=padding.all(5),
            )
            self.menu = Container(
                Row([
                    self.text_fld,
                    self.search_btn,
                ]),
                height=75,
                bgcolor=colors.with_opacity(0.5,'white'),
                padding=padding.only(10,20,10,0)
            )
        def build(self):
            return self.menu
         
    page.window_max_width=360
    page.window_width=360
    page.window_max_height=640
    page.window_height=640

    body = Container(
        #Row([
        #    TextField(label='Search',bgcolor='#FFFFFF',border_radius=20,border_width=3),
        #]),
        Column([
            Searcherc(),
        ]),
        gradient=LinearGradient(
            colors=['white','#ffcc99'],
            end=alignment.top_left,
            begin=alignment.bottom_right,
        ),
        width=360,
        height=640,
    )

    page.padding=0
    page.add(
        body
     )
fl.app(target=main)
