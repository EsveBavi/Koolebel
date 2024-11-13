import flet as ft
from typing import List
from router import Router
import subprocess
import sys
import os
import threading

router = None

def init_router(page: ft.Page):
    global router
    router = Router(page)
    router.add_route("/chat", chat_view)
    return router

def launch_main_process():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(current_dir, "main.py")
        
        startupinfo = None
        if sys.platform.startswith('win'):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(
                [sys.executable, main_path],
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        else:
            subprocess.Popen(
                [sys.executable, main_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
    except Exception as e:
        print(f"Error al abrir main.py: {e}")

class ChatMessage:
    def __init__(self, text: str, is_bot: bool):
        self.text = text
        self.is_bot = is_bot

class ChatBotApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = "#F0F0F0"
        self.page.padding = 0
        self.messages: List[ChatMessage] = []
        self.setup_ui()

    def setup_ui(self):
        # Configuración de imágenes de perfil
        self.bot_profile = "/api/placeholder/50/50"
        self.user_profile = "/api/placeholder/50/50"

        # Header del chat
        self.header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color="#4A4A4A",
                        on_click=self.go_back
                    ),
                    ft.Text(
                        "Your name",
                        size=20,
                        color="#4A4A4A",
                        weight=ft.FontWeight.BOLD
                    ),
                ],
            ),
            padding=10,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=4,
                color=ft.colors.BLACK12,
            )
        )

        # Chat messages container
        self.chat_container = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=True
        )

        # Input field container
        self.input_field = ft.TextField(
            hint_text="Have a question about sexual health or family planning? Ask me and learn more!",
            border_radius=25,
            expand=True,
            bgcolor=ft.colors.WHITE,
            border_color=ft.colors.TRANSPARENT,
            height=50,
            text_size=14,
            content_padding=ft.padding.only(left=20, right=20),
            on_submit=self.send_message,
        )

        self.send_button = ft.IconButton(
            icon=ft.icons.ARROW_FORWARD,
            icon_color=ft.colors.WHITE,
            bgcolor="#D65DB1",
            on_click=self.send_message,
        )

        self.input_container = ft.Container(
            content=ft.Row(
                controls=[
                    self.input_field,
                    ft.Container(
                        content=self.send_button,
                        bgcolor="#D65DB1",
                        border_radius=25,
                        padding=5,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.only(left=20, right=20, bottom=20, top=10),
        )

        def handle_navigation_change(e):
            index = e.control.selected_index
            if index == 0:  # HOME
                thread = threading.Thread(target=launch_main_process)
                thread.daemon = True
                thread.start()
                self.page.window_destroy()

        # Navigation bar actualizada
        self.nav_bar = ft.NavigationBar(
            bgcolor="#FFE1E1",
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.HOME_OUTLINED,
                    selected_icon=ft.icons.HOME_FILLED,
                    label="HOME",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.CHAT_BUBBLE_OUTLINE,
                    selected_icon=ft.icons.CHAT_BUBBLE,
                    label="CHAT",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.MAP_OUTLINED,
                    selected_icon=ft.icons.MAP,
                    label="MAPS",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.GROUPS_OUTLINED,
                    selected_icon=ft.icons.GROUPS,
                    label="FORUM",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.BOOK_OUTLINED,
                    selected_icon=ft.icons.BOOK,
                    label="NOTES",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.PERSON_OUTLINE,
                    selected_icon=ft.icons.PERSON,
                    label="USER",
                ),
            ],
            selected_index=1,
            on_change=handle_navigation_change,
            height=65,
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
        )

        # Main layout
        self.page.add(
            ft.Column(
                controls=[
                    self.header,
                    self.chat_container,
                    self.input_container,
                    self.nav_bar,
                ],
                expand=True,
            )
        )

        # Add initial messages
        self.add_message("Lorem ipsum dolor sit amet, consectetur adipiscing elit..", True)
        self.add_message("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum id ligula porta felis euismod semper.", False)
        self.add_message("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed auctor neque eu tellus rhoncus ut eleifend nibh porttitor. Ut in nulla enim.", True)
        self.add_message("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum id ligula porta felis euismod semper.", False)

    def create_message_bubble(self, message: ChatMessage) -> ft.Container:
        profile_picture = ft.Container(
            content=ft.CircleAvatar(
                foreground_image_url=self.bot_profile if message.is_bot else self.user_profile,
                radius=20,
            ),
            margin=ft.margin.only(right=10 if message.is_bot else 0, left=0 if message.is_bot else 10),
        )

        bubble = ft.Container(
            content=ft.Text(
                message.text,
                color=ft.colors.WHITE if message.is_bot else ft.colors.BLACK,
                size=14,
            ),
            bgcolor="#D65DB1" if message.is_bot else "#FFF9C4",
            border_radius=ft.border_radius.all(15),
            padding=ft.padding.all(15),
            width=280,
        )

        return ft.Row(
            controls=[
                profile_picture if message.is_bot else bubble,
                bubble if message.is_bot else profile_picture,
            ],
            alignment="start" if message.is_bot else "end",
        )

    def add_message(self, text: str, is_bot: bool):
        message = ChatMessage(text, is_bot)
        self.messages.append(message)
        self.chat_container.controls.append(self.create_message_bubble(message))
        self.page.update()

    def simulate_bot_response(self, e):
        self.add_message("Thank you for your question! I'm here to help.", True)

    def send_message(self, e):
        text = self.input_field.value
        if text:
            self.add_message(text, False)
            self.input_field.value = ""
            self.page.update()
            self.page.after(1000, self.simulate_bot_response)

    def go_back(self, e):
        thread = threading.Thread(target=launch_main_process)
        thread.daemon = True
        thread.start()
        self.page.window_destroy()

def chat_view(page: ft.Page):
    page.title = "CHAT VIEW"
    ChatBotApp(page)

if __name__ == "__main__":
    ft.app(target=chat_view, assets_dir=".")