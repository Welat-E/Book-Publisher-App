CREATE TABLE "Users" (
  "user_id" integer PRIMARY KEY,
  "first_name" text,
  "last_name" text,
  "role" text,
  "email" text,
  "password" text
);

CREATE TABLE "Author" (
  "auhtor_id" integer PRIMARY KEY,
  "name" text,
  "book_id" text
);

CREATE TABLE "Publication_Details" (
  "book_id" integer,
  "publisher_id" integer,
  "price" integer,
  "country" integer,
  "author_id" integer,
  "units" integer,
  "release_date" text
);

CREATE TABLE "Publisher" (
  "publisher_id" integer PRIMARY KEY,
  "author_id" integer,
  "publisher_name" text
);

CREATE TABLE "Book" (
  "book_id" integer PRIMARY KEY,
  "publisher_id" integer,
  "author_id" integer,
  "cover_image" text
);

CREATE TABLE "Chapters" (
  "chapter_id" integer PRIMARY KEY,
  "book_id" integer,
  "pages" integer,
  "comments" text
);

ALTER TABLE "Author" ADD FOREIGN KEY ("auhtor_id") REFERENCES "Publisher" ("author_id");

ALTER TABLE "Book" ADD FOREIGN KEY ("publisher_id") REFERENCES "Publisher" ("publisher_id");

ALTER TABLE "Book" ADD FOREIGN KEY ("book_id") REFERENCES "Author" ("book_id");

ALTER TABLE "Book" ADD FOREIGN KEY ("book_id") REFERENCES "Chapters" ("book_id");

ALTER TABLE "Book" ADD FOREIGN KEY ("book_id") REFERENCES "Users" ("user_id");

ALTER TABLE "Publication_Details" ADD FOREIGN KEY ("book_id") REFERENCES "Book" ("book_id");

ALTER TABLE "Publication_Details" ADD FOREIGN KEY ("publisher_id") REFERENCES "Author" ("auhtor_id");
