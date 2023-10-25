from flask import *
import stripe

app = Flask(__name__)

# public_key = "pk_test_51MeMeOSBEtdxpnN2G8fTQDOO4UOCFatZ0toVvOvVq4mNNx6Rg7XRaUtH8Qzm7VWXv2sV67RKIabQD6WdtTkkqBw2006LEXbWZG"
# stripe.api_key = "sk_test_51MeMeOSBEtdxpnN223Iaz2eDxPDMOIW7iei6rYNBTlvUlCqTtsGY42igbyRJDlwfC7xBJHlXo8HLyO8avgI7oo1c00lhgMJhJo"

public_key = "pk_test_6pRNASCoBOKtIshFeQd4XMUh"
stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"


@app.route("/")
def index():
    return render_template("razor_payment.html", public_key=public_key)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/payment', methods=['POST'])
def payment():

    # CUSTOMER INFO
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    # PAYMENT INFO
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=1999, # 19.99
        currency='USD',
        description='Donation'
    )

    return redirect(url_for('thankyou'))

if __name__ == '__main__':
    app.run("0.0.0.0")

