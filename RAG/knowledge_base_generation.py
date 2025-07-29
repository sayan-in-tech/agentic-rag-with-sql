# Construct a full RAG knowledge base text from the given JSON schema
import json

# Given schema as JSON string (truncated here, assume full schema is loaded)
schema_json = [
  "Table: Album\nColumns:\n  - AlbumId (INTEGER) [PK] [NOT NULL]\n  - Title (NVARCHAR(160)) [NOT NULL]\n  - ArtistId (INTEGER) [NOT NULL]\nForeign Keys:\n  - ArtistId → Artist.ArtistId",
  "Table: Artist\nColumns:\n  - ArtistId (INTEGER) [PK] [NOT NULL]\n  - Name (NVARCHAR(120))",
  "Table: Customer\nColumns:\n  - CustomerId (INTEGER) [PK] [NOT NULL]\n  - FirstName (NVARCHAR(40)) [NOT NULL]\n  - LastName (NVARCHAR(20)) [NOT NULL]\n  - Company (NVARCHAR(80))\n  - Address (NVARCHAR(70))\n  - City (NVARCHAR(40))\n  - State (NVARCHAR(40))\n  - Country (NVARCHAR(40))\n  - PostalCode (NVARCHAR(10))\n  - Phone (NVARCHAR(24))\n  - Fax (NVARCHAR(24))\n  - Email (NVARCHAR(60)) [NOT NULL]\n  - SupportRepId (INTEGER)\nForeign Keys:\n  - SupportRepId → Employee.EmployeeId",
  "Table: Employee\nColumns:\n  - EmployeeId (INTEGER) [PK] [NOT NULL]\n  - LastName (NVARCHAR(20)) [NOT NULL]\n  - FirstName (NVARCHAR(20)) [NOT NULL]\n  - Title (NVARCHAR(30))\n  - ReportsTo (INTEGER)\n  - BirthDate (DATETIME)\n  - HireDate (DATETIME)\n  - Address (NVARCHAR(70))\n  - City (NVARCHAR(40))\n  - State (NVARCHAR(40))\n  - Country (NVARCHAR(40))\n  - PostalCode (NVARCHAR(10))\n  - Phone (NVARCHAR(24))\n  - Fax (NVARCHAR(24))\n  - Email (NVARCHAR(60))\nForeign Keys:\n  - ReportsTo → Employee.EmployeeId",
  "Table: Genre\nColumns:\n  - GenreId (INTEGER) [PK] [NOT NULL]\n  - Name (NVARCHAR(120))",
  "Table: Invoice\nColumns:\n  - InvoiceId (INTEGER) [PK] [NOT NULL]\n  - CustomerId (INTEGER) [NOT NULL]\n  - InvoiceDate (DATETIME) [NOT NULL]\n  - BillingAddress (NVARCHAR(70))\n  - BillingCity (NVARCHAR(40))\n  - BillingState (NVARCHAR(40))\n  - BillingCountry (NVARCHAR(40))\n  - BillingPostalCode (NVARCHAR(10))\n  - Total (NUMERIC(10,2)) [NOT NULL]\nForeign Keys:\n  - CustomerId → Customer.CustomerId",
  "Table: InvoiceLine\nColumns:\n  - InvoiceLineId (INTEGER) [PK] [NOT NULL]\n  - InvoiceId (INTEGER) [NOT NULL]\n  - TrackId (INTEGER) [NOT NULL]\n  - UnitPrice (NUMERIC(10,2)) [NOT NULL]\n  - Quantity (INTEGER) [NOT NULL]\nForeign Keys:\n  - TrackId → Track.TrackId\n  - InvoiceId → Invoice.InvoiceId",
  "Table: MediaType\nColumns:\n  - MediaTypeId (INTEGER) [PK] [NOT NULL]\n  - Name (NVARCHAR(120))",
  "Table: Playlist\nColumns:\n  - PlaylistId (INTEGER) [PK] [NOT NULL]\n  - Name (NVARCHAR(120))",
  "Table: PlaylistTrack\nColumns:\n  - PlaylistId (INTEGER) [PK] [NOT NULL]\n  - TrackId (INTEGER) [PK] [NOT NULL]\nForeign Keys:\n  - TrackId → Track.TrackId\n  - PlaylistId → Playlist.PlaylistId",
  "Table: Track\nColumns:\n  - TrackId (INTEGER) [PK] [NOT NULL]\n  - Name (NVARCHAR(200)) [NOT NULL]\n  - AlbumId (INTEGER)\n  - MediaTypeId (INTEGER) [NOT NULL]\n  - GenreId (INTEGER)\n  - Composer (NVARCHAR(220))\n  - Milliseconds (INTEGER) [NOT NULL]\n  - Bytes (INTEGER)\n  - UnitPrice (NUMERIC(10,2)) [NOT NULL]\nForeign Keys:\n  - MediaTypeId → MediaType.MediaTypeId\n  - GenreId → Genre.GenreId\n  - AlbumId → Album.AlbumId"
]

# Business logic and query examples to append
business_logic = """
---
[BUSINESS LOGIC]

- Revenue per customer = SUM(Invoice.Total) GROUP BY CustomerId
- Churned customers = Customers who haven't purchased in the last 12 months
- Top-selling genre = COUNT(InvoiceLine.TrackId) JOIN Track → Genre
- Most valuable customer = MAX(SUM(Invoice.Total)) GROUP BY CustomerId
- Employee hierarchy = Employee.ReportsTo forms a tree structure of managers
- Playlist popularity = COUNT(PlaylistTrack.TrackId) GROUP BY PlaylistId
- Monthly revenue = SUM(Invoice.Total) GROUP BY strftime('%Y-%m', InvoiceDate)
- Artist revenue = SUM(UnitPrice * Quantity) JOIN Track → Album → Artist
"""

sample_queries = """
---
[EXAMPLE QUERIES]

Q: Which artist generated the highest sales?
SQL:
SELECT a.Name, SUM(il.UnitPrice * il.Quantity) AS TotalSales
FROM InvoiceLine il
JOIN Track t ON il.TrackId = t.TrackId
JOIN Album al ON t.AlbumId = al.AlbumId
JOIN Artist a ON al.ArtistId = a.ArtistId
GROUP BY a.Name
ORDER BY TotalSales DESC
LIMIT 1;

---

Q: Who are the top 5 customers by total spend?
SQL:
SELECT c.FirstName || ' ' || c.LastName AS CustomerName, SUM(i.Total) AS TotalSpent
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId
ORDER BY TotalSpent DESC
LIMIT 5;

---

Q: What is the most popular genre by track count?
SQL:
SELECT g.Name, COUNT(t.TrackId) AS TrackCount
FROM Track t
JOIN Genre g ON t.GenreId = g.GenreId
GROUP BY g.GenreId
ORDER BY TrackCount DESC
LIMIT 1;

---

Q: How much revenue was generated each month?
SQL:
SELECT strftime('%Y-%m', InvoiceDate) AS Month, SUM(Total) AS Revenue
FROM Invoice
GROUP BY Month
ORDER BY Month;

---

Q: Which employee manages the most customers?
SQL:
SELECT e.FirstName || ' ' || e.LastName AS RepName, COUNT(c.CustomerId) AS NumCustomers
FROM Customer c
JOIN Employee e ON c.SupportRepId = e.EmployeeId
GROUP BY e.EmployeeId
ORDER BY NumCustomers DESC
LIMIT 1;

---

Q: Which tracks appear in the most playlists?
SQL:
SELECT t.Name, COUNT(*) AS PlaylistCount
FROM PlaylistTrack pt
JOIN Track t ON pt.TrackId = t.TrackId
GROUP BY pt.TrackId
ORDER BY PlaylistCount DESC
LIMIT 5;
"""

# Combine all parts into one string
full_knowledge_base = "\n---\n[SCHEMA]\n\n" + "\n\n---\n".join(schema_json) + business_logic + sample_queries

# Save to a file
file_path = "RAG\chinook_knowledge_base.txt"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(full_knowledge_base)

file_path
