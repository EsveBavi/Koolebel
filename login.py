import os
import base64
import flet as ft
from flet_core.cupertino_icons import CIRCLE


def getImagenBytes(name_image):
    imagen_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", name_image)
    try:
        with open(imagen_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        print(f"Advertencia la imagen {name_image} no existe en {imagen_path}")
        return None

def main(page: ft.Page):
    page.title = "Kolebel"
    page.padding = 0
    page.spacing = 0

    # sección encabezado
    encabezado = ft.Container(
        content=ft.Column([
            ft.Container(
                image_src_base64=getImagenBytes("logo.png"),
                width=150,
                height=150,
                border_radius=100,
                shape=CIRCLE
            ),
            ft.Text("Koolebel", size=32, color=ft.colors.WHITE)
        ]),
        bgcolor="#C34B89",
        margin=0,
        padding=10,
        alignment=ft.alignment.center,
        width=page.width
    )

    # sección de form
    login_text = ft.Text("LOGIN", size=36, color=ft.colors.BLACK)
    columna_form = ft.Column(
        [
            ft.Text("USERNAME OR EMAIL", size=24, color="#C34B89"),
            ft.TextField(border=ft.InputBorder.OUTLINE, border_radius=10, filled=True, fill_color=ft.colors.WHITE),
            ft.Text("PASSWORD", size=24, color="#C34B89"),
            ft.TextField(border=ft.InputBorder.OUTLINE, border_radius=10, filled=True, fill_color=ft.colors.WHITE),
        ]
    )
    fila_missing = ft.Row(
        controls=[
            ft.Text("Forgot your password?",color=ft.colors.BLACK,size=18),
            ft.TextButton(
                text="Click here",
                style=ft.ButtonStyle(color="#C34B89"),
                height=50
            )
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=0
    )
    login_button = ft.FilledButton(text="SIGN UP", style=ft.ButtonStyle(bgcolor="#C34B89", color=ft.colors.WHITE), width=300)
    gradiente = ft.Container(
        content=ft.Column([login_text,columna_form,fila_missing,login_button]),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[
                "#EEB7CF",
                "#FCCCDC",
                "#FEE5DC",
            ],
            #rotation=math.pi
            #tile_mode=ft.GradientTileMode.MIRROR,
        ),
        alignment=ft.alignment.center,
        width=page.width,
        height=page.height,
        padding=10
    )

    #Imagen decorativa
    container_img = ft.Container(
        image_src_base64=getImagenBytes("glifos.png"),
        width=100,
        height=page.height,
    )
    # debemos definir 2 columnas para poder obtener la otra imagen
    login_column = ft.Column([encabezado,gradiente], spacing=0)
    #login_row = ft.Row([container_img,login_column], spacing=0)
    #page.add(login_row)
    page.add(login_column)

ft.app(target=main)