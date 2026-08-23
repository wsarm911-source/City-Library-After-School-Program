import pandas as pd
import sqlite3
conn = sqlite3.connect("library Database.db")

print ("members table from db")
members = pd.read_sql("SELECT * FROM members", conn)
print(members)
print (members.shape)

print ("\nbooks table from db")
books = pd.read_sql("SELECT * FROM books", conn)
print(books)
print (books.shape)

print ("\ncheckouts table from db")
checkouts = pd.read_sql("SELECT * FROM checkouts", conn)
print(checkouts)
print (checkouts.shape)

print ("\nbook catalog json file ")
book_catalog = pd.read_json("Book Catalog.json")
print (book_catalog.head(10))
print (book_catalog.shape)

print ("\nreading kickout signups html file ")
reading_kickoff_signups = pd.read_html("Reading Kickoff Signups.html")[0]
print (reading_kickoff_signups.head(10))
print (reading_kickoff_signups.shape)