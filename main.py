import flet as ft
from router import Router
import subprocess
import sys
import os
import threading

router = None

def init_router(page: ft.Page):
    global router
    router = Router(page)
    router.add_route("/", main)
    return router
#Funciones para el routing con las imagenes 
def launch_user_process():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        user_path = os.path.join(current_dir, "user.py")
        
        startupinfo = None
        if sys.platform.startswith('win'):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(
                [sys.executable, user_path],
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        else:
            subprocess.Popen(
                [sys.executable, user_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
    except Exception as e:
        print(f"Error al abrir user.py: {e}")

def launch_chat_process():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        chat_path = os.path.join(current_dir, "chat.py")
        
        startupinfo = None
        if sys.platform.startswith('win'):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(
                [sys.executable, chat_path],
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        else:
            subprocess.Popen(
                [sys.executable, chat_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
    except Exception as e:
        print(f"Error al abrir chat.py: {e}")

def main(page: ft.Page):
    page.title = "HOME VIEW"
    page.bgcolor = "#FFFFFF"
    page.padding = 0
    page.spacing = 0
   
    page.fonts = {
        "Instrument Sans": "https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&display=swap"
    }

    def navigate_to_menstruation_tips(e):
        page.launch_url("https://www.intimina.com/es/blog/higiene-menstrual/")
        
    def navigate_to_std_info(e):
        page.launch_url("https://www.plannedparenthood.org/es/temas-de-salud/enfermedades-de-transmision-sexual-ets")

    def navigate_to_std_info2(e):
        page.launch_url("https://www.gacetasanitaria.org/es-salud-equidad-justicia-menstrual-saberes-articulo-S0213911124000037")
    
    main_column = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )
    
    # Optimización: Carga de imágenes bajo demanda
    header = ft.Container(
        content=ft.Stack(
            controls=[
                ft.Container(
                    content=ft.Image(
                        src="/img/header.png",
                        width=page.width,
                        height=800,
                        fit=ft.ImageFit.COVER,
                    ),
                    bgcolor="#FFB6C1",
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Image(
                                    src="/img/kliaassits.png",
                                    width=60,
                                    height=60,
                                ),
                                border_radius=30,
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            ),
                            ft.Text(
                                "Welcome \"Your name\"",
                                size=18,
                                weight=ft.FontWeight.W_600,
                                color="#4A4A4A",
                                font_family="Instrument Sans",
                            ),
                        ],
                        spacing=15,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=ft.padding.only(left=20, top=30),
                ),
            ],
        ),
        height=80,
    )

    todays_phrase = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Today's phrase",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color="#4A4A4A",
                    font_family="Instrument Sans",
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "\"Science and everyday life cannot and should not be separated.\"",
                                size=16,
                                color="#666666",
                                text_align=ft.TextAlign.CENTER,
                                font_family="Instrument Sans",
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Text(
                                "— Rosalind Franklin",
                                size=14,
                                color="#666666",
                                text_align=ft.TextAlign.CENTER,
                                font_family="Instrument Sans",
                                weight=ft.FontWeight.W_400,
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    bgcolor="#FFB6C1",
                    border_radius=15,
                    padding=20,
                    margin=ft.margin.symmetric(vertical=10),
                    border=ft.border.all(width=2, color="#FF99B4"),
                ),
            ],
            spacing=10,
        ),
        padding=20,
    )

    you_might_like = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "You Might Like...",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color="#4A4A4A",
                    font_family="Instrument Sans",
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.GestureDetector(
                                content=ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Text(
                                                "tips for menstruation.....",
                                                color="#666666",
                                                font_family="Instrument Sans",
                                                weight=ft.FontWeight.W_500,
                                                size=14,
                                            ),
                                            ft.Icon(
                                                name=ft.icons.ARROW_FORWARD_IOS_ROUNDED,
                                                color="#666666",
                                                size=20,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    padding=15,
                                    bgcolor="#E6E6FA",
                                    border_radius=10,
                                    border=ft.border.all(width=2, color="#C6C6FA"),
                                ),
                                on_tap=navigate_to_menstruation_tips,
                            ),
                            ft.GestureDetector(
                                content=ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Text(
                                                "sexually transmitted diseases",
                                                color="#666666",
                                                font_family="Instrument Sans",
                                                weight=ft.FontWeight.W_500,
                                                size=14,
                                            ),
                                            ft.Icon(
                                                name=ft.icons.ARROW_FORWARD_IOS_ROUNDED,
                                                color="#666666",
                                                size=20,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    bgcolor="#E6E6FA",
                                    padding=15,
                                    border_radius=10,
                                    margin=ft.margin.only(top=10),
                                    border=ft.border.all(width=2, color="#C6C6FA"),
                                ),
                                on_tap=navigate_to_std_info,
                            ),
                        ],
                    ),
                ),
            ],
            spacing=10,
        ),
        padding=20,
    )

    explore_more = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Explore More of What You Discovered...",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color="#4A4A4A",
                    font_family="Instrument Sans",
                ),
                ft.GestureDetector(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    content=ft.Text(
                                        "Collective knowledge and epistemological transformations: trajectories in menstrual research",
                                        color="#FFFFFF",
                                        font_family="Instrument Sans",
                                        weight=ft.FontWeight.W_500,
                                        size=14,
                                        text_align=ft.TextAlign.LEFT,
                                    ),
                                    width=300,
                                ),
                                ft.Container(
                                    content=ft.Icon(
                                        name=ft.icons.ARROW_FORWARD_IOS_ROUNDED,
                                        color="#FFFFFF",
                                        size=20,
                                    ),
                                    alignment=ft.alignment.center_right,
                                    margin=ft.margin.only(top=10),
                                ),
                            ],
                        ),
                        bgcolor="#C71585",
                        padding=20,
                        border_radius=10,
                        margin=ft.margin.only(top=10),
                        border=ft.border.all(width=2, color="#A71565"),
                        width=340,
                    ),
                    on_tap=navigate_to_std_info2,
                ),
            ],
        ),
        padding=20,
    )
    #hago con un if else dependiendo de el index del navbar 
    def handle_navigation_change(e):
        index = e.control.selected_index
        if index == 5:  # USER
            thread = threading.Thread(target=launch_user_process)
            thread.daemon = True
            thread.start()
            page.window_destroy()
        elif index == 1:  # CHAT
            thread = threading.Thread(target=launch_chat_process)
            thread.daemon = True
            thread.start()
            page.window_destroy()

    navigation_bar = ft.NavigationBar(
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
        selected_index=0,
        on_change=handle_navigation_change,
        height=65,
        label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
    )
            

    main_column.controls = [
        header,
        todays_phrase,
        you_might_like,
        explore_more,
    ]

    page_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=main_column,
                    expand=True,
                ),
                navigation_bar,
            ],
            spacing=0,
        ),
        expand=True,
    )

    page.add(page_container)

if __name__ == "__main__":
    ft.app(target=main, assets_dir=".")