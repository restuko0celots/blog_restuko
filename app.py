from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "restuko_secret_key_y2k"

# Base de datos simulada en memoria
USUARIOS = {
    "restuko": {
        "husbando": "nombre personaje",
        "tipo_yume": "💕 Amor Eterno (Yume)",
        "fondo": "flowers.png",
        "gif": "minecraft-creeper.gif",
        "musica": "wii_channel.mp3"
    }
}

PUBLICACIONES = [
    {
        "autor": "restuko",
        "titulo": "¡Inauguración oficial de Yumeship Rincón Secret!",
        "fecha": "13 de Septiembre, 2026",
        "contenido": "bienvenido a el espacio para tu yumeship o simplemente tu personaje favorito",
        "categoria": "🔮 Update"
    }
]

# Listas de opciones reales que tienes en tus carpetas
OPCIONES_RECURSOS = {
    "fondos": [
        {"archivo": "creeper.png", "nombre": "Bloques Creeper"},
        {"archivo": "flowers.png", "nombre": "Encaje Gótico Flores"},
        {"archivo": "y2l.png", "nombre": "Notas Musicales Y2K"},
        {"archivo": "osito.png", "nombre": "Osito Soft Emo"}
    ],
    "gifs": [
        {"archivo": "cat-space.gif", "nombre": "Nyan Cat Espacial"},
        {"archivo": "dancing-cat.gif", "nombre": "Gato Bailarín"},
        {"archivo": "miku-pusheen.gif", "nombre": "Miku Pusheen Laptop"},
        {"archivo": "minecraft-creeper.gif", "nombre": "Creeper Pixelado"}
    ],
    "musicas": [
        {"archivo": "nyan_cat.mp3", "nombre": "Nyan Cat Theme"},
        {"archivo": "wii_channel.mp3", "nombre": "Wii Channel Mii"}
    ]
}

@app.route('/')
def home():
    usuario_activo = session.get('usuario_actual', 'restuko')
    config_actual = USUARIOS.get(usuario_activo, USUARIOS['restuko'])
    
    return render_template('index.html', 
                           posts=PUBLICACIONES, 
                           usuarios=USUARIOS, 
                           opciones=OPCIONES_RECURSOS,
                           config=config_actual,
                           actual=usuario_activo)

@app.route('/registrar', methods=['POST'])
def registrar():
    username = request.form.get('username')
    husbando = request.form.get('husbando')
    tipo_yume = request.form.get('tipo_yume')
    fondo = request.form.get('fondo')
    gif = request.form.get('gif')
    musica = request.form.get('musica')

    if username in USUARIOS:
        flash("¡Ese nickname ya está registrado!")
    elif username:
        USUARIOS[username] = {
            "husbando": husbando if husbando else "Desconocido",
            "tipo_yume": tipo_yume if tipo_yume else "Casual Lover",
            "fondo": fondo,
            "gif": gif,
            "musica": musica
        }
        session['usuario_actual'] = username
        flash(f"¡Usuario {username} creado! Estilo personalizado aplicado.")
    return redirect(url_for('home'))

@app.route('/cambiar-estilo', methods=['POST'])
def cambiar_estilo():
    usuario_activo = session.get('usuario_actual', 'restuko')
    if usuario_activo in USUARIOS:
        USUARIOS[usuario_activo]['fondo'] = request.form.get('fondo')
        USUARIOS[usuario_activo]['gif'] = request.form.get('gif')
        USUARIOS[usuario_activo]['musica'] = request.form.get('musica')
        flash("¡Configuración de estilo actualizada con éxito!")
    return redirect(url_for('home'))

@app.route('/seleccionar-usuario/<username>')
def seleccionar_usuario(username):
    if username in USUARIOS:
        session['usuario_actual'] = username
        flash(f"Viendo el blog con la estética de: {username}")
    return redirect(url_for('home'))

@app.route('/publicar', methods=['POST'])
def publicar():
    autor = request.form.get('autor')
    titulo = request.form.get('titulo')
    contenido = request.form.get('contenido')
    categoria = request.form.get('categoria')
    fecha_hoy = datetime.now().strftime("%d de %B, %Y")

    if autor and titulo and contenido:
        if autor not in USUARIOS:
            flash("Debes registrar tu usuario antes de publicar.")
            return redirect(url_for('home'))

        PUBLICACIONES.insert(0, {
            "autor": autor,
            "titulo": titulo,
            "fecha": fecha_hoy,
            "contenido": contenido,
            "categoria": categoria
        })
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
