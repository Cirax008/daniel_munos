import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class ClinicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Pacientes - Clínica SaludTotal")
        self.root.geometry("700x600")

        # Conectar a la base de datos MySQL
        self.conn = mysql.connector.connect(
          host="localhost",
            user="root",      # Reemplaza con tu usuario de MySQL
            password="root",  # Reemplaza con tu contraseña de MySQL
            database="videojuegos_db",
            allow_local_infile=True,
            use_pure=True   
        )
        self.cursor = self.conn.cursor()

        # Encabezado de la aplicación
        self.header_label = ttk.Label(root, text="Gestión de Información de Pacientes", font=("Arial", 16))
        self.header_label.pack(pady=10)

        # Frame para el formulario de entrada de datos
        self.form_frame = ttk.Frame(root)
        self.form_frame.pack(pady=10)

        # Campos de entrada de información del paciente
        self.name_label = ttk.Label(self.form_frame, text="Nombre:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(self.form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.age_label = ttk.Label(self.form_frame, text="Edad:")
        self.age_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.age_entry = ttk.Entry(self.form_frame, width=30)
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)

        self.gender_label = ttk.Label(self.form_frame, text="Género:")
        self.gender_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.gender_entry = ttk.Entry(self.form_frame, width=30)
        self.gender_entry.grid(row=2, column=1, padx=5, pady=5)

        self.history_label = ttk.Label(self.form_frame, text="Historial Médico:")
        self.history_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.history_entry = tk.Text(self.form_frame, width=30, height=5)
        self.history_entry.grid(row=3, column=1, padx=5, pady=5)

        # Botones
        self.add_button = ttk.Button(self.form_frame, text="Agregar Paciente", command=self.add_patient)
        self.add_button.grid(row=4, column=0, pady=10)

        self.update_button = ttk.Button(self.form_frame, text="Actualizar Paciente", command=self.update_patient)
        self.update_button.grid(row=4, column=1, pady=10)

        # Tabla para mostrar los pacientes registrados
        self.patient_table = ttk.Treeview(root, columns=("Nombre", "Edad", "Género"), show="headings", selectmode="browse")
        self.patient_table.heading("Nombre", text="Nombre")
        self.patient_table.heading("Edad", text="Edad")
        self.patient_table.heading("Género", text="Género")
        self.patient_table.pack(pady=20, fill=tk.BOTH, expand=True)

        # Vincula la selección de la tabla al método para cargar datos
        self.patient_table.bind("<<TreeviewSelect>>", self.load_patient_data)

        # Cargar los datos de los pacientes desde la base de datos al iniciar
        self.load_patients_from_db()

    def add_patient(self):
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        gender = self.gender_entry.get().strip()
        history = self.history_entry.get("1.0", tk.END).strip()

        if name and age and gender and history:
            # Insertar paciente en la base de datos
            query = "INSERT INTO pacientes (nombre, edad, genero, historial_medico) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (name, age, gender, history))
            self.conn.commit()

            # Recargar la tabla
            self.load_patients_from_db()
            self.clear_entries()
            messagebox.showinfo("Información", "Paciente agregado exitosamente.")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos")

    def update_patient(self):
        selected_item = self.patient_table.selection()
        if selected_item:
            # Obtener el ID del paciente seleccionado
            item = self.patient_table.item(selected_item)
            patient_id = item["values"][0]

            # Actualizar datos del paciente en la base de datos
            name = self.name_entry.get().strip()
            age = self.age_entry.get().strip()
            gender = self.gender_entry.get().strip()
            history = self.history_entry.get("1.0", tk.END).strip()

            query = """
            UPDATE pacientes
            SET nombre = %s, edad = %s, genero = %s, historial_medico = %s
            WHERE id = %s
            """
            self.cursor.execute(query, (name, age, gender, history, patient_id))
            self.conn.commit()

            # Recargar la tabla
            self.load_patients_from_db()
            self.clear_entries()
            messagebox.showinfo("Actualización", "Paciente actualizado exitosamente.")
        else:
            messagebox.showwarning("Advertencia", "Selecciona un paciente para actualizar")

    def load_patient_data(self, event):
        selected_item = self.patient_table.selection()
        if selected_item:
            item = self.patient_table.item(selected_item)
            patient_id = item["values"][0]

            # Cargar datos desde la base de datos
            query = "SELECT nombre, edad, genero, historial_medico FROM pacientes WHERE id = %s"
            self.cursor.execute(query, (patient_id,))
            result = self.cursor.fetchone()

            if result:
                name, age, gender, history = result

                # Cargar datos en los campos de entrada
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, name)

                self.age_entry.delete(0, tk.END)
                self.age_entry.insert(0, age)

                self.gender_entry.delete(0, tk.END)
                self.gender_entry.insert(0, gender)

                self.history_entry.delete("1.0", tk.END)
                self.history_entry.insert("1.0", history)

    def load_patients_from_db(self):
        # Limpiar la tabla antes de recargarla
        for item in self.patient_table.get_children():
            self.patient_table.delete(item)

        # Cargar pacientes de la base de datos
        query = "SELECT id, nombre, edad, genero FROM pacientes"
        self.cursor.execute(query)
        patients = self.cursor.fetchall()

        for patient in patients:
            self.patient_table.insert("", tk.END, values=patient)

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_entry.delete(0, tk.END)
        self.history_entry.delete("1.0", tk.END)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicApp(root)
    root.mainloop()
