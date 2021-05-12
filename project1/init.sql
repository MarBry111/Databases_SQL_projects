CREATE DATABASE homework1;

USE homework1;

CREATE TABLE Games (
    GAME_ID int NOT NULL PRIMARY KEY,
    GAME_NAME varchar(100) NOT NULL,
    RELEASE_DATE date NOT NULL,
    PRICE money NOT NULL,
    SCORE decimal NOT NULL
);

CREATE TABLE Orders (
    ORDER_ID INT IDENTITY NOT NULL PRIMARY KEY,
    ORDER_DATE date NOT NULL,
    GAME_ID int NOT NULL,
    NET_AMOUNT money NOT NULL,
    DISCOUNT decimal NULL,
    GROSS_AMOUNT money NOT NULL,
    CONSTRAINT fk_orders_games_id
        FOREIGN KEY (GAME_ID)
        REFERENCES Games (GAME_ID)
        ON DELETE CASCADE
);

INSERT INTO Games (GAME_ID, GAME_NAME, RELEASE_DATE, PRICE, SCORE)
VALUES 
    (1, 'Skyrim', '2015-01-01', 100, 5),
    (2, 'Cyberpunk', '2021-09-01', 180, 3),
    (3, 'Mario', '1970-03-10', 10, 10);


CREATE PROCEDURE UpdateOrderValues @ord_id int, @ord_date date, @g_id int, @net money, @disc decimal, @gross money
AS
    BEGIN
        UPDATE Orders 
        SET 
            ORDER_DATE = @ord_date,
            GAME_ID = @g_id,
            NET_AMOUNT = @net,
            DISCOUNT = @disc,
            GROSS_AMOUNT = @gross
        WHERE ORDER_ID=@ord_id
    END
    
CREATE PROCEDURE ListGames @s_dt date, @e_dt date, @phr varchar(100), @min_s decimal
AS
    BEGIN
        SELECT *
        FROM Games g 
        WHERE RELEASE_DATE BETWEEN @s_dt AND @e_dt
            AND GAME_NAME LIKE  CONCAT('%',@phr,'%')
            AND SCORE >= @min_s
    END
        