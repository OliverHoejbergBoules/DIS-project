from flask import Flask, render_template, request
from database import init_db, db_connection

init_db()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    selected = request.form.get('ticker', 'AAPL')

    # Regular expression validation: ticker must be 1-5 uppercase letters
    if not re.match(r'^[A-Z]{1,5}$', selected):
        return "Invalid ticker format", 400

    conn = db_connection()
    cur = conn.cursor()

    # Dropdown list of available tickers
    cur.execute("SELECT DISTINCT ticker FROM stock_prices ORDER BY ticker;")
    tickers = [row[0] for row in cur.fetchall()]

    # Only select ticker, date, close
    cur.execute("""
        SELECT ticker, date, close
        FROM stock_prices
        WHERE ticker = %s
        ORDER BY date DESC
        LIMIT 5
    """, (selected,))
    stocks = cur.fetchall()
    conn.close()

    # Extract data for chart
    dates = [str(row[1]) for row in reversed(stocks)]  # reverse for oldest to newest
    closes = [round(float(row[2]), 2) for row in reversed(stocks)]

    return render_template('stocks.html',
                           stocks=stocks,
                           tickers=tickers,
                           selected=selected,
                           dates=dates,
                           closes=closes)

if __name__ == '__main__':
    app.run(debug=True)
