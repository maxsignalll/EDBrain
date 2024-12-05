create table NEW_ORDER
(
    NO_O_ID INTEGER  default '0' not null,
    NO_D_ID TINYINT  default '0' not null,
    NO_W_ID SMALLINT default '0' not null,
    constraint NO_PK_TREE
        primary key (NO_D_ID, NO_W_ID, NO_O_ID),
    constraint NO_FKEY_O
        foreign key (NO_O_ID, NO_D_ID, NO_W_ID) references ORDERS (O_ID, O_D_ID, O_W_ID)
);

