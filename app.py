from flask import Flask, render_template, request
from server import analyzeStock #imports function for stock analysis from server.py

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', results=None, symbol=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    symbol = request.form['symbol'].upper()

    try:
        results = analyzeStock(symbol)
        return render_template('index.html', results=results, symbol=symbol)


    except Exception as e:
        error_message = f"Error analyzing stock {symbol}: {str(e)}"
        return render_template('index.html', results=None, symbol=symbol, error=error_message)
    


if __name__ == '__main__':
    app.run(debug=True)