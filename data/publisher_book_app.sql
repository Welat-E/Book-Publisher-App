PGDMP      *    
        	    |           publisher_book_app    16.4    16.4                 0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            !           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            "           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            #           1262    16394    publisher_book_app    DATABASE     t   CREATE DATABASE publisher_book_app WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
 "   DROP DATABASE publisher_book_app;
                postgres    false            �            1259    16409    Author    TABLE     r   CREATE TABLE public."Author" (
    name "char",
    author_image text,
    birth_date date,
    user_id "char"
);
    DROP TABLE public."Author";
       public         heap    postgres    false            �            1259    24640    Book    TABLE     �   CREATE TABLE public."Book" (
    book_id integer NOT NULL,
    user_id integer,
    release_date "char",
    cover_image "char",
    chapters integer,
    pages integer
);
    DROP TABLE public."Book";
       public         heap    postgres    false            �            1259    16416    Publication_Details    TABLE        CREATE TABLE public."Publication_Details" (
    book_id "char" NOT NULL,
    user_id "char",
    price numeric,
    country "char",
    units integer,
    release_date date,
    cover_image text,
    pages integer,
    chapters integer,
    "Link" text
);
 )   DROP TABLE public."Publication_Details";
       public         heap    postgres    false            �            1259    16404 	   Publisher    TABLE     a   CREATE TABLE public."Publisher" (
    publisher_id "char" NOT NULL,
    publisher_name "char"
);
    DROP TABLE public."Publisher";
       public         heap    postgres    false            �            1259    16399    Users    TABLE     �   CREATE TABLE public."Users" (
    user_id "char" NOT NULL,
    first_name "char",
    last_name "char",
    admin boolean,
    email "char",
    password "char"
);
    DROP TABLE public."Users";
       public         heap    postgres    false                      0    16409    Author 
   TABLE DATA           K   COPY public."Author" (name, author_image, birth_date, user_id) FROM stdin;
    public          postgres    false    217   Z                 0    24640    Book 
   TABLE DATA           ^   COPY public."Book" (book_id, user_id, release_date, cover_image, chapters, pages) FROM stdin;
    public          postgres    false    219   w                 0    16416    Publication_Details 
   TABLE DATA           �   COPY public."Publication_Details" (book_id, user_id, price, country, units, release_date, cover_image, pages, chapters, "Link") FROM stdin;
    public          postgres    false    218   �                 0    16404 	   Publisher 
   TABLE DATA           C   COPY public."Publisher" (publisher_id, publisher_name) FROM stdin;
    public          postgres    false    216   �                 0    16399    Users 
   TABLE DATA           Y   COPY public."Users" (user_id, first_name, last_name, admin, email, password) FROM stdin;
    public          postgres    false    215   �       �           2606    24644    Book Book_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public."Book"
    ADD CONSTRAINT "Book_pkey" PRIMARY KEY (book_id);
 <   ALTER TABLE ONLY public."Book" DROP CONSTRAINT "Book_pkey";
       public            postgres    false    219            �           2606    16422 ,   Publication_Details Publication_Details_pkey 
   CONSTRAINT     s   ALTER TABLE ONLY public."Publication_Details"
    ADD CONSTRAINT "Publication_Details_pkey" PRIMARY KEY (book_id);
 Z   ALTER TABLE ONLY public."Publication_Details" DROP CONSTRAINT "Publication_Details_pkey";
       public            postgres    false    218            �           2606    16408    Publisher Publisher_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public."Publisher"
    ADD CONSTRAINT "Publisher_pkey" PRIMARY KEY (publisher_id);
 F   ALTER TABLE ONLY public."Publisher" DROP CONSTRAINT "Publisher_pkey";
       public            postgres    false    216            �           2606    16403    Users Users_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY (user_id);
 >   ALTER TABLE ONLY public."Users" DROP CONSTRAINT "Users_pkey";
       public            postgres    false    215                  x������ � �            x������ � �            x������ � �            x������ � �            x������ � �     