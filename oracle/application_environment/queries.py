"""
queries
"""

def example_query(user_id):
    """Example about how to write a query.
    - dont use ; at the end of queries
    - f at begining of string means it is a template that
      gets any variable in current function with {} simbols
    - complete info about string manipulation https://realpython.com/python-string-formatting/
    - complete info about string methods https://www.w3schools.com/python/python_ref_string.asp
    - complete info about string manipulation https://www.pythonforbeginners.com/basics/string-manipulation-in-python
    """
    return f'select * from pujlab.USER WHERE id_user={user_id}'


def get_fecha_db():
    """
    Despliegue los datos que se visualizan cuando un usuario dado ingresa a la aplicación. Esto
    incluye
    - Información de su cuenta
    - Los últimos 3 mensajes que ha puesto (más recientes) y las 2 réplicas más recientes
    que cada uno de esos mensajes ha recibido. Todo esto en ord en cronológico,
    empezando por los más recientes.
    - Los 3 mensajes más recientes que han puesto 3 de los usuarios a los que sigue.
    Despliega los 3 primeros usuarios, en orden alfabético.
    """
    return 'select sysdate from dual'

def get_login_data(user_id):
    """
    Despliegue los datos que se visualizan cuando un usuario dado ingresa a la aplicación. Esto
    incluye
    - Información de su cuenta
    - Los últimos 3 mensajes que ha puesto (más recientes) y las 2 réplicas más recientes
    que cada uno de esos mensajes ha recibido. Todo esto en ord en cronológico,
    empezando por los más recientes.
    - Los 3 mensajes más recientes que han puesto 3 de los usuarios a los que sigue.
    Despliega los 3 primeros usuarios, en orden alfabético.
    """
    return ''


def get_a_followers_not_in_b(user_a_email, user_b_email):
    """
    b. Seleccione el id y nombre de usuario de los usuarios que siguen al usuario ‘huasen@dos.dk’,
    pero no siguen a ‘dowi@pokla.tt’
    Nota: Puede cambiar los nombres de los usuarios por otros que se adapten a sus datos
    """
    return ''


def get_user_info_from_good_email(user_email):
    """
    c. Seleccione los datos de los usuarios cuya dirección de correo está bien escrita. Se considera
    una dirección válida aquella que está constituida por dos partes: el nombre del usuario (antes
    de ‘@’), y el nombre de dominio (después de ‘@’). La parte del nombre del usuario es una
    cadena no vacía que puede incluir letras, digitos, y los signos punto (.), guión bajo (_),
    porcentaje (%),o guión (-). El dominio a su vez, consta de dos partes separadas por punto (.).
    La primera parte es una cadena no vacía que puede incluir letras, digitos, y los signos punto
    (.) y guión bajo (_). La segunda parte es una cadena que tiene entre 2 y 4 letras.
    Use la consulta anterior para seleccionar usuarios cuya dirección de correo no cumple con
    estas especificaciones.
    Nota: si esta usando los datos de prueba, agregue algunos usuarios que no cumplan la
    especifiación.
    """
    return ''


def list_users_3_years():
    """
    d. Liste, para los usuarios activos, el id y nombre de usuario, la cantidad tweets que el usuario
    ha puesto en los últimos 3 años, y el número promedio de réplicas que sus tweets han recibido
    en esos 3 años. Liste solamente aquellos usuarios que tienen un promedio de réplicas mayor
    a 3.TAL L ER ORACL E
    Nota: si esta usando los datos de prueba, agregue algunas r éplicas para lograr promedios
    mayor a 3, ya que en esos datos todos los mensajes tienen 3 réplicas.
    (Sugerencia: use subconsultas, WITH https://oracle-base.com/articles/misc/with-clause )
    """
    return ''


def get_city_rank_by_tweets():
    """
    e. Realice un ranking de las ciudades por el número de tweets que han producido los usuarios
    de esa ciudad.
    (Sugerencia: use la función RANK)
    """
    return ''


def folowers_tree(root_email):
    """
    f.
    Liste el árbol de seguidores del usuario ‘lubhiklo@geemupu.pm’. La raíz del árbol es el
    usuario ‘lubhiklo@geemupu.pm’, en el siguiente nivel están los seguidores de
    ‘lubhiklo@geemupu.pm’, y en el siguiente nivel los seguidores de los anteriores. Liste el árbol
    hasta los seguidores de nivel 5.
    (Sugerencia: consulta recursiva o jerárquica
    https://oracle-base.com/articles/11g/recursive-subquery-factoring-11gr2
    https://docs.oracle.com/cd/B28359_01/server.111/b28286/queries003.htm#SQLRF52315 )
    Nota: Puede cambiar el nombre del usuario raíz por otro que se adapte a sus datos
    """
    return ''
