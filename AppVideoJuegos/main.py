import tkinter as tk
from tkinter import ttk, messagebox
from operations import VideoGameDatabase

class VideoGameApp:

    # instancia la ventana
    def __init__(self, root):
        self.root = root
        # titulo de la  ventana
        self.root.title("Gestión de Videojuegos")
        # tamaño de la ventana
        self.root.geometry("600x500")

        
        # instancia de las funciones para la  base de datos
        self.db = VideoGameDatabase()


        # Labels y campos de entrada
        # texto del campo 
        self.title_label = ttk.Label(root, text="Título:")
        # posicion de titulo
        self.title_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        # instancia de caja de texto
        self.title_entry = ttk.Entry(root, width=40)
        # posicion de caja de texto
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        # texto del campo 
        self.genre_label = ttk.Label(root, text="Género:")
        # posicion de titulo
        self.genre_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        
        # instancia de caja de texto
        self.genre_entry = ttk.Entry(root, width=40)
         # posicion de caja de texto
        self.genre_entry.grid(row=1, column=1, padx=10, pady=5)

         # texto del campo 
        self.rating_label = ttk.Label(root, text="Clasificación:")
        # posicion de titulo
        self.rating_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        # instancia de caja de texto
        self.rating_entry = ttk.Entry(root, width=40)
         # posicion de caja de texto
        self.rating_entry.grid(row=2, column=1, padx=10, pady=5)

        # texto del campo 
        self.platform_label = ttk.Label(root, text="Plataforma:")
         # texto del campo 
        self.platform_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        # instancia de caja de texto
        self.platform_entry = ttk.Entry(root, width=40)
         # posicion de caja de texto
        self.platform_entry.grid(row=3, column=1, padx=10, pady=5)

        # Botones

        # instancia boton            Elemento principal, texto del boton, funcion del boton en ese orden    
        self.add_button = ttk.Button(root, text="Agregar Videojuego", command=self.add_game)
        #posicion del boton
        self.add_button.grid(row=4, column=0, columnspan=2, pady=5)

        # instancia boton            Elemento principal, texto del boton, funcion del boton en ese orden    
        self.delete_button = ttk.Button(root, text="Eliminar Videojuego", command=self.delete_game)
        #posicion del boton
        self.delete_button.grid(row=5, column=0, columnspan=2, pady=5)

        # instancia boton            Elemento principal, texto del boton, funcion del boton en ese orden    
        self.update_button = ttk.Button(root, text="Actualizar Videojuego", command=self.update_game)
        #posicion del boton
        self.update_button.grid(row=6, column=0, columnspan=2, pady=5)

        # Lista de videojuegos
        # caja donde se mostraran los video juegos de la base de datos
        self.game_list_label = ttk.Label(root, text="Lista de Videojuegos:")
        #posicion de los diferentes elementos
        self.game_list_label.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
        self.game_list = tk.Listbox(root, width=70, height=10)
        self.game_list.grid(row=8, column=0, columnspan=2, padx=10, pady=5)
        #carga un evento (<<ListboxSelect>>) que al seleccionar una linea de la caja de juegos , se muestre en los campos de texto para editar

        self.game_list.bind('<<ListboxSelect>>', self.load_game_to_update)
        #carga los juegos
        self.update_game_list()


    #metodo que agrega un  juego a la base de datos
    def add_game(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        rating = self.rating_entry.get().strip()
        platform = self.platform_entry.get().strip()

        if title and genre and rating and platform:
            message = self.db.add_game(title, genre, rating, platform)
            self.update_game_list()
            self.clear_entries()
            messagebox.showinfo("Información", message)
        else:
            messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos")


    #metodo que elimina un juego en la base de datos
    def delete_game(self):
        title = self.title_entry.get().strip()
        if title:
            message = self.db.delete_game(title)
            self.update_game_list()
            self.clear_entries()
            messagebox.showinfo("Información", message)
        else:
            messagebox.showwarning("Advertencia", "Debes ingresar el título del videojuego a eliminar")

    # metodo que actualiza un juego en la base de datos
    def update_game(self):
        old_title = self.selected_title
        new_title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        rating = self.rating_entry.get().strip()
        platform = self.platform_entry.get().strip()

        if old_title and new_title and genre and rating and platform:
            message = self.db.update_game(old_title, new_title, genre, rating, platform)
            self.update_game_list()
            self.clear_entries()
            messagebox.showinfo("Información", message)
        else:
            messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos para actualizar")
    #actualiza la lista de juegos
    def update_game_list(self):
        self.game_list.delete(0, tk.END)
        for game in self.db.get_all_games():
            game_info = f"Título: {game[0]}, Género: {game[1]}, Clasificación: {game[2]}, Plataforma: {game[3]}"
            self.game_list.insert(tk.END, game_info)
    
    #carga datos despues de actualizar un  juego
    def load_game_to_update(self, event):
        selected_index = self.game_list.curselection()
        if selected_index:
            selected_game = self.game_list.get(selected_index)
            title, genre, rating, platform = [info.split(": ")[1] for info in selected_game.split(", ")]
            self.selected_title = title  # Guarda el título original para la actualización
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, title)
            self.genre_entry.delete(0, tk.END)
            self.genre_entry.insert(0, genre)
            self.rating_entry.delete(0, tk.END)
            self.rating_entry.insert(0, rating)
            self.platform_entry.delete(0, tk.END)
            self.platform_entry.insert(0, platform)

    #metodo que limpia los campos de texto
    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
        self.platform_entry.delete(0, tk.END)
        self.selected_title = None

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoGameApp(root)
    root.mainloop()
