PGDMP  8            	    	    |           publisher_book_app    16.4    16.4                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                        0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            !           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            "           1262    16394    publisher_book_app    DATABASE     t   CREATE DATABASE publisher_book_app WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
 "   DROP DATABASE publisher_book_app;
                postgres    false            �            1259    16409    Author    TABLE     }   CREATE TABLE public."Author" (
    author_id "char" NOT NULL,
    name "char",
    author_image text,
    birth_date date
);
    DROP TABLE public."Author";
       public         heap    postgres    false            �            1259    16416    Publication_Details    TABLE       CREATE TABLE public."Publication_Details" (
    book_id "char" NOT NULL,
    publisher_id "char",
    price numeric,
    country "char",
    author_id "char",
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
    password "char",
    publisher_id "char",
    author_id "char"
);
    DROP TABLE public."Users";
       public         heap    postgres    false                      0    16409    Author 
   TABLE DATA           M   COPY public."Author" (author_id, name, author_image, birth_date) FROM stdin;
    public          postgres    false    217   �                 0    16416    Publication_Details 
   TABLE DATA           �   COPY public."Publication_Details" (book_id, publisher_id, price, country, author_id, units, release_date, cover_image, pages, chapters, "Link") FROM stdin;
    public          postgres    false    218   �                 0    16404 	   Publisher 
   TABLE DATA           C   COPY public."Publisher" (publisher_id, publisher_name) FROM stdin;
    public          postgres    false    216   �                 0    16399    Users 
   TABLE DATA           r   COPY public."Users" (user_id, first_name, last_name, admin, email, password, publisher_id, author_id) FROM stdin;
    public          postgres    false    215   �       �           2606    16415    Author Author_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public."Author"
    ADD CONSTRAINT "Author_pkey" PRIMARY KEY (author_id);
 @   ALTER TABLE ONLY public."Author" DROP CONSTRAINT "Author_pkey";
       public            postgres    false    217            �           2606    16422 ,   Publication_Details Publication_Details_pkey 
   CONSTRAINT     s   ALTER TABLE ONLY public."Publication_Details"
    ADD CONSTRAINT "Publication_Details_pkey" PRIMARY KEY (book_id);
 Z   ALTER TABLE ONLY public."Publication_Details" DROP CONSTRAINT "Publication_Details_pkey";
       public            postgres    false    218            �           2606    16408    Publisher Publisher_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public."Publisher"
    ADD CONSTRAINT "Publisher_pkey" PRIMARY KEY (publisher_id);
 F   ALTER TABLE ONLY public."Publisher" DROP CONSTRAINT "Publisher_pkey";
       public            postgres    false    216                       2606    16403    Users Users_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY (user_id);
 >   ALTER TABLE ONLY public."Users" DROP CONSTRAINT "Users_pkey";
       public            postgres    false    215            �           2606    16423    Users author_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT author_id_fkey FOREIGN KEY (author_id) REFERENCES public."Author"(author_id) NOT VALID;
 @   ALTER TABLE ONLY public."Users" DROP CONSTRAINT author_id_fkey;
       public          postgres    false    217    215    3459            �           2606    16438 6   Publication_Details publication_details_fkey_to_author    FK CONSTRAINT     �   ALTER TABLE ONLY public."Publication_Details"
    ADD CONSTRAINT publication_details_fkey_to_author FOREIGN KEY (author_id) REFERENCES public."Author"(author_id) NOT VALID;
 b   ALTER TABLE ONLY public."Publication_Details" DROP CONSTRAINT publication_details_fkey_to_author;
       public          postgres    false    3459    218    217            �           2606    16433 9   Publication_Details publication_details_fkey_to_publisher    FK CONSTRAINT     �   ALTER TABLE ONLY public."Publication_Details"
    ADD CONSTRAINT publication_details_fkey_to_publisher FOREIGN KEY (publisher_id) REFERENCES public."Publisher"(publisher_id) NOT VALID;
 e   ALTER TABLE ONLY public."Publication_Details" DROP CONSTRAINT publication_details_fkey_to_publisher;
       public          postgres    false    216    218    3457            �           2606    16428    Users publisher_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT publisher_id_fkey FOREIGN KEY (publisher_id) REFERENCES public."Publisher"(publisher_id) NOT VALID;
 C   ALTER TABLE ONLY public."Users" DROP CONSTRAINT publisher_id_fkey;
       public          postgres    false    216    3457    215                  x������ � �            x������ � �            x������ � �            x������ � �     