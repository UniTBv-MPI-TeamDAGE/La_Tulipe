--
-- PostgreSQL database dump
--

\restrict pmaPrZXoHCP1ZGSf2snDn5Vdzoina7KpdGv6Jq7wC7hiLeyUtiF4vbUiSSs6zEP

-- Dumped from database version 18.2
-- Dumped by pg_dump version 18.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: order_status_enum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.order_status_enum AS ENUM (
    'PENDING',
    'CONFIRMED',
    'DELIVERED',
    'CANCELLED'
);


ALTER TYPE public.order_status_enum OWNER TO postgres;

--
-- Name: product_season_enum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.product_season_enum AS ENUM (
    'ALL_SEASON',
    'SPRING',
    'SUMMER',
    'AUTUMN',
    'WINTER'
);


ALTER TYPE public.product_season_enum OWNER TO postgres;

--
-- Name: product_type_enum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.product_type_enum AS ENUM (
    'INDIVIDUAL',
    'BOUQUET'
);


ALTER TYPE public.product_type_enum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: colors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.colors (
    id integer NOT NULL,
    name character varying NOT NULL,
    hex_code character varying
);


ALTER TABLE public.colors OWNER TO postgres;

--
-- Name: colors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.colors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.colors_id_seq OWNER TO postgres;

--
-- Name: colors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.colors_id_seq OWNED BY public.colors.id;


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    id integer NOT NULL,
    order_id integer NOT NULL,
    product_id integer,
    product_name character varying,
    quantity integer NOT NULL,
    unit_price double precision NOT NULL,
    line_total double precision NOT NULL,
    color_id integer,
    color_name character varying,
    composition json
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_items_id_seq OWNER TO postgres;

--
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    order_number character varying NOT NULL,
    user_id integer,
    customer_name character varying NOT NULL,
    customer_email character varying NOT NULL,
    customer_phone character varying NOT NULL,
    delivery_address character varying NOT NULL,
    card_message character varying,
    total_price double precision NOT NULL,
    status public.order_status_enum NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: product_color_stocks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_color_stocks (
    id integer NOT NULL,
    product_id integer NOT NULL,
    color_id integer NOT NULL,
    stock integer NOT NULL
);


ALTER TABLE public.product_color_stocks OWNER TO postgres;

--
-- Name: product_color_stocks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.product_color_stocks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.product_color_stocks_id_seq OWNER TO postgres;

--
-- Name: product_color_stocks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.product_color_stocks_id_seq OWNED BY public.product_color_stocks.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying NOT NULL,
    price double precision NOT NULL,
    stock integer NOT NULL,
    image_url character varying,
    is_featured boolean NOT NULL,
    category_id integer NOT NULL,
    product_type public.product_type_enum NOT NULL,
    description character varying NOT NULL,
    season public.product_season_enum NOT NULL
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying CONSTRAINT users_nume_not_null NOT NULL,
    email character varying NOT NULL,
    password_hash character varying NOT NULL,
    role character varying,
    phone character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: colors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.colors ALTER COLUMN id SET DEFAULT nextval('public.colors_id_seq'::regclass);


--
-- Name: order_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: product_color_stocks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_color_stocks ALTER COLUMN id SET DEFAULT nextval('public.product_color_stocks_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
a1b2c3d4e5f6
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, name) FROM stdin;
1	Iubire & Pasiune
2	Prietenie & Bucurie
3	Respect & Admiratie
4	Puritate & Nou Inceput
5	Recunostinta
6	Alinare & Condoleante
\.


--
-- Data for Name: colors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.colors (id, name, hex_code) FROM stdin;
1	Red	#FF0000
2	White	#FFFFFF
3	Pink	#FFC0CB
4	Yellow	#FFD700
5	Orange	#FFA500
6	Purple	#800080
7	Blue	#0000FF
8	Cream	#FFFDD0
\.


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_items (id, order_id, product_id, product_name, quantity, unit_price, line_total, color_id, color_name, composition) FROM stdin;
1	1	18	Spring Bouquet	1	90	90	\N	\N	null
2	1	\N	Custom Bouquet	1	169	169	\N	\N	"[{\\"product_id\\": 1, \\"product_name\\": \\"Trandafir\\", \\"color_id\\": 1, \\"color_name\\": \\"Red\\", \\"quantity\\": 5}, {\\"product_id\\": 7, \\"product_name\\": \\"Bujor\\", \\"color_id\\": 1, \\"color_name\\": \\"Red\\", \\"quantity\\": 3}, {\\"product_id\\": 10, \\"product_name\\": \\"Crizantema\\", \\"color_id\\": 3, \\"color_name\\": \\"Pink\\", \\"quantity\\": 1}]"
3	2	7	Bujor	5	18	90	3	Pink	null
4	2	\N	Custom Bouquet	1	193	193	\N	\N	"[{\\"product_id\\": 7, \\"product_name\\": \\"Bujor\\", \\"color_id\\": 2, \\"color_name\\": \\"White\\", \\"quantity\\": 5}, {\\"product_id\\": 9, \\"product_name\\": \\"Frezie\\", \\"color_id\\": 2, \\"color_name\\": \\"White\\", \\"quantity\\": 3}, {\\"product_id\\": 10, \\"product_name\\": \\"Crizantema\\", \\"color_id\\": 2, \\"color_name\\": \\"White\\", \\"quantity\\": 1}, {\\"product_id\\": 15, \\"product_name\\": \\"Eucalipt\\", \\"quantity\\": 4}, {\\"product_id\\": 12, \\"product_name\\": \\"Gypsophila\\", \\"quantity\\": 3}]"
5	3	\N	Custom Bouquet	1	261	261	\N	\N	"[{\\"product_id\\": 1, \\"product_name\\": \\"Trandafir\\", \\"color_id\\": 2, \\"color_name\\": \\"White\\", \\"quantity\\": 7}, {\\"product_id\\": 4, \\"product_name\\": \\"Cala\\", \\"color_id\\": 2, \\"color_name\\": \\"White\\", \\"quantity\\": 4}, {\\"product_id\\": 6, \\"product_name\\": \\"Alstroemeria\\", \\"color_id\\": 2, \\"color_name\\": \\"White\\", \\"quantity\\": 3}, {\\"product_id\\": 12, \\"product_name\\": \\"Gypsophila\\", \\"quantity\\": 5}]"
6	4	17	Love Bouquet	5	150	750	\N	\N	null
7	5	2	Orhidee	5	40	200	6	Purple	null
8	6	2	Orhidee	5	40	200	2	White	null
9	7	2	Orhidee	3	40	120	6	Purple	null
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, order_number, user_id, customer_name, customer_email, customer_phone, delivery_address, card_message, total_price, status, created_at) FROM stdin;
2	ORD-20260404121234-EE10EA25	5	Titi Bucatarul	titiBuc@titi.com	0721345678	Strada Iuliu Maniu	\N	283	DELIVERED	2026-04-04 15:12:34.212518+03
1	ORD-20260404120535-758CD257	5	Titi Bucatarul	titiBuc@titi.com	0721345678	Strada Iuliu Maniu	\N	259	CONFIRMED	2026-04-04 15:05:35.929732+03
3	ORD-20260405081946-643A0F4A	4	Daniela Lupu	danaBoss@lt.com	07345678901	Bulevardul Dunărea 	\N	261	CANCELLED	2026-04-05 11:19:46.923315+03
4	ORD-20260405082306-EBA580AB	4	Daniela Lupu	danaBoss@lt.com	0754668860	Bulevardul Dunărea 	\N	750	DELIVERED	2026-04-05 11:23:06.66742+03
6	ORD-20260406103519-311439D9	4	Daniela Lupu	danaBoss@lt.com	0754668860	Bulevardul Dunărea 64	\N	200	PENDING	2026-04-06 13:35:19.247757+03
5	ORD-20260405082643-0FA8CD77	4	Daniela Lupu	danaBoss@lt.com	0754668860	Bulevardul Dunărea 64	\N	200	CONFIRMED	2026-04-05 11:26:43.679701+03
7	ORD-20260406103747-D84E9C28	4	Daniela Lupu	danaBoss@lt.com	0754668860	Bulevardul Dunărea 64	\N	120	PENDING	2026-04-06 13:37:47.446905+03
\.


--
-- Data for Name: product_color_stocks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.product_color_stocks (id, product_id, color_id, stock) FROM stdin;
3	1	3	25
5	2	3	15
8	4	3	20
9	4	6	8
10	5	4	15
11	5	5	15
12	5	1	4
14	6	3	5
15	6	4	5
16	6	5	5
17	6	6	5
21	8	1	20
22	8	4	20
23	8	5	20
24	8	6	10
25	8	3	10
27	9	3	10
28	9	4	9
30	10	6	15
32	10	4	10
33	13	6	15
34	13	3	10
35	13	2	10
36	14	5	20
37	14	2	20
38	14	3	10
39	14	4	15
1	1	1	45
20	7	1	7
31	10	3	14
18	7	2	20
19	7	3	20
26	9	2	22
29	10	2	14
2	1	2	18
7	4	2	26
13	6	2	2
4	2	2	25
6	2	6	7
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (id, name, price, stock, image_url, is_featured, category_id, product_type, description, season) FROM stdin;
4	Cala	12	56	https://images.pexels.com/photos/11991760/pexels-photo-11991760.jpeg?auto=compress&cs=tinysrgb&w=800	f	4	INDIVIDUAL	Forma sculpturala si culoare pura. Alegerea clasica pentru nunti si botezuri.	ALL_SEASON
6	Alstroemeria	11	22	https://images.pexels.com/photos/8789648/pexels-photo-8789648.jpeg?auto=compress&cs=tinysrgb&w=800	f	5	INDIVIDUAL	Floare longeviva cu petale tigrate. Simbolizeaza prietenia durabila si recunostinta.	ALL_SEASON
12	Gypsophila	8	32	https://images.pexels.com/photos/31212419/pexels-photo-31212419.jpeg?auto=compress&cs=tinysrgb&w=800	f	4	INDIVIDUAL	Floricele mici ca niste nori delicati. Completeaza orice buchet, simbol al inocentei.	ALL_SEASON
5	Gerbera	10	35	https://images.pexels.com/photos/850359/pexels-photo-850359.jpeg?auto=compress&cs=tinysrgb&w=800	f	2	INDIVIDUAL	Colorata si jucausa, simbolizeaza prietenia sincera si un suflet deschis.	ALL_SEASON
3	Floarea-soarelui	20	30	https://images.pexels.com/photos/289628/pexels-photo-289628.jpeg?auto=compress&cs=tinysrgb&w=800	t	2	INDIVIDUAL	Radianta si vesela, urmeaza lumina soarelui si aduce bucurie oriunde ajunge.	SUMMER
8	Lalea	9	80	https://images.pexels.com/photos/10817651/pexels-photo-10817651.jpeg?auto=compress&cs=tinysrgb&w=800	t	1	INDIVIDUAL	Eleganta si simpla, declaratie de iubire discreta si sincera.	SPRING
13	Lisianthus	15	35	https://images.pexels.com/photos/4355514/pexels-photo-4355514.jpeg?auto=compress&cs=tinysrgb&w=800	f	5	INDIVIDUAL	Petale suprapuse ca ale unui trandafir. Transmite eleganța si multumire profunda.	SUMMER
14	Crin	18	65	https://images.pexels.com/photos/10477649/pexels-photo-10477649.jpeg?auto=compress&cs=tinysrgb&w=800	f	6	INDIVIDUAL	Maiestuos si intens parfumat. Transmite pace, puritate si alinare sufleteasca.	ALL_SEASON
18	Spring Bouquet	90	9	https://images.pexels.com/photos/4022223/pexels-photo-4022223.jpeg?auto=compress&cs=tinysrgb&w=800	f	2	BOUQUET	Lalele rosii: 5\nFrezii: 3\nBujori roz: 2\nGypsophila	SPRING
17	Love Bouquet	150	10	https://images.pexels.com/photos/8903960/pexels-photo-8903960.jpeg?auto=compress&cs=tinysrgb&w=800	f	1	BOUQUET	Trandafiri rosii: 5\nBujori roz: 3\nEucalipt	ALL_SEASON
7	Bujor	18	47	https://images.pexels.com/photos/5566048/pexels-photo-5566048.jpeg?auto=compress&cs=tinysrgb&w=800	f	1	INDIVIDUAL	Floare voluminoasa cu parfum dulce. Asociata cu prosperitatea si dragostea adevarata.	SPRING
19	White Bouquet	170	10	https://images.pexels.com/photos/32552675/pexels-photo-32552675.jpeg?auto=compress&cs=tinysrgb&w=800	f	4	BOUQUET	Cale albe: 5\nCrini albi: 3\nLisianthus \nEucalipt	ALL_SEASON
9	Frezie	12	42	https://images.pexels.com/photos/31321813/pexels-photo-31321813.jpeg?auto=compress&cs=tinysrgb&w=800	t	2	INDIVIDUAL	Parfum delicat si flori in buchețele. Transmit ganduri frumoase celor dragi.	SPRING
10	Crizantema	15	53	https://images.pexels.com/photos/8194982/pexels-photo-8194982.jpeg?auto=compress&cs=tinysrgb&w=800	f	3	INDIVIDUAL	Rezistenta si eleganta. Simbolizeaza longevitatea si respectul fata de cei dragi.	AUTUMN
15	Eucalipt	7	31	https://images.pexels.com/photos/15385822/pexels-photo-15385822.jpeg?auto=compress&cs=tinysrgb&w=800	f	4	INDIVIDUAL	Verde aromat folosit ca filler. Adauga textura, prospețime si un parfum discret de padure.	ALL_SEASON
20	Cactus	35	2	\N	f	5	INDIVIDUAL		ALL_SEASON
1	Trandafir	20	88	https://images.pexels.com/photos/15934045/pexels-photo-15934045.jpeg?auto=compress&cs=tinysrgb&w=800	t	1	INDIVIDUAL	Regele florilor. Simbolizeaza iubirea ai pasiunea, perfect pentru orice ocazie romantica.	ALL_SEASON
2	Orhidee	40	47	https://images.pexels.com/photos/5714450/pexels-photo-5714450.jpeg?auto=compress&cs=tinysrgb&w=800	f	3	INDIVIDUAL	Exotica si rafinata, orhideea transmite admiratie profunda. Inflorire de 2–3 luni.	ALL_SEASON
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, password_hash, role, phone) FROM stdin;
1	Dana Lupu	danalupuT1@yahoo.com	$2b$12$qZkpYA5ydIV59cl..qDdwOkscJYXk4bb670AWiUtrPaT2/91zP0WK	customer	
2	Ana Popescu	ana@example.com	$2b$12$AyZnKmc5llgwCisB6OKdTu7uZ/EJ5lvm0Soyqb10cUvZpfxV9BVKC	customer	0747 789 123
3	Admin La Tulipe	admin@latulipe.ro	$2b$12$bjLQjQw0e1WKl8uzsO98uu30dKJ.7F4a0up8mWar7Q3aHnvX5Ab42	admin	0723658900
4	Daniela Lupu	danaBoss@lt.com	$2b$12$xfj/X8/IGpJT8Dt6W61e/Oa4bVxPYh15ekM90EbZ.u5fT.jGYb4pG	admin	\N
5	Titi Bucatarul	titiBuc@titi.com	$2b$12$uEWwTn5YMtyAnXdbt4CSyO8Mqp.A9WBNOlCI.zh5mWt82NtxvRqwy	customer	\N
6	Daniela Lupu	daniela.lupu39@yahoo.com	$2b$12$aJieKPjNzUvZcmyRMBYMLeHtayjyk9GINcnufP1z/vpxMsFHlYplK	admin	+40754668860
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 6, true);


--
-- Name: colors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.colors_id_seq', 8, true);


--
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_items_id_seq', 9, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 7, true);


--
-- Name: product_color_stocks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.product_color_stocks_id_seq', 39, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_seq', 20, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: categories categories_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_name_key UNIQUE (name);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: colors colors_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.colors
    ADD CONSTRAINT colors_name_key UNIQUE (name);


--
-- Name: colors colors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.colors
    ADD CONSTRAINT colors_pkey PRIMARY KEY (id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: product_color_stocks product_color_stocks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_color_stocks
    ADD CONSTRAINT product_color_stocks_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: product_color_stocks uq_product_color_stocks_product_color; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_color_stocks
    ADD CONSTRAINT uq_product_color_stocks_product_color UNIQUE (product_id, color_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_categories_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_categories_id ON public.categories USING btree (id);


--
-- Name: ix_colors_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_colors_id ON public.colors USING btree (id);


--
-- Name: ix_order_items_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_items_id ON public.order_items USING btree (id);


--
-- Name: ix_orders_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_id ON public.orders USING btree (id);


--
-- Name: ix_orders_order_number; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_orders_order_number ON public.orders USING btree (order_number);


--
-- Name: ix_product_color_stocks_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_color_stocks_id ON public.product_color_stocks USING btree (id);


--
-- Name: ix_products_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_id ON public.products USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: order_items fk_order_items_color_id_colors; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT fk_order_items_color_id_colors FOREIGN KEY (color_id) REFERENCES public.colors(id);


--
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- Name: order_items order_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: product_color_stocks product_color_stocks_color_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_color_stocks
    ADD CONSTRAINT product_color_stocks_color_id_fkey FOREIGN KEY (color_id) REFERENCES public.colors(id);


--
-- Name: product_color_stocks product_color_stocks_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_color_stocks
    ADD CONSTRAINT product_color_stocks_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- PostgreSQL database dump complete
--

\unrestrict pmaPrZXoHCP1ZGSf2snDn5Vdzoina7KpdGv6Jq7wC7hiLeyUtiF4vbUiSSs6zEP

