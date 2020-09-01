CREATE USER pujlab
  IDENTIFIED BY "Pujlab123!"
  DEFAULT TABLESPACE USERS
  temporary tablespace temp
  quota unlimited on users;

GRANT create session TO pujlab;
GRANT create table TO pujlab;
GRANT create view TO pujlab;
GRANT create any trigger TO pujlab;
GRANT create any procedure TO pujlab;
GRANT create sequence TO pujlab;
GRANT create synonym TO pujlab;