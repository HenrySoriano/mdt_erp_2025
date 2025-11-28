"""
Datos de provincias y ciudades de Ecuador para los formularios
"""

PROVINCIAS_ECUADOR = [
    ('Azuay', 'Azuay'),
    ('Bolívar', 'Bolívar'),
    ('Cañar', 'Cañar'),
    ('Carchi', 'Carchi'),
    ('Chimborazo', 'Chimborazo'),
    ('Cotopaxi', 'Cotopaxi'),
    ('El Oro', 'El Oro'),
    ('Esmeraldas', 'Esmeraldas'),
    ('Galápagos', 'Galápagos'),
    ('Guayas', 'Guayas'),
    ('Imbabura', 'Imbabura'),
    ('Loja', 'Loja'),
    ('Los Ríos', 'Los Ríos'),
    ('Manabí', 'Manabí'),
    ('Morona Santiago', 'Morona Santiago'),
    ('Napo', 'Napo'),
    ('Orellana', 'Orellana'),
    ('Pastaza', 'Pastaza'),
    ('Pichincha', 'Pichincha'),
    ('Santa Elena', 'Santa Elena'),
    ('Santo Domingo de los Tsáchilas', 'Santo Domingo de los Tsáchilas'),
    ('Sucumbíos', 'Sucumbíos'),
    ('Tungurahua', 'Tungurahua'),
    ('Zamora Chinchipe', 'Zamora Chinchipe'),
]

# Ciudades principales por provincia
CIUDADES_POR_PROVINCIA = {
    'Azuay': ['Cuenca', 'Gualaceo', 'Paute', 'Sigsig', 'Girón', 'San Fernando', 'Santa Isabel', 'Pucará', 'Chordeleg', 'Sevilla de Oro', 'Oña', 'El Pan', 'Nabón'],
    'Bolívar': ['Guaranda', 'Chillanes', 'Chimbo', 'Echeandía', 'Las Naves', 'San Miguel', 'Caluma', 'Salinas'],
    'Cañar': ['Azogues', 'Biblián', 'Cañar', 'La Troncal', 'El Tambo', 'Déleg', 'Suscal'],
    'Carchi': ['Tulcán', 'Bolívar', 'Espejo', 'Mira', 'Montúfar', 'San Pedro de Huaca'],
    'Chimborazo': ['Riobamba', 'Alausí', 'Chambo', 'Chunchi', 'Colta', 'Cumandá', 'Guamote', 'Guano', 'Pallatanga', 'Penipe'],
    'Cotopaxi': ['Latacunga', 'La Maná', 'Pangua', 'Pujilí', 'Salcedo', 'Saquisilí', 'Sigchos'],
    'El Oro': ['Machala', 'Arenillas', 'Atahualpa', 'Balsas', 'Chilla', 'El Guabo', 'Huaquillas', 'Las Lajas', 'Marcabelí', 'Pasaje', 'Piñas', 'Portovelo', 'Santa Rosa', 'Zaruma'],
    'Esmeraldas': ['Esmeraldas', 'Atacames', 'Eloy Alfaro', 'Muisne', 'Quinindé', 'Río Verde', 'San Lorenzo'],
    'Galápagos': ['Puerto Baquerizo Moreno', 'Puerto Ayora', 'Puerto Villamil'],
    'Guayas': ['Guayaquil', 'Daule', 'Durán', 'El Empalme', 'General Villamil', 'Milagro', 'Naranjal', 'Naranjito', 'Palestina', 'Pedro Carbo', 'Samborondón', 'Santa Lucía', 'Salitre', 'San Jacinto de Yaguachi', 'Playas', 'Simón Bolívar', 'Yaguachi'],
    'Imbabura': ['Ibarra', 'Antonio Ante', 'Cotacachi', 'Otavalo', 'Pimampiro', 'San Miguel de Urcuquí'],
    'Loja': ['Loja', 'Calvas', 'Catamayo', 'Celica', 'Chaguarpamba', 'Espíndola', 'Gonzanamá', 'Macará', 'Olmedo', 'Paltas', 'Pindal', 'Puyango', 'Quilanga', 'Saraguro', 'Sozoranga', 'Zapotillo'],
    'Los Ríos': ['Babahoyo', 'Baba', 'Buena Fe', 'Mocache', 'Montalvo', 'Palenque', 'Pueblo Viejo', 'Quevedo', 'Quinsaloma', 'Urdaneta', 'Valencia', 'Ventanas', 'Vínces'],
    'Manabí': ['Portoviejo', 'Bolívar', 'Chone', 'El Carmen', 'Flavio Alfaro', 'Jama', 'Jaramijó', 'Jipijapa', 'Junín', 'Manta', 'Montecristi', 'Olmedo', 'Paján', 'Pedernales', 'Pichincha', 'Puerto López', 'Rocafuerte', 'San Vicente', 'Santa Ana', 'Sucre', 'Tosagua', 'Veinticuatro de Mayo'],
    'Morona Santiago': ['Macas', 'Gualaquiza', 'Huamboya', 'Limón Indanza', 'Logroño', 'Pablo Sexto', 'Palora', 'San Juan Bosco', 'Santiago', 'Sucúa', 'Taisha', 'Tiwintza'],
    'Napo': ['Tena', 'Archidona', 'Carlos Julio Arosemena Tola', 'El Chaco', 'Quijos'],
    'Orellana': ['Francisco de Orellana', 'Aguarico', 'La Joya de los Sachas', 'Loreto'],
    'Pastaza': ['Puyo', 'Arajuno', 'Mera', 'Santa Clara'],
    'Pichincha': ['Quito', 'Cayambe', 'Mejía', 'Pedro Moncayo', 'Pedro Vicente Maldonado', 'Puerto Quito', 'Rumiñahui', 'San Miguel de los Bancos', 'Santo Domingo'],
    'Santa Elena': ['Santa Elena', 'La Libertad', 'Salinas'],
    'Santo Domingo de los Tsáchilas': ['Santo Domingo', 'La Concordia'],
    'Sucumbíos': ['Nueva Loja', 'Cascales', 'Cuyabeno', 'Gonzalo Pizarro', 'Lago Agrio', 'Putumayo', 'Shushufindi', 'Sucumbíos'],
    'Tungurahua': ['Ambato', 'Baños', 'Cevallos', 'Mocha', 'Patate', 'Pelileo', 'Píllaro', 'Quero', 'Tisaleo'],
    'Zamora Chinchipe': ['Zamora', 'Centinela del Cóndor', 'Chinchipe', 'El Pangui', 'Nangaritza', 'Palanda', 'Paquisha', 'Yacuambi', 'Yantzaza'],
}

def get_ciudades_por_provincia(provincia):
    """Retorna la lista de ciudades para una provincia dada"""
    return CIUDADES_POR_PROVINCIA.get(provincia, [])

def get_todas_las_ciudades():
    """Retorna todas las ciudades de todas las provincias"""
    todas = []
    for ciudades in CIUDADES_POR_PROVINCIA.values():
        todas.extend(ciudades)
    return sorted(set(todas))

