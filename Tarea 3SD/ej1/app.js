const express = require('express');
const { Pool } = require('pg');

const app = express();
const port = 3000;

// Configuración de la conexión a la base de datos
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'postgres',
  password: 'root',
  port: 5432,
});

// Middleware para manejar solicitudes JSON
app.use(express.json());

// Ruta POST para realizar la búsqueda
app.post('/buscar', async (req, res) => {
  const palabra = req.body.palabra; // Se espera que se pase la palabra en el cuerpo de la solicitud POST

  try {
    // Consulta para obtener los 5 documentos con mayor frecuencia para la palabra dada
    const consulta = `
      SELECT palabra, id_doc, frecuencia, url
      FROM palabras
      JOIN documentos ON palabras.id_doc = documentos.id
      WHERE palabra = $1
      ORDER BY frecuencia DESC
      LIMIT 5;
    `;
    //const consulta= `SELECT * FROM palabras WHERE palabra = '$1';
    //`

    const resultados = await pool.query(consulta, [palabra]);

    res.json(resultados.rows);
  } catch (error) {
    console.error('Error al realizar la búsqueda:', error);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
});

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
});
