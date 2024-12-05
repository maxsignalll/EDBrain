create table HISTORY
(
    H_C_ID   INTEGER     default NULL,
    H_C_D_ID TINYINT     default NULL,
    H_C_W_ID SMALLINT    default NULL,
    H_D_ID   TINYINT     default NULL,
    H_W_ID   SMALLINT    default '0'               not null,
    H_DATE   TIMESTAMP   default CURRENT_TIMESTAMP not null,
    H_AMOUNT FLOAT       default NULL,
    H_DATA   VARCHAR(32) default NULL,
    constraint H_FKEY_C
        foreign key (H_C_ID, H_C_D_ID, H_C_W_ID) references CUSTOMER (C_ID, C_D_ID, C_W_ID),
    constraint H_FKEY_D
        foreign key (H_D_ID, H_W_ID) references DISTRICT (D_ID, D_W_ID)
);

