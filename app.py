# Python модули
from flask import Flask, render_template, request

import requests


# Переменные
app = Flask(__name__)

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"


def get_exchange_rates():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data["rates"]
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении курсов валют: {e}")
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    rates = get_exchange_rates()
    if rates is None:
        error = "Не удалось загрузить курсы валют. Попробуйте позже."
        return render_template("index.html", error=error)

    currencies = list(rates.keys())  # Список доступных валют

    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            from_currency = request.form["from_currency"]
            to_currency = request.form["to_currency"]

            # Конвертация
            if from_currency != "USD":
                amount_in_usd = amount / rates[from_currency]
            else:
                amount_in_usd = amount

            if to_currency != "USD":
                result = amount_in_usd * rates[to_currency]
            else:
                result = amount_in_usd

            result = round(result, 2)
            return render_template(
                "index.html",
                currencies=currencies,
                result=result,
                amount=amount,
                from_currency=from_currency,
                to_currency=to_currency
            )
        except (ValueError, KeyError):
            error = "Ошибка ввода данных. Проверьте введенные значения."
            return render_template("index.html", currencies=currencies, error=error)

    return render_template("index.html", currencies=currencies)


if __name__ == "__main__":
    app.run(debug=True)
