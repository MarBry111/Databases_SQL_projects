from flask import Flask, flash, Markup
from flask import render_template
from flask import request

import pymssql

app = Flask(__name__)
app.secret_key = 'asrtarstaursdlarsn'

# connection data - not the safest option
user='SA'
password='Montenegro1!'
server='localhost:1433'
database='homework1'

# create connection
conn = pymssql.connect(server, user, password, database)
cursor = conn.cursor(as_dict=True)

cursor.execute('SELECT * FROM Games')

@app.route("/", methods=["GET", "POST"])
def home():
    cursor.execute(f'''
        SELECT *
        FROM Games''')
    
    games=cursor.fetchall()

    cursor.execute(f'''
        SELECT *
        FROM Orders''')
    
    orders=cursor.fetchall()

    return render_template("home.html", orders=orders, games=games)

@app.route("/add", methods=["GET", "POST"])
def add_order():
    cursor.execute(f'''
        SELECT *
        FROM Games''')
    
    games=cursor.fetchall()

    if request.form:
        game = request.form

        sql_query = f'''
            INSERT INTO Orders (ORDER_DATE, GAME_ID, NET_AMOUNT, DISCOUNT, GROSS_AMOUNT)
            SELECT
                CONVERT (date, GETDATE()),
                GAME_ID,
                PRICE,
                CASE 
                    WHEN DATEDIFF(year, RELEASE_DATE, CONVERT(date, GETDATE())) >= 3 THEN PRICE*0.2 
                    ELSE 0 END,
                CASE 
                    WHEN DATEDIFF(year, RELEASE_DATE, CONVERT(date, GETDATE())) >= 3 THEN PRICE*0.8*1.23 
                    ELSE PRICE*1.23 END
            FROM Games
            WHERE GAME_ID = {game['game_id']};'''

        cursor.execute(sql_query)
        conn.commit()

    cursor.execute(f'''
        SELECT *
        FROM Orders''')
    
    orders=cursor.fetchall()

    return render_template("home.html", orders=orders, games=games)

@app.route("/delete", methods=["GET", "POST"])
def delete_order():
    cursor.execute(f'''
        SELECT *
        FROM Games''')
    
    games=cursor.fetchall()

    if request.form:    
        game = request.form

        sql_query = f'''
            DELETE FROM Orders 
            WHERE ORDER_ID = {game['ORDER_ID']};'''

        cursor.execute(sql_query)
        conn.commit()

    cursor.execute(f'''
        SELECT *
        FROM Orders''')
    
    orders=cursor.fetchall()

    return render_template("home.html", orders=orders, games=games)


@app.route("/edit", methods=["GET", "POST"])
def edit_order():
    if request.form:    
        edit = request.form
        print(edit)

        cursor.execute(f'''
            SELECT *
            FROM Orders
            WHERE ORDER_ID = {edit['ORDER_ID']}''')
    
        order=cursor.fetchall()
        print(order)

    return render_template("edit.html", order=order[0])


@app.route("/evaluate", methods=["GET", "POST"])
def evaluate():
    if request.form:    
        edit = request.form

        try:
            cursor.execute(f'''
                EXEC UpdateOrderValues 
                    @ord_id = {edit['ORDER_ID']}, 
                    @ord_date = '{edit['ORDER_DATE']}', 
                    @g_id = {edit['GAME_ID']}, 
                    @net = {edit['NET_AMOUNT']}, 
                    @disc = {edit['DISCOUNT']}, 
                    @gross = {edit['GROSS_AMOUNT']};''')
            conn.commit()
        except (pymssql.IntegrityError, pymssql.OperationalError) as e:
            print('ERRROR')
            message = Markup("<h1>Wrong format of values or not existing game</h1>")
            flash(message)

    cursor.execute(f'''
        SELECT *
        FROM Games''')
    games=cursor.fetchall()

    cursor.execute(f'''
        SELECT *
        FROM Orders''')
    orders=cursor.fetchall()

    return render_template("home.html", orders=orders, games=games)

@app.route("/filter", methods=["GET", "POST"])
def filter():
    if request.form:    
        filtered = request.form

        try:
            cursor.execute(f'''
                EXEC ListGames
                    @s_dt='{filtered['START_DATE']}', 
                    @e_dt='{filtered['END_DATE']}', 
                    @phr='{filtered['PHRASE']}',
                    @min_s={filtered['MIN_SCORE']};''')
            games=cursor.fetchall()
        except (pymssql.IntegrityError, pymssql.OperationalError) as e:
            message_fitler = Markup("<h1>Wrong format of filter data</h1>")
            flash(message_fitler)

            cursor.execute(f'''
                SELECT *
                FROM Games''')
            games=cursor.fetchall()

    cursor.execute(f'''
        SELECT *
        FROM Orders''')
    orders=cursor.fetchall()

    return render_template("home.html", orders=orders, games=games)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)