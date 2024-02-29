# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import *
from datetime import date
import logging

_logger = logging.getLogger(__name__)

class usuario(models.Model):
    _name = 'musictracker.usuario'
    _description = 'Permite definir los datos de un usuario y sus ratings'

    name = fields.Char('Username',required=True,help='Introduce el nombre de usuario')
    nombre = fields.Text(string='Nombre')
    apellidos = fields.Text(string='Apellidos')
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento',default=fields.date.today())
    ubicacion = fields.Text(string='Ubicación',help='Selecciona el lugar de procedencia')
    foto = fields.Binary()
    biografia = fields.Text('Biografía',help='Introduce información biográfica del usuario')
    correo = fields.Text(string='E-mail')
    # relaciones
    ratings = fields.One2many('musictracker.rating','usuario',string='Ratings')

    # restricciones
    _sql_constraints=[('name_unique','unique(name)','El nombre de usuario ya existe')]    

    def enviar_correo(self):
        mail_mail = self.env['mail.mail']
        correo = self.correo
        asunto = "Envío de correo MusicTracker"
        cuerpo = """
                    <h1>Buenos días</h1>

                    <p>Desde MusicTracker, queremos agradecer tu colaboración estableciando valoraciones de tus álbumes favoritos</p>

                    <p>Un cordial saludo,
                    <b>MusicTracker</b></p>
                """
        mail_id = mail_mail.create({
            'email_to': correo,
            'subject': asunto,
            'body_html': '<pre>%s</pre>' % cuerpo, 
        })
        mail_mail.send([mail_id])


class rating(models.Model):
    _name = 'musictracker.rating'
    _description = 'Relaciona el usuario que ha hecho un rating con la publicación valorada'

    # name recibirá un valor calculado del estilo Username - Rating1 autoincrementado
    name = fields.Char('Número de rating',compute='_compute_rating_name',store=True)
    # el rating tendrá valores de media estrella a media estrella, y usará un widget
    rating = fields.Selection(string='Rating',help='Valoración asignada a la publicación, de 1 a 10 estrellas',selection=[('0','Sin rating'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10')],default='0')
    review = fields.Text(string='Review')
    fecha_rating = fields.Date(string='Fecha del rating',default=fields.date.today())
    # relaciones
    usuario = fields.Many2one('musictracker.usuario',string='Usuario',required=True,help='Selecciona el usuario que asigna el rating',ondelete="cascade")
    publicacion = fields.Many2one('musictracker.publicacion',string='Publicación',required=True,help='Selecciona la publicación que se valora',ondelete="cascade")

    @api.depends('usuario', 'usuario.ratings')
    def _compute_rating_name(self):
        for rating in self:
            ratings_usuario = self.env['musictracker.rating'].search([('usuario', '=', rating.usuario.id)])
            numero_ratings = len(ratings_usuario) + 1
            rating.name = f"{rating.usuario.name} - Rating{numero_ratings}"


class publicacion(models.Model):
    _name = 'musictracker.publicacion'
    _description = 'Permite añadir publicaciones de cualquier tipo para un determinado artista'

    name = fields.Char('Nombre',required=True,help='Introduce el nombre de la publicación')
    fecha_publicacion = fields.Date(string='Fecha de publicación',default=fields.date.today())
    #campo para buscar el año de publicación
    ano_publicacion = fields.Char('Año de publicación',compute='_compute_ano_publicacion',store=True)
    tipo = fields.Selection(string='Tipo',selection=[('a','Álbum'),('c','Compilación'),('e','EP / Mini-álbum'),('s','Single'),('m','Mixtape'),('d','DJ Mix'),('b','Bootleg / No autorizado'),('r','Álbum remix')],default='a')
    foto = fields.Binary()
    url_spotify = fields.Char(string='Código embed Spotify')
    #el rating recibirá el valor medio de todos los ratings de la publicación
    rating = fields.Float(string='Rating',compute='_compute_media_rating',store=True)
    # relaciones
    artista = fields.Many2one('musictracker.artista',string='Artista',required=True,help='Selecciona el artista de esta producción musical',ondelete="cascade")
    generos = fields.Many2many('musictracker.genero',string='Géneros',ondelete="cascade")
    tags = fields.Many2many('musictracker.tag',string='Tags',ondelete="cascade")
    canciones = fields.One2many('musictracker.cancion','publicacion',string='Canciones')
    #duracion_total (a desarrollar, relación con canción)
    #relación para ayudar a la hora de establecer la media del rating
    ratings = fields.One2many('musictracker.rating','publicacion',string='Ratings')

    @api.depends('ratings.rating')
    def _compute_media_rating(self):
        for publicacion in self:
            total_rating = sum(float(rating.rating) for rating in publicacion.ratings)
            if publicacion.ratings:
                publicacion.rating = total_rating / len(publicacion.ratings)
            else:
                publicacion.rating = 0.0

    @api.depends('fecha_publicacion')
    def _compute_ano_publicacion(self):
        for publicacion in self:
            publicacion.ano_publicacion = publicacion.fecha_publicacion.year if publicacion.fecha_publicacion else False

    # override del método name_get para mostrar artista - publicacion
    def name_get(self):
        nombre_final = []
        for publicacion in self:
            nombre_completo = f"{publicacion.artista.name} - {publicacion.name}"
            nombre_final.append((publicacion.id, nombre_completo))
        return nombre_final

    # restricciones
    # la fecha de publicación no puede ser anterior a la fecha de formación del artista
    _sql_constraints = [
        ('check_fecha_publicacion', 'CHECK(fecha_publicacion >= artista.fecha_formacion)', 'La fecha de publicación no puede ser anterior a la fecha de formación del artista.'),
    ]

            
class artista(models.Model):
    _name = 'musictracker.artista'
    _description = 'Recoge todos los artistas y sus publicaciones'

    name = fields.Char('Nombre',required=True,help='Introduce el nombre del artista o grupo')
    fecha_formacion = fields.Date(string='Fecha de formación',default=fields.date.today())
    #campo para buscar el año de formación
    ano_formacion = fields.Char('Año de formación',compute='_compute_ano_formacion',store=True)
    fecha_separacion = fields.Date(string='Fecha de separación',default=fields.date.today())
    ubicacion = fields.Text(string='Ubicación',help='Selecciona el lugar de procedencia')
    foto = fields.Binary()
    # relaciones
    publicaciones = fields.One2many('musictracker.publicacion','artista',string='Publicaciones')
    generos = fields.Many2many('musictracker.genero',string='Géneros',ondelete="cascade")
    miembros = fields.One2many('musictracker.miembro','artista',string='Miembros')

    @api.depends('fecha_formacion')
    def _compute_ano_formacion(self):
        for artista in self:
            artista.ano_formacion = artista.fecha_formacion.year if artista.fecha_formacion else False
    
    # restricciones
    #comprueba que la fecha de separación no sea anterior a la fecha de formación
    @api.constrains('fecha_formacion','fecha_separacion')
    def _check_orden_fechas(self):
        for artista in self:
            if artista.fecha_separacion and artista.fecha_separacion < artista.fecha_formacion:
                raise ValidationError("La fecha de separación no puede ser anterior a la fecha de formación")


class miembro(models.Model):
    _name = 'musictracker.miembro'
    _description = 'Permite asignar miembros a un determinado artista e incluir el instrumento que usa'

    name = fields.Char('Nombre artístico',required=True,help='Introduce el nombre artístico del miembro')
    nombre = fields.Text(string='Nombre',help='Introduce el nombre real del miembro')
    apellidos = fields.Text(string='Apellidos')
    instrumento = fields.Text(string='Instrumento/s',help='Introduce el instrumento o instrumento que utiliza este miembro en su grupo')
    fecha_inicio = fields.Date(string='Fecha de inicio',default=fields.date.today(),help='Añade la fecha en la que el miembro empezó a formar parte del grupo')
    fecha_fin = fields.Date(string='Fecha final',default=fields.date.today(),help='Añade, si procede, la fecha en la que el miembro se separó del grupo')
    # relaciones
    artista = fields.Many2one('musictracker.artista',string='Artista',required=True,help='Selecciona el artista al que pertenece este miembro',ondelete="cascade")

    # restricciones
    #comprueba que la fecha de separación no sea anterior a la fecha de inicio
    @api.constrains('fecha_inicio','fecha_fin')
    def _check_orden_fechas(self):
        for miembro in self:
            if miembro.fecha_fin and miembro.fecha_fin < miembro.fecha_inicio:
                raise ValidationError("La fecha de separación no puede ser anterior a la fecha de inicio")


class cancion(models.Model):
    _name = 'musictracker.cancion'
    _description = 'Almacena toda canción que pueda formar parte de una publicación'

    name = fields.Char('Nombre',required=True,help='Introduce el nombre de la canción')
    artista = fields.Char('Artista',compute='_compute_artista',store=True)
    #duracion (a desarrollar)
    # relaciones
    publicacion = fields.Many2one('musictracker.publicacion',required=True,string='Publicación',ondelete="cascade")

    #el campo artista se recibe al introducir la publicación a la que pertence la canción
    @api.depends('publicacion.artista')
    def _compute_artista(self):
        for cancion in self:
            cancion.artista = cancion.publicacion.artista.name



class genero(models.Model):
    _name = 'musictracker.genero'
    _description = 'Almacena de forma simple todo tipo de géneros'

    name = fields.Char('Nombre',required=True,help='Introduce el nombre del género')

    # restricciones
    _sql_constraints=[('name_unique','unique(name)','Este género ya está almacenado')]


class tag(models.Model):
    _name = 'musictracker.tag'
    _description = 'Almacena de forma simple todo tipo de etiquetas para publicaciones'

    name = fields.Char('Nombre',required=True,help='Introduce el nombre de la etiqueta')

    # restricciones
    _sql_constraints=[('name_unique','unique(name)','Esta etiqueta ya está almacenada')]


