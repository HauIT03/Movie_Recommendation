CREATE DATABASE MovieRecommendation
USE MovieRecommendation

CREATE TABLE Movies (
    MovieID INT PRIMARY KEY,
    Title NVARCHAR(255),
    Genre NVARCHAR(255)
);

CREATE TABLE Users (
    UserId INT PRIMARY KEY,
);

CREATE TABLE Ratings (
    UserID INT,
    MovieID INT,
    Rating FLOAT,
    Timestamp INT
	PRIMARY KEY( UserID, MovieID),
	FOREIGN KEY (MovieID) REFERENCES Movies(MovieID),
	FOREIGN KEY (UserId) REFERENCES Users(UserId)
);

CREATE TABLE Tags (
    UserID INT,
    MovieID INT,
    Tag NVARCHAR(255),
    Timestamp INT

	FOREIGN KEY (MovieID) REFERENCES Movies(MovieID),
	FOREIGN KEY (UserId) REFERENCES Users(UserId)
)

--thêm dữ liệu vào các bảng từ file csv
BULK INSERT Movies
FROM 'D:\doannganh\MovieData\movies.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',', 
    ROWTERMINATOR = '\n',
    TABLOCK
);

BULK INSERT Ratings
FROM 'D:\doannganh\MovieData\ratings.csv'
WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', FIRSTROW = 2);

BULK INSERT Tags
FROM 'D:\doannganh\MovieData\tags.csv'
WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', FIRSTROW = 2);

UPDATE Movies
SET Title = REPLACE(Title, '"', '');

--UPDATE movies
--SET Title = 
--    CASE
--        WHEN LEFT(Title, 1) = '"' AND RIGHT(Title, 1) = '"' THEN SUBSTRING(Title, 2, LEN(Title) - 2)
--        ELSE Title
--    END
--WHERE LEFT(Title, 1) = '"' AND RIGHT(Title, 1) = '"';

--Xữ lý dữ liệu trong bảng Ratings
SELECT 
    Timestamp, 
    DATEADD(SECOND, Timestamp, '1970-01-01') AS DateTimeConverted
FROM Ratings;

ALTER TABLE Ratings
ADD DateTimeConverted DATETIME;

UPDATE Ratings
SET DateTimeConverted = DATEADD(SECOND, Timestamp, '1970-01-01');

ALTER TABLE Ratings
DROP COLUMN Timestamp;

EXEC sp_rename 'Ratings.DateTimeConverted', 'Timestamp', 'COLUMN';

--Xữ lý dữ liệu trong bảng Tags
SELECT 
    Timestamp, 
    DATEADD(SECOND, Timestamp, '1970-01-01') AS DateTimeConverted
FROM Tags;

ALTER TABLE Tags
ADD DateTimeConverted DATETIME;

UPDATE Tags
SET DateTimeConverted = DATEADD(SECOND, Timestamp, '1970-01-01');

ALTER TABLE Tags
DROP COLUMN Timestamp;

EXEC sp_rename 'Tags.DateTimeConverted', 'Timestamp', 'COLUMN';

--Xử lý các dữ liệu trong bảng USer
INSERT INTO Users (UserId)
SELECT DISTINCT UserId
FROM Ratings;

ALTER TABLE Users ADD UserName NVARCHAR(255);

UPDATE Users
SET UserName = 'User' + CAST(UserId AS NVARCHAR);

SELECT * FROM Movies WHERE MovieID IS NULL OR Title IS NULL OR Genre IS NULL;
DELETE FROM Movies WHERE MovieID IS NULL OR Title IS NULL OR Genre IS NULL;

SELECT * FROM Ratings WHERE UserID IS NULL OR MovieID IS NULL OR Rating IS NULL OR Timestamp IS NULL;
DELETE FROM Ratings WHERE UserID IS NULL OR MovieID IS NULL OR Rating IS NULL OR Timestamp IS NULL;

SELECT * FROM Tags WHERE UserID IS NULL OR MovieID IS NULL OR Tag IS NULL OR Timestamp IS NULL;
DELETE FROM Tags WHERE UserID IS NULL OR MovieID IS NULL OR Tag IS NULL OR Timestamp IS NULL;


select * from [dbo].[Movies]
select * from [dbo].[Ratings]
select * from[dbo].[Users]
select * from [dbo].[Tags]