create table ORDERS
(
    O_ID         INTEGER   default '0'               not null,
    O_C_ID       INTEGER   default NULL,
    O_D_ID       TINYINT   default '0'               not null,
    O_W_ID       SMALLINT  default '0'               not null,
    O_ENTRY_D    TIMESTAMP default CURRENT_TIMESTAMP not null,
    O_CARRIER_ID INTEGER   default NULL,
    O_OL_CNT     INTEGER   default NULL,
    O_ALL_LOCAL  INTEGER   default NULL,
    constraint O_2FKEY_C
        foreign key (O_C_ID, O_D_ID, O_W_ID) references CUSTOMER (C_ID, C_D_ID, C_W_ID)
);

