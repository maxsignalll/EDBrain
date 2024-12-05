create table ITEM
(
    I_ID    INTEGER     default '0' not null
        constraint I_PK_ARRAY
            primary key,
    I_IM_ID INTEGER     default NULL,
    I_NAME  VARCHAR(32) default NULL,
    I_PRICE FLOAT       default NULL,
    I_DATA  VARCHAR(64) default NULL
);

