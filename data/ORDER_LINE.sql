create table ORDER_LINE
(
    OL_O_ID        INTEGER     default '0' not null,
    OL_D_ID        TINYINT     default '0' not null,
    OL_W_ID        SMALLINT    default '0' not null,
    OL_NUMBER      INTEGER     default '0' not null,
    OL_I_ID        INTEGER     default NULL,
    OL_SUPPLY_W_ID SMALLINT    default NULL,
    OL_DELIVERY_D  TIMESTAMP   default NULL,
    OL_QUANTITY    INTEGER     default NULL,
    OL_AMOUNT      FLOAT       default NULL,
    OL_DIST_INFO   VARCHAR(32) default NULL,
    primary key (OL_W_ID, OL_D_ID, OL_O_ID, OL_NUMBER),
    constraint OL_FKEY_O
        foreign key (OL_O_ID, OL_D_ID, OL_W_ID) references ORDERS (O_ID, O_D_ID, O_W_ID),
    constraint OL_FKEY_S
        foreign key (OL_I_ID, OL_SUPPLY_W_ID) references STOCK (S_I_ID, S_W_ID)
);

