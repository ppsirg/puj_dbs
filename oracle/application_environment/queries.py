"""
queries
"""

def example_query():
    """Example about how to write a query.
    - dont use ; at the end of queries
    - f at begining of string means it is a template that
      gets any variable in current function with {} simbols
    - complete info about string manipulation https://realpython.com/python-string-formatting/
    - complete info about string methods https://www.w3schools.com/python/python_ref_string.asp
    - complete info about string manipulation https://www.pythonforbeginners.com/basics/string-manipulation-in-python
    """
    return {
        'list_users': 'select * from PUJLAB."USER"'
    }


def get_login_data():
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
    last_messages = """select message_id 
    from (select * from message where message_owner_id = :message_owner_id ORDER BY message.created_date)
    WHERE ROWNUM < 4
    """
    recent_messages = """select * from (select * from message
    where 
    message.reply_to_id IN (select message_id from (select * from message where message_owner_id = :message_owner_id ORDER BY message.created_date) 
    WHERE ROWNUM < 4)
    ORDER BY message.created_date)
    where ROWNUM < 3
    """
    queries = {
        'user_info': 'select * from PUJLAB."USER" WHERE id_user=:id_user',
        'last_messages': last_messages,
        'recent_messages': recent_messages
    }
    return queries


def get_a_followers_not_in_b():
    """
    b. Seleccione el id y nombre de usuario de los usuarios que siguen al usuario ‘huasen@dos.dk’,
    pero no siguen a ‘dowi@pokla.tt’
    Nota: Puede cambiar los nombres de los usuarios por otros que se adapten a sus datos
    """
    diff_follows = """select user_name, id_user from PUJLAB."USER" where id_user in (select user_id from PUJLAB." SOCIAL_NETWORK"
    where not user_id_related={a} and relation_type = 'FOLLOWING' and user_id_related={b})
    """
    return {
        'diff_follows': diff_follows
    }


def get_user_info_from_good_email():
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
    email_detector = """SELECT id_user, email, user_name
    FROM PUJLAB."USER"
    WHERE email NOT LIKE '%_@%_._%'
    """
    return {
        'email_detector': email_detector
    }


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
    listing_3yr = """Select id_user, COUNT(m1.Contenido) cantidad_tweets, user_name, ROUND(AVG( m2.reply_to_id )) prom_replicas
    from PUJLAB."USER" inner join message m1 on (m1.message_owner_id = id_user and 
    m1.created_date > sysdate - interval '3' year ) inner join message m2 on (m1.message_id = m2.reply_to_id)  
    GROUP BY id_user, user_name
    """
    return {
        'listing_3yr': listing_3yr
    }


def get_city_rank_by_tweets():
    """
    e. Realice un ranking de las ciudades por el número de tweets que han producido los usuarios
    de esa ciudad.
    (Sugerencia: use la función RANK)
    """
    ranking = """SELECT city.name_city, PUJLAB."USER".city_id_city, message_owner_id,
    RANK() OVER (PARTITION BY name_city
    ORDER BY message_owner_id) "Rank"
    FROM city, PUJLAB."USER", message
    """
    return {
        'ranking': ranking
    }


def folowers_tree():
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
    tree = """SELECT user_id, user_id_related, relation_type, s0.user_name, level, s1.user_name 
    FROM PUJLAB." SOCIAL_NETWORK" n inner join PUJLAB."USER" s0 on (n.user_id = s0.id_user) 
    inner join PUJLAB."USER" s1 on (s1.id_user=n.user_id_related)
    START WITH s0.user_name = :user_name
    CONNECT BY PRIOR n.user_id= n.user_id_related AND LEVEL <= 5;
    """
    return {
        'tree': tree
    }
