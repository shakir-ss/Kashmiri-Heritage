from twilio.rest import Client
from flask import current_app

class MessagingService:
    @staticmethod
    def send_order_confirmation(to_phone, order_id, total_amount):
        """
        Sends notifications to customer and admin.
        """
        # --- ADMIN ALERT ---
        print("\n" + "="*50)
        print(f"🚨 ADMIN ALERT: NEW ORDER PLACED! 🚨")
        print(f"Order ID: #{order_id}")
        print(f"Amount:   ₹{total_amount}")
        print(f"Customer: {to_phone}")
        print("="*50 + "\n")

        try:
            account_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
            auth_token = current_app.config['TWILIO_AUTH_TOKEN']
            from_phone = current_app.config['TWILIO_PHONE_NUMBER'] # e.g. 'whatsapp:+14155238886'

            if not all([account_sid, auth_token, from_phone]):
                print(f"Skipping WhatsApp: Twilio config missing for Order #{order_id}")
                return False

            client = Client(account_sid, auth_token)
            
            message = client.messages.create(
                from_=from_phone,
                body=f"Salam! Your Order #{order_id} for Kashmiri Heritage (Total: ₹{total_amount}) has been placed. We'll notify you when it's shipped!",
                to=f"whatsapp:{to_phone}"
            )
            return message.sid
        except Exception as e:
            print(f"Error sending WhatsApp: {e}")
            return False
