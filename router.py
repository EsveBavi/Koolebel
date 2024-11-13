import flet as ft

class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.routes = {}
        self.current_route = None

    def add_route(self, route: str, view_function):
        self.routes[route] = view_function

    def route(self, route_path: str):
        if route_path in self.routes:
            self.page.clean()
            self.current_route = route_path
            self.routes[route_path](self.page)
            self.page.update()