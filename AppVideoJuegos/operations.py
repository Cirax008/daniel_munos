import mysql.connector  # type: ignore

class VideoGameDatabase:
    def __init__(self):
        # Conexión a la base de datos MySQL
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",      # Reemplaza con tu usuario de MySQL
            password="root",  # Reemplaza con tu contraseña de MySQL
            database="videojuegos_db",
            allow_local_infile=True,
            use_pure=True   
        )
        self.cursor = self.conn.cursor()

    # ejecuta un insert en la base de datos
    def add_game(self, title, genre, rating, platform):
        query = "INSERT INTO Videojuegos (Titulo, Genero, Clasificacion, Plataforma) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (title, genre, rating, platform))
        self.conn.commit()
        return f"Videojuego '{title}' agregado exitosamente."

    #Ejecuta un select en la base de datos
    def get_all_games(self):
        query = "SELECT Titulo, Genero, Clasificacion, Plataforma FROM Videojuegos"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    #ejecuta un delete en la base de datos
    def delete_game(self, title):
        query = "DELETE FROM Videojuegos WHERE Titulo = %s"
        self.cursor.execute(query, (title,))
        self.conn.commit()
        return f"Videojuego '{title}' eliminado exitosamente."
    #actualiza un juego ne la base de datos
    def update_game(self, old_title, new_title, genre, rating, platform):
        query = """
        UPDATE Videojuegos 
        SET Titulo = %s, Genero = %s, Clasificacion = %s, Plataforma = %s
        WHERE Titulo = %s
        """
        self.cursor.execute(query, (new_title, genre, rating, platform, old_title))
        self.conn.commit()
        return f"Videojuego '{old_title}' actualizado a '{new_title}'."

    def __del__(self):
        self.cursor.close()
        self.conn.close()
