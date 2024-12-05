create table CUSTOMER
(
    C_ID           INTEGER     default '0'               not null,
    C_D_ID         TINYINT     default '0'               not null,
    C_W_ID         SMALLINT    default '0'               not null,
    C_FIRST        VARCHAR(32) default NULL,
    C_MIDDLE       VARCHAR(2)  default NULL,
    C_LAST         VARCHAR(32) default NULL,
    C_STREET_1     VARCHAR(32) default NULL,
    C_STREET_2     VARCHAR(32) default NULL,
    C_CITY         VARCHAR(32) default NULL,
    C_STATE        VARCHAR(2)  default NULL,
    C_ZIP          VARCHAR(9)  default NULL,
    C_PHONE        VARCHAR(32) default NULL,
    C_SINCE        TIMESTAMP   default CURRENT_TIMESTAMP not null,
    C_CREDIT       VARCHAR(2)  default NULL,
    C_CREDIT_LIM   FLOAT       default NULL,
    C_DISCOUNT     FLOAT       default NULL,
    C_BALANCE      FLOAT       default NULL,
    C_YTD_PAYMENT  FLOAT       default NULL,
    C_PAYMENT_CNT  INTEGER     default NULL,
    C_DELIVERY_CNT INTEGER     default NULL,
    C_DATA         VARCHAR(500),
    primary key (C_W_ID, C_D_ID, C_ID),
    constraint C_FKEY_D
        foreign key (C_D_ID, C_W_ID) references DISTRICT (D_ID, D_W_ID)
);

