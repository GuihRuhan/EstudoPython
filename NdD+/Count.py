import flet as ft

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_maximized = True
    page.window_resizable = False

    login = ft.Column([
        ft.Container(
            bgcolor=ft.Colors.GREEN_200,  # Atualizado para a nova enum
            width=page.width - 10,  # Corrigido para o atributo correto
            height=page.height - 60,  # Corrigido para o atributo correto
            border_radius=10,
            content=ft.Column(
                [
                    ft.Container(
                        bgcolor=ft.Colors.WHITE70,  # Atualizado para a nova enum
                        width=400,
                        height=320,
                        border_radius=10,
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Ajustado para a sintaxe correta
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
    ])

    page.add(login)

ft.app(target=main)
