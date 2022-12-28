import paypalrestsdk
import stripe


class Paypal():
  def __init__(self):
    self.payment = paypalrestsdk.Payment

  def setup_paypal(self):
    # Set up the PayPal API credentials
    paypalrestsdk.configure({
      "mode": "sandbox", # sandbox or live
      "client_id": "YOUR_CLIENT_ID",
      "client_secret": "YOUR_CLIENT_SECRET"
    })

  def set_payment_details(self):
    # Set the payment details
    self.payment = paypalrestsdk.Payment({
      "intent": "sale",
      "payer": {
        "payment_method": "paypal" # or "credit_card"
      },
      "transactions": [{
        "amount": {
          "total": "10.00",
          "currency": "USD"
        },
        "description": "Payment for goods or services"
      }]
    })

  def create_payment(self):
    # Create the payment
    self.setup_paypal()
    self.set_payment_details()

    if self.payment.create():
      print("Payment successful!")
    else:
      print("Error:", payment.error)




class CardPayment():
  def __init__(self):
    self.payment_method = "card"
    self.amount = 10
    self.currency = "usd"
    self.description = "Payment for JVD downloader."
    pass

  def setup_credentials(self):
    # Set up the Stripe API credentials
    stripe.api_key = "YOUR_SECRET_KEY"

  def setup_payment_details(self):
    # Set up the payment details
    self.payment_method = "card" # or "card"
    self.amount = 1000 # amount in cents
    self.currency = "usd"
    self.description = "Payment for goods or services"

  def create_payment(self):
    self.setup_credentials()
    self.setup_payment_details()

    # Create the payment
    try:
      self.payment = stripe.Charge.create(
        amount=self.amount,
        currency=self.currency,
        description=self.description,
        payment_method=self.payment_method,
      )
      print("Payment successful!")
    except Exception as e:
      print("Error:", e)


pay = Paypal()
pay.create_payment()