import base64


api_key = '0bba93a2'  # Your API key from Vonage
api_secret = '1dECQaSlgmqJ0s4H'  # Your API secret from Vonage


encoded_credentials = base64.b64encode(f"{api_key}:{api_secret}".encode('utf-8')).decode('utf-8')
authorization_header = f"Basic {encoded_credentials}"


print(authorization_header)