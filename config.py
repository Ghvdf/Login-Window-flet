# config.py
import flet as ft
import state

def create_tabs():
    tabs = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                tab_content=ft.Icon(ft.Icons.HOME),
                content=ft.Text(value=f'Привет {state.username_input.value}')
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.Icons.SEARCH),
                content=ft.Text("This is Tab 2"),
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.Icons.SETTINGS),
                content=ft.Row(
                    controls=[],
                    alignment=ft.MainAxisAlignment.CENTER  # Выравнивание по центру
                ),
            ),
        ],
        expand=1,
    )
    return tabs