import flet as ft

def main(page: ft.Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.window.maximized = True
    page.window.resizable = False
    
    login = ft.Column([
        ft.Container(
            bgcolor= ft.colors.GREEN_200,
            width=page.window.width - 10,
            height= page.window - 60,
            border_radius= 10,
            
            content=ft.Column([
                ft.Container(
                    bgcolor=ft.colors.WHITE70,
                    width=400,
                    height=320,
                    border_radius=10,
                    
                )
            ]horizontal_aligment='center',alignment='center')
        )
    ])