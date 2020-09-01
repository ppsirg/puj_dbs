-- Generated by Oracle SQL Developer Data Modeler 17.4.0.355.2121
--   at:        2020-08-31 23:16:11 COT
--   site:      Oracle Database 11g
--   type:      Oracle Database 11g



CREATE TABLE pujlab.city (
    id_city               NUMBER NOT NULL,
    country_cod_country   VARCHAR2(3) NOT NULL,
    name_city             VARCHAR2(100)
);

COMMENT ON COLUMN pujlab.city.id_city IS
    'LLAVE PRIMARIA DE LA TABLA CIUDADES';

COMMENT ON COLUMN pujlab.city.name_city IS
    'NOMBRE DE LA CIUDAD';

ALTER TABLE pujlab.city ADD CONSTRAINT city_pk PRIMARY KEY ( id_city );

CREATE TABLE pujlab.country (
    cod_country    VARCHAR2(3) NOT NULL,
    name_country   VARCHAR2(100)
);

COMMENT ON COLUMN pujlab.country.cod_country IS
    'LLAVE PRIMARIA DE LA TABLA PAIS CODIGO ISO 3 DIGITOS';

ALTER TABLE pujlab.country ADD CONSTRAINT country_pk PRIMARY KEY ( cod_country );

CREATE TABLE pujlab.message (
    message_id          NUMBER NOT NULL,
    content             VARCHAR2(140),
    message_owner_id    NUMBER NOT NULL,
    reply_to_id         NUMBER,
    shared_message_id   NUMBER
);

ALTER TABLE pujlab.message ADD CONSTRAINT message_pk PRIMARY KEY ( message_id );

CREATE TABLE pujlab." SOCIAL_NETWORK" (
    user_id           NUMBER NOT NULL,
    user_id_related   NUMBER NOT NULL,
    relation_type     VARCHAR2(9) NOT NULL
);

ALTER TABLE pujlab." SOCIAL_NETWORK"
    ADD CHECK ( relation_type IN (
        'FOLLOWER',
        'FOLLOWING'
    ) );

COMMENT ON COLUMN pujlab." SOCIAL_NETWORK".relation_type IS
    'TIPO DE RELACION, SI SIGUE A LA PERSONA O ES SEGUIDO';

CREATE TABLE pujlab.topic_hashtag (
    topic_content        VARCHAR2(140) NOT NULL,
    message_message_id   NUMBER NOT NULL
);

CREATE TABLE pujlab."USER" (
    id_user          NUMBER NOT NULL,
    city_id_city     NUMBER NOT NULL,
    email            VARCHAR2(100),
    mobile           NUMBER(10),
    mobile_prefix    NUMBER(3),
    passwd           VARCHAR2(1000) NOT NULL,
    public_profile   CHAR(1) NOT NULL,
    user_name        VARCHAR2(50)
);

COMMENT ON COLUMN pujlab."USER".id_user IS
    'Llave primaria de la tabla de usuarios';

COMMENT ON COLUMN pujlab."USER".email IS
    'CORREO ELECTRONICO DEL USUARIO';

COMMENT ON COLUMN pujlab."USER".mobile IS
    'NUMERO DE TELEFONO MOVIL DEL USUARIO';

COMMENT ON COLUMN pujlab."USER".mobile_prefix IS
    'CODIGO ISO PARA PAISES DE 3 DIGITOS';

COMMENT ON COLUMN pujlab."USER".passwd IS
    'CONTRASEŅA DEL USUARIO';

COMMENT ON COLUMN pujlab."USER".public_profile IS
    'PROPIEDAD QUE DEFINE SI EL USUARIO ES DE PERFIL PUBLICO O PRIVADO 1= PUBLICO, 0 = PRIVADO';

COMMENT ON COLUMN pujlab."USER".user_name IS
    'NOMBRE DEL USUARIO PARA MOSTRAR';

ALTER TABLE pujlab."USER"
    ADD CONSTRAINT user_ck_username CHECK (
        email IS NOT NULL
        OR (
            mobile IS NOT NULL
            AND mobile_prefix IS NOT NULL
        )
    );

ALTER TABLE pujlab."USER" ADD CONSTRAINT user_pk PRIMARY KEY ( id_user );

ALTER TABLE pujlab.city
    ADD CONSTRAINT city_country_fk FOREIGN KEY ( country_cod_country )
        REFERENCES pujlab.country ( cod_country );

ALTER TABLE pujlab.message
    ADD CONSTRAINT message_message_fk FOREIGN KEY ( reply_to_id )
        REFERENCES pujlab.message ( message_id );

ALTER TABLE pujlab.message
    ADD CONSTRAINT message_message_fkv2 FOREIGN KEY ( shared_message_id )
        REFERENCES pujlab.message ( message_id );

ALTER TABLE pujlab.message
    ADD CONSTRAINT message_user_fk FOREIGN KEY ( message_owner_id )
        REFERENCES pujlab."USER" ( id_user );

ALTER TABLE pujlab." SOCIAL_NETWORK"
    ADD CONSTRAINT " SOCIAL_NETWORK_USER_FK1" FOREIGN KEY ( user_id )
        REFERENCES pujlab."USER" ( id_user );

ALTER TABLE pujlab." SOCIAL_NETWORK"
    ADD CONSTRAINT " SOCIAL_NETWORK_USER_FK2" FOREIGN KEY ( user_id_related )
        REFERENCES pujlab."USER" ( id_user );

ALTER TABLE pujlab.topic_hashtag
    ADD CONSTRAINT topic_hashtag_message_fk FOREIGN KEY ( message_message_id )
        REFERENCES pujlab.message ( message_id );

ALTER TABLE pujlab."USER"
    ADD CONSTRAINT user_city_fk FOREIGN KEY ( city_id_city )
        REFERENCES pujlab.city ( id_city );



-- Oracle SQL Developer Data Modeler Summary Report: 
-- 
-- CREATE TABLE                             6
-- CREATE INDEX                             0
-- ALTER TABLE                             14
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
