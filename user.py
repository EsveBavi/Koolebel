import flet as ft
import subprocess
import sys
import os
import threading
from dataclasses import dataclass
from typing import Callable, List

@dataclass
class MenuItem:
    icon: str
    title: str
    route: str

class SettingsManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.setup_routes()
        self.page.go(self.page.route)
        
    def setup_page(self):
        self.page.title = "SETTINGS"
        self.page.bgcolor = "#FFFFFF"
        self.page.padding = 20
        self.page.spacing = 0
        self.page.fonts = {
            "Instrument Sans": "https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&display=swap"
        }
        self.page.views.clear()
        self.page.views.append(self.settings_view())

    def setup_routes(self):
        def route_change(route):
            self.page.views.clear()
            self.page.views.append(self.settings_view())
            
            routes = {
                "/edit_profile": "Edit Profile",
                "/security": "Security",
                "/notifications": "Notifications",
                "/privacy": "Privacy",
                "/help_support": "Help & Support",
                "/terms_policies": "Terms and Policies",
                "/free_space": "Free up Space",
                "/data_saver": "Data Saver",
                "/report_problem": "Report a Problem",
                "/add_account": "Add Account",
                "/logout": "Log Out"
            }
            
            if self.page.route in routes:
                self.page.views.append(self.create_page(routes[self.page.route]))
                
            self.page.update()

        def view_pop(view):
            self.page.views.pop()
            top_view = self.page.views[-1]
            self.page.go(top_view.route)

        self.page.on_route_change = route_change
        self.page.on_view_pop = view_pop

    def launch_main_process(self):
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

    def go_to_home(self, e):
        thread = threading.Thread(target=self.launch_main_process)
        thread.daemon = True
        thread.start()
        self.page.window_destroy()

    def create_section(self, title: str, items: List[MenuItem]) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        title,
                        size=20,
                        weight=ft.FontWeight.W_700,
                        color="#4A4A4A",
                        font_family="Instrument Sans",
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.ListTile(
                                    leading=ft.Icon(item.icon, color="#4A4A4A"),
                                    title=ft.Text(
                                        item.title,
                                        size=16,
                                        weight=ft.FontWeight.W_500,
                                        color="#4A4A4A",
                                        font_family="Instrument Sans",
                                    ),
                                    on_click=lambda _, r=item.route: self.page.go(r)
                                ) for item in items
                            ],
                            spacing=0,
                        ),
                        bgcolor="#F5F5F5",
                        border_radius=15,
                        padding=10,
                        margin=ft.margin.only(top=10),
                    )
                ],
                spacing=0,
            ),
            margin=ft.margin.only(bottom=20)
        )

    def create_navigation_bar(self) -> ft.NavigationBar:
        return ft.NavigationBar(
            bgcolor="#FFE1E1",
            destinations=[
                ft.NavigationDestination(
                    icon=ft.icons.HOME_OUTLINED,
                    selected_icon=ft.icons.HOME_FILLED,
                    label="HOME",
                ),
                ft.NavigationDestination(
                    icon=ft.icons.CHAT_BUBBLE_OUTLINE,
                    selected_icon=ft.icons.CHAT_BUBBLE,
                    label="CHAT",
                ),
                ft.NavigationDestination(
                    icon=ft.icons.MAP_OUTLINED,
                    selected_icon=ft.icons.MAP,
                    label="MAPS",
                ),
                ft.NavigationDestination(
                    icon=ft.icons.GROUPS_OUTLINED,
                    selected_icon=ft.icons.GROUPS,
                    label="FORUM",
                ),
                ft.NavigationDestination(
                    icon=ft.icons.BOOK_OUTLINED,
                    selected_icon=ft.icons.BOOK,
                    label="NOTES",
                ),
                ft.NavigationDestination(
                    icon=ft.icons.PERSON_OUTLINE,
                    selected_icon=ft.icons.PERSON,
                    label="USER",
                ),
            ],
            selected_index=5,
            on_change=self.handle_navigation_change,
            height=65,
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
        )

    def handle_navigation_change(self, e):
        if e.control.selected_index == 0:  # HOME
            thread = threading.Thread(target=self.launch_main_process)
            thread.daemon = True
            thread.start()
            self.page.window_destroy()

    def create_page(self, title: str) -> ft.View:
        return ft.View(
            "/"+title.lower().replace(" ", "_"),
            [
                ft.AppBar(
                    leading=ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.page.go("/")
                    ),
                    title=ft.Text(title),
                    bgcolor="#FFFFFF",
                ),
                ft.Text(f"This is {title} page", size=20, text_align=ft.TextAlign.CENTER)
            ]
        )

    def settings_view(self):
        # Define los botones del menu pagina settings
        account_items = [
            MenuItem(ft.icons.PERSON_OUTLINE, "Edit profile", "/edit_profile"),
            MenuItem(ft.icons.SECURITY, "Security", "/security"),
            MenuItem(ft.icons.NOTIFICATIONS_NONE, "Notifications", "/notifications"),
            MenuItem(ft.icons.LOCK_OUTLINE, "Privacy", "/privacy"),
        ]
        
        support_items = [
            MenuItem(ft.icons.HELP_OUTLINE, "Help & Support", "/help_support"),
            MenuItem(ft.icons.DESCRIPTION_OUTLINED, "Terms and Policies", "/terms_policies"),
        ]
        
        cache_items = [
            MenuItem(ft.icons.DELETE_OUTLINE, "Free up space", "/free_space"),
            MenuItem(ft.icons.DATA_USAGE, "Data Saver", "/data_saver"),
        ]
        
        actions_items = [
            MenuItem(ft.icons.FLAG_OUTLINED, "Report a problem", "/report_problem"),
            MenuItem(ft.icons.PERSON_ADD_OUTLINED, "Add account", "/add_account"),
            MenuItem(ft.icons.LOGOUT, "Log out", "/logout"),
        ]

        # Header with back button
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color="#4A4A4A",
                        on_click=self.go_to_home
                    ),
                    ft.Text(
                        "Settings",
                        size=24,
                        weight=ft.FontWeight.W_700,
                        color="#4A4A4A",
                        font_family="Instrument Sans",
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            margin=ft.margin.only(bottom=20)
        )

        # Crea las columnas
        main_column = ft.Column(
            controls=[
                header,
                self.create_section("Account", account_items),
                self.create_section("Support & About", support_items),
                self.create_section("Cache & cellular", cache_items),
                self.create_section("Actions", actions_items),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
        )

        # llama o pone todo el contenido
        page_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=main_column,
                        expand=True,
                    ),
                    self.create_navigation_bar(),
                ],
                spacing=0,
            ),
            expand=True,
        )

        return ft.View(
            "/",
            [page_container],
        )

def main(page: ft.Page):
    SettingsManager(page)

if __name__ == "__main__":
    ft.app(target=main, assets_dir=".")