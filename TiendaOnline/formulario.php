<form action="insert_producto.php" method="POST">
    <label>Nombre del producto:</label>
    <input type="text" name="nombre" required>
    
    <label>Descripción:</label>
    <textarea name="descripcion" required></textarea>

    <label>Precio:</label>
    <input type="number" name="precio" step="0.01" required>

    <label>Stock:</label>
    <input type="number" name="stock" required>

    <button type="submit">Guardar Producto</button>
</form>
