import sqlite3
import flet as ft
from flet import *
from config import create_tabs
import state

def main(page: ft.Page):
    state.username_input = ft.TextField(label="Username", width=300)
    state.password_input = ft.TextField(label="Password", password=True, width=300, can_reveal_password=True)
    
    def on_login(e):
        name = state.username_input.value
        password = state.password_input.value

        if name.strip() == '' or password.strip() == '':
            page.open(dlg_modal)
        else:
            insert_data(name, password)
            print(f"Username: {name}, Password: {password}")

    login_button = ft.ElevatedButton(text="Login", on_click=on_login, height=40, width=150)

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    con = sqlite3.connect('Data.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS user (name TEXT NOT NULL, password TEXT NOT NULL)')

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()

        if page.route == '/':
            page.views.append(
                View(
                    route='/',
                    controls=[
                        AppBar(title=Text('Regestration'), bgcolor='blue'),
                        Text(value='Regestration', size=30),
                        state.username_input,
                        state.password_input,
                        login_button,
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=10
                )
            )
        elif page.route == '/home':
            tabs = create_tabs()
            page.views.append(
                View(
                    route='/home',
                    controls=[
                        AppBar(title=Text('Home'), bgcolor='blue'),
                        Text(value=f'Welcome {state.username_input.value}', size=30),
                        tabs,
                        ElevatedButton(text='Go back', on_click=lambda _: page.go('/'))
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=25
                )
            )

        page.update()

    def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        if page.views:
            top_view: View = page.views[-1]
            page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    def insert_data(name, password):
        con = sqlite3.connect('Data.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM user WHERE name = ? AND password = ?', (name, password))
        user = cur.fetchone()

        if user:
            dlg_modal.title = ft.Text('Авторизация')
            dlg_modal.content = ft.Text(f'Вы успешно вошли в аккаунт {state.username_input.value}')
            page.go('/home')
        else:
            cur.execute('INSERT INTO user (name, password) VALUES (?, ?)', (name, password))
            dlg_modal.title = ft.Text('Регистрация')
            dlg_modal.content = ft.Text(f'Вы успешно зарегистрировали аккаунт {state.username_input.value}')

        page.open(dlg_modal)
        con.commit()
        con.close()

    def handle_close(e):
        page.close(dlg_modal)

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text('Предупреждение'),
        content=ft.Text('Поля ввода не должны быть пустыми'),
        actions=[ft.Button(text='OK', on_click=handle_close)]
    )

    page.add(state.username_input, state.password_input, login_button)

    con.commit()
    con.close()

ft.app(target=main, port=8000, view=ft.AppView.WEB_BROWSER)