from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Inicializamos el motor 3D
app = Ursina(title="G-Creativa 3D Voxel Studio")

# Ocultamos el contador de FPS y el botón de salida predeterminado para una interfaz más limpia
window.fps_counter.enabled = False
window.exit_button.visible = False

# Variables globales para la interfaz
color_actual = color.white

class Voxel(Button):
    def __init__(self, position=(0,0,0), color_cubo=color.white):
        """
        Cada bloque en el espacio 3D es un 'Voxel'.
        Hereda de 'Button' para que el motor calcule automáticamente las colisiones
        y los eventos del ratón (raycasting) sobre su geometría.
        """
        super().__init__(
            parent=scene,
            position=position,
            model='cube',            # Geometría del modelo 3D
            origin_y=0.5,            # Ajuste del punto de pivote al centro del cubo
            texture='white_cube',    # Textura base optimizada del motor
            color=color_cubo,        # Color aplicado sobre la textura
            highlight_color=color.lime, # Color al pasar el cursor (Hover)
            collider='box'           # Física de colisión fundamental para construir
        )

    def input(self, key):
        """
        Manejo de eventos vectoriales. 
        'mouse.normal' es un vector 3D perpendicular a la cara del cubo que estamos mirando.
        """
        if self.hovered:
            # Construir: Sumamos la posición actual + el vector normal para colocarlo exactamente al lado
            if key == 'left mouse down':
                nuevo_voxel = Voxel(position=self.position + mouse.normal, color_cubo=color_actual)
            
            # Destruir: Eliminamos la instancia de la memoria y la escena
            if key == 'right mouse down':
                destroy(self)

# ==========================================
# Generación de la Base (Plano Cartesiano)
# ==========================================
# Creamos un plano de 16x16 cubos en los ejes X y Z (Y es la altura)
for z in range(16):
    for x in range(16):
        voxel = Voxel(position=(x, 0, z), color_cubo=color.dark_gray)

# ==========================================
# Controles de UI e Input General
# ==========================================
def update():
    """
    Bucle de actualización del motor gráfico (se ejecuta cada frame).
    Detecta el cambio de colores usando los números del teclado.
    """
    global color_actual
    
    # Paleta de colores estilo Cyberpunk / Sci-Fi
    if held_keys['1']: color_actual = color.white
    if held_keys['2']: color_actual = color.cyan
    if held_keys['3']: color_actual = color.magenta
    if held_keys['4']: color_actual = color.black
    if held_keys['5']: color_actual = color.orange

    # Salir del programa limpiamente
    if held_keys['escape']:
        application.quit()

# Interfaz en pantalla para guiar al usuario
Text(text='1:Blanco | 2:Cyan | 3:Magenta | 4:Negro | 5:Naranja', position=(-0.85, 0.45), scale=1.2, color=color.white)
Text(text='Click Izquierdo: Construir | Click Derecho: Destruir', position=(-0.85, 0.40), scale=1.2, color=color.cyan)

# Añadimos un controlador de cámara que nos permite movernos en el eje XYZ con las teclas WASD y el ratón
jugador = FirstPersonController()
# Ajustamos la altura de la cámara y la velocidad
jugador.y = 5 
jugador.speed = 8

# Ejecutamos el renderizado
app.run()