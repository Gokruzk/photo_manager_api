/*==============================================================*/
/* Table: dates                                                 */
/*==============================================================*/
create table dates (
   cod_date             INT4                 not null,
   "year"               INT4                 not null,
   "month"              INT4                 not null,
   "day"                DATE                 not null,
   constraint PK_DATES primary key (cod_date)
);

/*==============================================================*/
/* Index: dates_pk                                              */
/*==============================================================*/
create unique index dates_pk on dates (
cod_date
);

/*==============================================================*/
/* Table: images                                                */
/*==============================================================*/
create table images (
   cod_image            SERIAL               not null,
   cod_ubi              INT4                 not null,
   "image"              VARCHAR(300)         not null,
   uploadedat           Int                  not null,
   constraint PK_IMAGES primary key (cod_image)
);

/*==============================================================*/
/* Index: images_pk                                             */
/*==============================================================*/
create unique index images_pk on images (
cod_image
);

/*==============================================================*/
/* Index: images_ubication_fk                                   */
/*==============================================================*/
create  index images_ubication_fk on images (
cod_ubi
);

/*==============================================================*/
/* Index: images_dates_fk                                   */
/*==============================================================*/
create  index images_dates_fk on images (
uploadedat
);

/*==============================================================*/
/* Table: state                                                 */
/*==============================================================*/
create table state (
   cod_state            INT4                 not null,
   "state"              VARCHAR(8)           not null,
   constraint PK_STATE primary key (cod_state)
);

/*==============================================================*/
/* Index: state_pk                                              */
/*==============================================================*/
create unique index state_pk on state (
cod_state
);

/*==============================================================*/
/* Table: state                                                 */
/*==============================================================*/
create table descriptions (
   cod_description       INT4                 not null,
   "description"         VARCHAR(8)           not null,
   constraint PK_DESCR primary key (cod_description)
);

/*==============================================================*/
/* Index: state_pk                                              */
/*==============================================================*/
create unique index descriptions_pk on descriptions (
cod_description
);

/*==============================================================*/
/* Table: ubication                                             */
/*==============================================================*/
create table ubication (
   cod_ubi              INT4                 not null,
   country              VARCHAR(100)         null,
   constraint PK_UBICATION primary key (cod_ubi)
);

/*==============================================================*/
/* Index: ubication_pk                                          */
/*==============================================================*/
create unique index ubication_pk on ubication (
cod_ubi
);

/*==============================================================*/
/* Table: "user"                                                */
/*==============================================================*/
create table "user" (
   cod_user             SERIAL               not null,
   cod_ubi              INT4                 not null,
   cod_state            INT4                 not null,
   username             VARCHAR(15) UNIQUE   not null,
   email                VARCHAR(50)          not null,
   "password"           VARCHAR(300)         not null,
   constraint PK_USER primary key (cod_user)
);

/*==============================================================*/
/* Index: user_pk                                               */
/*==============================================================*/
create unique index user_pk on "user" (
cod_user
);

/*==============================================================*/
/* Index: user_ubication_fk                                     */
/*==============================================================*/
create  index user_ubication_fk on "user" (
cod_ubi
);

/*==============================================================*/
/* Table: user_dates                                            */
/*==============================================================*/
create table user_dates (
   cod_date             INT4                 not null,
   cod_user             INT4                 not null,
   cod_description      INT4                 not null,
   constraint PK_USER_DATES primary key (cod_date, cod_user, cod_description)
);

/*==============================================================*/
/* Index: user_dates_pk                                         */
/*==============================================================*/
create unique index user_dates_pk on user_dates (
cod_date,
cod_user,
cod_description
);

/*==============================================================*/
/* Index: user_dates_fk                                         */
/*==============================================================*/
create  index user_dates_fk on user_dates (
cod_user,
cod_description
);

/*==============================================================*/
/* Table: user_images                                           */
/*==============================================================*/
create table user_images (
   cod_image            INT4                 not null,
   cod_user             INT4                 not null,
   "description"        VARCHAR(11)          null,
   constraint PK_USER_IMAGES primary key (cod_image, cod_user)
);

/*==============================================================*/
/* Index: user_images_pk                                        */
/*==============================================================*/
create unique index user_images_pk on user_images (
cod_image,
cod_user
);

/*==============================================================*/
/* Index: user_images_fk                                        */
/*==============================================================*/
create  index user_images_fk on user_images (
cod_user
);

alter table images
   add constraint FK_IMAGES_IMAGES_UB_UBICATIO foreign key (cod_ubi)
      references ubication (cod_ubi)
      on delete restrict on update restrict;

alter table images
   add constraint FK_IMAGES_IMAGES_DATES foreign key (uploadedat)
      references dates (cod_date)
      on delete restrict on update restrict;

alter table "user"
   add constraint FK_USER_USER_UBIC_UBICATIO foreign key (cod_ubi)
      references ubication (cod_ubi)
      on delete restrict on update restrict;

alter table "user"
   add constraint FK_USER_USER_STA_STATE foreign key (cod_state)
      references "state" (cod_state)
      on delete restrict on update restrict;

alter table user_dates
   add constraint FK_USER_DAT_RELATIONS_USER foreign key (cod_user)
      references "user" (cod_user)
      on delete restrict on update restrict;

alter table user_dates
   add constraint FK_USER_DAT_RELATIONS_DATES foreign key (cod_date)
      references dates (cod_date)
      on delete restrict on update restrict;

alter table user_dates
   add constraint FK_USER_DAT_RELATIONS_DESCR foreign key (cod_description)
      references descriptions (cod_description)
      on delete restrict on update restrict;

alter table user_images
   add constraint FK_USER_IMA_RELATIONS_USER foreign key (cod_user)
      references "user" (cod_user)
      on delete restrict on update restrict;

alter table user_images
   add constraint FK_USER_IMA_RELATIONS_IMAGES foreign key (cod_image)
      references images (cod_image)
      on delete restrict on update restrict;

