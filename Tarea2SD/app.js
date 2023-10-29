const express = require("express");
const { Kafka } = require('kafkajs')
const bodyParser = require("body-parser");
const { Pool, Client } = require('pg');
const nodemailer = require('nodemailer');

const connectionString = 'postgresql://root:root@postgres:5432/test';

var transport = nodemailer.createTransport({
    host: "sandbox.smtp.mailtrap.io",
    port: 2525,
    auth: {
      user: "0d167cd97ed558",
      pass: "2216c531315046"
    }
  });

// Crear una instancia de cliente
const client = new Client({
    connectionString: connectionString
  });
  
// Conectar al servidor PostgreSQL
client.connect();

const app = express();

app.use(express.json());
app.use(bodyParser.json());

const kafka = new Kafka({
    brokers: [process.env.kafkaHost]

});

function generarStringAleatorio() {
    const caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let resultado = '';
  
    for (let i = 0; i < 7; i++) {
      const indiceAleatorio = Math.floor(Math.random() * caracteres.length);
      resultado += caracteres.charAt(indiceAleatorio);
    }
  
    return resultado;
  }

const run=async()=>{
    const consumer=kafka.consumer({groupId:"t2"})
    await consumer.connect();
    await consumer.subscribe({topic:'inscripciones'});
    await consumer.run({
        eachMessage:async ({topic,partition,message})=>{
            const formData = JSON.parse(message.value.toString());
            console.log('El usuario dice: Hola mi nombre es ',formData.nombre,' quiero registrarme en el gremio aqui van mis datos...')
            // Guardar los datos en la base de datos
            const query = 'INSERT INTO users (nombre, email, rut) VALUES ($1, $2, $3)';
            const values = [formData.nombre, formData.email, formData.rut];

            const pass = generarStringAleatorio();

            client.query(query, values, (err) => {
                if (err) {
                console.error('Error al insertar en la base de datos:', err);
                } else {
                console.log('Usuario registrado correctamente, sus datos:', formData);
                }
            });

            const info = await transport.sendMail({
                from: '"MOMOCHI" <cuentas@momochi.com>',
                to: formData.email,
                subject: "MOMOCHI - Envio Credenciales",
                text: "Credenciales para ingresar a la plataforma",
                html: `<p>Estimado: ${formData.nombre} hemos recibido su solicitud para ser parte de MOMOCHI. Sus credenciales son las siguientes:
                    email: ${formData.email}
                    contraseña: ${pass}
                  </p>
                  
                  `,
              });        
        }
    })
    const consumer2=kafka.consumer({groupId:"t2_1"})
    await consumer2.connect();
    await consumer2.subscribe({topic:'sin-stock'});
    await consumer2.run({
        eachMessage:async ({topic,partition,message})=>{
            const formData = JSON.parse(message.value.toString());
            console.log('El usuario dice: ',formData.msj)
             // Guardar los datos en la base de datos
             const query = 'UPDATE carrito SET stock = 14 WHERE usuario_id = $1';
            // INSERT INTO users (nombre, email, rut) VALUES ($1, $2, $3);
             const values = [formData.id];
             client.query(query, values, (err) => {
                if (err) {
                console.error('Error al insertar en la base de datos:', err);
                } else {
                console.log('El stock del usuario ha sido renovado exitosamente');
                }
            });

        }
    })

    const consumer3=kafka.consumer({groupId:"t2_2"})
    await consumer3.connect();
    await consumer3.subscribe({topic:'ventas'});
    await consumer3.run({
        eachMessage:async ({topic,partition,message})=>{
            const formData = JSON.parse(message.value.toString());
            console.log('El usuario dice: ',formData.msj)
             // Guardar los datos en la base de datos
             const query = 'INSERT INTO ventas (ganancias, usuario_id, semana) VALUES ($1, $2, $3)';
           
             const values = [formData.ganancias,formData.id,formData.semana];

             const query2='UPDATE carrito SET stock = stock - $1 WHERE usuario_id=$2';
             const values2=[formData.cantidad,formData.id];

             client.query(query, values, (err) => {
                if (err) {
                console.error('Error al insertar en la base de datos:', err);
                } else {
                console.log('Venta registrada exitosamente');
                }

            });

            client.query(query2, values2, (err) => {
                if (err) {
                console.error('Error al insertar en la base de datos:', err);
                } else {
                console.log('Venta registrada exitosamente');
                }
                
            });

        }
    })

    const consumer4=kafka.consumer({groupId:"t2_3"})
    await consumer4.connect();
    await consumer4.subscribe({topic:'contabilidad'});
    await consumer4.run({
        eachMessage:async ({topic,partition,message})=>{
            let sumaDeGanancias=0;
            let numeroDeFilas=0;
            const formData = JSON.parse(message.value.toString());
            console.log('El usuario dice: ',formData.msj)
             // Guardar los datos en la base de datos
             const query = 'SELECT SUM(ganancias) AS suma_de_ganancias_semana FROM ventas WHERE semana = $1 AND usuario_id = $2';
             const query2 = 'SELECT COUNT(*) AS numero_de_filas_semana FROM ventas WHERE semana = $1 AND usuario_id = $2';
             const values = [formData.semana,formData.id];

             const executeQuery = async (query, values) => {
                try {
                  const result = await client.query(query, values);
                  return result.rows;
                } catch (error) {
                  throw error;
                }
              };

              async function processData() {
                try {
                  const result1 = await executeQuery(query, values);
                  sumaDeGanancias = result1[0].suma_de_ganancias_semana;
              
                  const result2 = await executeQuery(query2, values);
                  numeroDeFilas = result2[0].numero_de_filas_semana;

                  const info = await transport.sendMail({
                    from: '"Contabilidades MOMOCHI" <contabilidad@momochi.com>',
                    to: formData.email,
                    subject: `MOMOCHI - Envio Contabilidad Semana ${formData.semana}`,
                    text: "Estadisticas de sus ventas esta semana",
                    html: `<p>Numero de ventas realizadas semana ${formData.semana}: ${numeroDeFilas}. Ganancias en la semana ${formData.semana}: ${sumaDeGanancias}</p>
                      
                      `,
                  });
                  console.log('Datos enviados al correo')
                } catch (error) {
                  console.error('Error al interactuar con la base de datos:', error);
                }
              }
             processData();
            
        }
        
    })


}


const producer = kafka.producer();
app.post("/inscripciones", async (req, res) => {
    const formData = req.body;
    const paid=formData.paid

    await producer.connect();
    if(paid==true){
        const partition=1;
        await producer.send({
            topic:'inscripciones',
            messages: [
                {
                    key:'formulario',
                    value: JSON.stringify(formData)
                }
            ],
            partition
        });
    }
    else{
        const partition=2;
        await producer.send({
            topic:'inscripciones',
            messages: [
                {
                    key:'formulario',
                    value: JSON.stringify(formData)
                }
            ],
            partition
        });
    }

    await producer.disconnect();

    
});

app.post("/sin-stock",async(req,res)=>{
    const formData = req.body;
    await producer.connect();
    await producer.send({
        topic:'sin-stock',
        messages: [
            {
                key:'sin-stock',
                value: JSON.stringify(formData)
            }
        ],
    });
    await producer.disconnect();

})

app.post("/venta",async(req,res)=>{
    const formData = req.body;
    await producer.connect();
    await producer.send({
        topic:'ventas',
        messages: [
            {
                key:'venta',
                value: JSON.stringify(formData)
            }
        ],
    });
    await producer.disconnect();

})

app.post("/contabilidad",async(req,res)=>{
    const formData = req.body;
    await producer.connect();
    await producer.send({
        topic:'contabilidad',
        messages: [
            {
                key:'contabilidad',
                value: JSON.stringify(formData)
            }
        ],
    });
    console.log('Datos enviados',formData);
    await producer.disconnect();

})


app.listen(3000, () => {
    console.log(`Listening on port 3000`);
    run();
});