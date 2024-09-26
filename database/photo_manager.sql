/*==============================================================*/
/* Table: ubication                                             */
/*==============================================================*/
create table
   ubication (
      cod_ubi INT4 not null,
      country VARCHAR(100) null,
      constraint PK_UBICATION primary key (cod_ubi)
   );

/*==============================================================*/
/* Table: users_state                                                 */
/*==============================================================*/
create table
   users_state (
      cod_state INT4 not null,
      "state" VARCHAR(8) not null,
      constraint PK_STATE primary key (cod_state)
   );

/*==============================================================*/
/* Table: "user"                                                */
/*==============================================================*/
create table
   users (
      cod_user SERIAL not null,
      cod_ubi INT4 not null, -- Ubication relation
      cod_state INT4 not null, -- User satet relation
      username VARCHAR(15) UNIQUE not null,
      email VARCHAR(50) not null,
      "password" VARCHAR(300) not null,
      constraint PK_USER primary key (cod_user),
      constraint fk_user_ubication foreign key (cod_ubi) references ubication (cod_ubi),
      constraint fk_user_state foreign key (cod_state) references users_state (cod_state)
   );

/*==============================================================*/
/* Table: dates                                                 */
/*==============================================================*/
create table
   dates (
      cod_date INT4 not null,
      "year" INT4 not null,
      "month" INT4 not null,
      "day" DATE not null,
      constraint PK_DATES primary key (cod_date)
   );

/*==============================================================*/
/* Table: images                                                */
/*==============================================================*/
create table
   images (
      cod_image SERIAL not null,
      cod_ubi INT4 not null,
      cod_user INT4 not null, -- User relation
      uploadedat INT4 not null, -- Dates relation
      "image" VARCHAR(300) not null,
      constraint PK_IMAGES primary key (cod_image),
      constraint fk_image_dates foreign key (uploadedat) references dates (cod_date),
      constraint fk_user_image foreign key (cod_user) references users (cod_user)
   );

/*==============================================================*/
/* Table: date_descriptions                                     */
/*==============================================================*/
create table
   date_descriptions (
      cod_description INT4 not null,
      "description" VARCHAR(8) not null,
      constraint PK_DESCR primary key (cod_description)
   );

/*==============================================================*/
/* Table: users_dates                                            */
/*==============================================================*/
create table
   users_dates (
      cod_date INT4 not null, -- Date relation
      cod_user INT4 not null, -- User relation
      cod_description INT4 not null, -- Date descriptions relation
      constraint PK_USER_DATES primary key (cod_date, cod_user, cod_description),
      constraint fk_user_dates foreign key (cod_user) references users (cod_user),
      constraint fk_dates_description foreign key (cod_description) references date_descriptions (cod_description)
   );