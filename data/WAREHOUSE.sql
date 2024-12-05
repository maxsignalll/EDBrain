create table WAREHOUSE
(
    W_ID       SMALLINT    default '0' not null
        constraint W_PK_ARRAY
            primary key,
    W_NAME     VARCHAR(16) default NULL,
    W_STREET_1 VARCHAR(32) default NULL,
    W_STREET_2 VARCHAR(32) default NULL,
    W_CITY     VARCHAR(32) default NULL,
    W_STATE    VARCHAR(2)  default NULL,
    W_ZIP      VARCHAR(9)  default NULL,
    W_TAX      FLOAT       default NULL,
    W_YTD      FLOAT       default NULL
);

