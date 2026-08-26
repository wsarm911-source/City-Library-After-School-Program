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

# Question 1 : How much is each member borrowing?
query1 = """
SELECT 
    members.first_name as member,
    COUNT(checkouts.member_id) AS number_of_borrowing
FROM members
LEFT JOIN checkouts
    ON members.member_id = checkouts.member_id
GROUP BY members.member_id;
"""

ques1 = pd.read_sql_query(query1, conn)
print ("\n\n" , ques1.head(10))

# Question 2 : Which books match a chosen author pattern?
# chosen pattern = "A%"
query2 = """
SELECT 
    title 
FROM books
WHERE author LIKE "A%"
"""

ques2 = pd.read_sql_query(query2, conn)
print ("\n\n" , ques2.head())

# Question 3 : What are the most popular books?
query3 = """
SELECT 
    books.title,
    COUNT(checkouts.book_id) AS number_of_borrowing
FROM books
JOIN checkouts
    ON books.book_id = checkouts.book_id
GROUP BY checkouts.book_id
ORDER BY number_of_borrowing DESC limit 5 ;
"""

ques3 = pd.read_sql_query(query3, conn)
print ("\n\n" , ques3)

# Question 4 : Who are the most active readers?
query4 = """
SELECT 
    members.first_name,
    COUNT(checkouts.member_id) AS number_of_borrowing
FROM members
JOIN checkouts
    ON members.member_id = checkouts.member_id
GROUP BY checkouts.member_id
ORDER BY number_of_borrowing DESC limit 10 ;
"""

ques4 = pd.read_sql_query(query4, conn)
print ("\n\n" , ques4)

# Question 5 : What does a neighborhood's activity look like further back in time?
# chosen neighborhood : "Maadi"
query5 = """
SELECT 
    members.first_name as member,
    COUNT(checkouts.member_id) AS number_of_borrowing
FROM members
LEFT JOIN checkouts
    ON members.member_id = checkouts.member_id
GROUP BY members.member_id
HAVING neighborhood = "Maadi"
ORDER BY join_date DESC limit 10 OFFSET 10;
"""

ques5 = pd.read_sql_query(query5, conn)
print ("\n\n" , ques5)

# Merge members with checkouts
result = pd.merge(
    checkouts,
    members,
    on="member_id",
    how="left" )

# Add the number of books borrowed by each member
result["books_borrowed"] = result.groupby("member_id")["checkout_id"].transform("count")

# Merge the JSON data with the result
result = pd.merge(
    result,
    book_catalog,
    on="book_id",
    how="left" )

# Merge the HTML file with the result 

reading_kickoff_signups = reading_kickoff_signups.rename(columns={
    "Member ID": "member_id",
    "Book ID": "book_id",
    "Checkout Date": "checkout_date"})

new_checkouts = reading_kickoff_signups.merge(members, on="member_id")
new_checkouts = new_checkouts.merge(book_catalog, on="book_id")


new_checkouts["books_borrowed"] = new_checkouts.groupby("member_id")["book_id"].transform("count")

result = pd.concat([result, new_checkouts], ignore_index=True)

print("\n\n" , result.shape)
print (result.columns)
print(result)

result.to_csv("Task1_combined_data.csv" , index=False)