/*==============================================================*/
/* Table: ubication                                             */
/*==============================================================*/
create table
   ubication (
      cod_ubi INT4 not null,
      country VARCHAR(100) null,
      constraint PK_UBICATION primary key (cod_ubi)
   );

INSERT INTO
   ubication (cod_ubi, country)
VALUES
   (1, 'Afghanistan'),
   (2, 'Albania'),
   (3, 'Algeria'),
   (4, 'Andorra'),
   (5, 'Angola'),
   (6, 'Antigua and Barbuda'),
   (7, 'Argentina'),
   (8, 'Armenia'),
   (9, 'Australia'),
   (10, 'Austria'),
   (11, 'Azerbaijan'),
   (12, 'Bahamas'),
   (13, 'Bahrain'),
   (14, 'Bangladesh'),
   (15, 'Barbados'),
   (16, 'Belarus'),
   (17, 'Belgium'),
   (18, 'Belize'),
   (19, 'Benin'),
   (20, 'Bhutan'),
   (21, 'Bolivia'),
   (22, 'Bosnia and Herzegovina'),
   (23, 'Botswana'),
   (24, 'Brazil'),
   (25, 'Brunei'),
   (26, 'Bulgaria'),
   (27, 'Burkina Faso'),
   (28, 'Burundi'),
   (29, 'Cabo Verde'),
   (30, 'Cambodia'),
   (31, 'Cameroon'),
   (32, 'Canada'),
   (33, 'Central African Republic'),
   (34, 'Chad'),
   (35, 'Chile'),
   (36, 'China'),
   (37, 'Colombia'),
   (38, 'Comoros'),
   (39, 'Congo, Democratic Republic of the'),
   (40, 'Congo, Republic of the'),
   (41, 'Costa Rica'),
   (42, 'Croatia'),
   (43, 'Cuba'),
   (44, 'Cyprus'),
   (45, 'Czech Republic'),
   (46, 'Denmark'),
   (47, 'Djibouti'),
   (48, 'Dominica'),
   (49, 'Dominican Republic'),
   (50, 'Ecuador'),
   (51, 'Egypt'),
   (52, 'El Salvador'),
   (53, 'Equatorial Guinea'),
   (54, 'Eritrea'),
   (55, 'Estonia'),
   (56, 'Eswatini'),
   (57, 'Ethiopia'),
   (58, 'Fiji'),
   (59, 'Finland'),
   (60, 'France'),
   (61, 'Gabon'),
   (62, 'Gambia'),
   (63, 'Georgia'),
   (64, 'Germany'),
   (65, 'Ghana'),
   (66, 'Greece'),
   (67, 'Grenada'),
   (68, 'Guatemala'),
   (69, 'Guinea'),
   (70, 'Guinea-Bissau'),
   (71, 'Guyana'),
   (72, 'Haiti'),
   (73, 'Honduras'),
   (74, 'Hungary'),
   (75, 'Iceland'),
   (76, 'India'),
   (77, 'Indonesia'),
   (78, 'Iran'),
   (79, 'Iraq'),
   (80, 'Ireland'),
   (81, 'Israel'),
   (82, 'Italy'),
   (83, 'Jamaica'),
   (84, 'Japan'),
   (85, 'Jordan'),
   (86, 'Kazakhstan'),
   (87, 'Kenya'),
   (88, 'Kiribati'),
   (89, 'Kuwait'),
   (90, 'Kyrgyzstan'),
   (91, 'Laos'),
   (92, 'Latvia'),
   (93, 'Lebanon'),
   (94, 'Lesotho'),
   (95, 'Liberia'),
   (96, 'Libya'),
   (97, 'Liechtenstein'),
   (98, 'Lithuania'),
   (99, 'Luxembourg'),
   (100, 'Madagascar'),
   (101, 'Malawi'),
   (102, 'Malaysia'),
   (103, 'Maldives'),
   (104, 'Mali'),
   (105, 'Malta'),
   (106, 'Marshall Islands'),
   (107, 'Mauritania'),
   (108, 'Mauritius'),
   (109, 'Mexico'),
   (110, 'Micronesia'),
   (111, 'Moldova'),
   (112, 'Monaco'),
   (113, 'Mongolia'),
   (114, 'Montenegro'),
   (115, 'Morocco'),
   (116, 'Mozambique'),
   (117, 'Myanmar'),
   (118, 'Namibia'),
   (119, 'Nauru'),
   (120, 'Nepal'),
   (121, 'Netherlands'),
   (122, 'New Zealand'),
   (123, 'Nicaragua'),
   (124, 'Niger'),
   (125, 'Nigeria'),
   (126, 'North Korea'),
   (127, 'North Macedonia'),
   (128, 'Norway'),
   (129, 'Oman'),
   (130, 'Pakistan'),
   (131, 'Palau'),
   (132, 'Panama'),
   (133, 'Papua New Guinea'),
   (134, 'Paraguay'),
   (135, 'Peru'),
   (136, 'Philippines'),
   (137, 'Poland'),
   (138, 'Portugal'),
   (139, 'Qatar'),
   (140, 'Romania'),
   (141, 'Russia'),
   (142, 'Rwanda'),
   (143, 'Saint Kitts and Nevis'),
   (144, 'Saint Lucia'),
   (145, 'Saint Vincent and the Grenadines'),
   (146, 'Samoa'),
   (147, 'San Marino'),
   (148, 'Sao Tome and Principe'),
   (149, 'Saudi Arabia'),
   (150, 'Senegal'),
   (151, 'Serbia'),
   (152, 'Seychelles'),
   (153, 'Sierra Leone'),
   (154, 'Singapore'),
   (155, 'Slovakia'),
   (156, 'Slovenia'),
   (157, 'Solomon Islands'),
   (158, 'Somalia'),
   (159, 'South Africa'),
   (160, 'South Korea'),
   (161, 'South Sudan'),
   (162, 'Spain'),
   (163, 'Sri Lanka'),
   (164, 'Sudan'),
   (165, 'Suriname'),
   (166, 'Sweden'),
   (167, 'Switzerland'),
   (168, 'Syria'),
   (169, 'Taiwan'),
   (170, 'Tajikistan'),
   (171, 'Tanzania'),
   (172, 'Thailand'),
   (173, 'Timor-Leste'),
   (174, 'Togo'),
   (175, 'Tonga'),
   (176, 'Trinidad and Tobago'),
   (177, 'Tunisia'),
   (178, 'Turkey'),
   (179, 'Turkmenistan'),
   (180, 'Tuvalu'),
   (181, 'Uganda'),
   (182, 'Ukraine'),
   (183, 'United Arab Emirates'),
   (184, 'United Kingdom'),
   (185, 'United States'),
   (186, 'Uruguay'),
   (187, 'Uzbekistan'),
   (188, 'Vanuatu'),
   (189, 'Vatican City'),
   (190, 'Venezuela'),
   (191, 'Vietnam'),
   (192, 'Yemen'),
   (193, 'Zambia'),
   (194, 'Zimbabwe');

/*==============================================================*/
/* Table: users_state                                                 */
/*==============================================================*/
create table
   users_state (
      cod_state INT4 not null,
      "state" VARCHAR(8) not null,
      constraint PK_STATE primary key (cod_state)
   );

INSERT INTO
   users_state (cod_state, state)
VALUES
   (1, 'enabled'),
   (2, 'disabled');

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

INSERT INTO
   date_descriptions (cod_description, "description")
VALUES
   (1, 'created'),
   (2, 'modified'),
   (3, 'birthday');

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