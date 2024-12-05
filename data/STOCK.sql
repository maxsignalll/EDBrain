create table STOCK
(
    S_I_ID       INTEGER     default '0'  not null
        references ITEM,
    S_W_ID       SMALLINT    default '0 ' not null
        references WAREHOUSE,
    S_QUANTITY   INTEGER     default '0'  not null,
    S_DIST_01    VARCHAR(32) default NULL,
    S_DIST_02    VARCHAR(32) default NULL,
    S_DIST_03    VARCHAR(32) default NULL,
    S_DIST_04    VARCHAR(32) default NULL,
    S_DIST_05    VARCHAR(32) default NULL,
    S_DIST_06    VARCHAR(32) default NULL,
    S_DIST_07    VARCHAR(32) default NULL,
    S_DIST_08    VARCHAR(32) default NULL,
    S_DIST_09    VARCHAR(32) default NULL,
    S_DIST_10    VARCHAR(32) default NULL,
    S_YTD        INTEGER     default NULL,
    S_ORDER_CNT  INTEGER     default NULL,
    S_REMOTE_CNT INTEGER     default NULL,
    S_DATA       VARCHAR(64) default NULL,
    primary key (S_W_ID, S_I_ID)
);

