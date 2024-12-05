create table DISTRICT
(
    D_ID        TINYINT     default '0' not null,
    D_W_ID      SMALLINT    default '0' not null
        references WAREHOUSE,
    D_NAME      VARCHAR(16) default NULL,
    D_STREET_1  VARCHAR(32) default NULL,
    D_STREET_2  VARCHAR(32) default NULL,
    D_CITY      VARCHAR(32) default NULL,
    D_STATE     VARCHAR(2)  default NULL,
    D_ZIP       VARCHAR(9)  default NULL,
    D_TAX       FLOAT       default NULL,
    D_YTD       FLOAT       default NULL,
    D_NEXT_O_ID INT         default NULL,
    primary key (D_W_ID, D_ID)
);

