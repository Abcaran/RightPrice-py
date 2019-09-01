import requests
from bs4 import BeautifulSoup
import smtplib

# This script currently only works for zoom webpages
url = 'ENTER PRODUCT PAGE FROM ZOOM'

# Enter the optimum price you desire
best_price = 2800


def check_price(best_price):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    product_name = soup.find(id='productInfo').find('span').get_text()
    price = float(soup.find('strong', {'class': 'price-label'}).attrs['value'])

    if price < best_price:
        message = (f"That is awesome! The price is only R${price}!\nIf you buy {product_name} now you are gona save R${best_price-price}.\n")
        print(message)
        send_mail(message, product_name)

    elif price == best_price:
        message = ("You've made it!\nThe price is right where you wanted it! Buy now for R${price}.\n")
        print(message)
        send_mail(message, product_name)
    else:
        message = (f"Unfortunately it's not time to buy {product_name} yet!\nThe price is R${price}, R${price-best_price} more than you wanted to pay.\n")
        print(message)


def send_mail(message, product_name):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    user_email = 'ENTER YOUR EMAIL'
    user_password = 'ENTER PASSWORD FOR EMAIL'

    server.login(user_email, user_password)

    subject = f'PRICE ALERT {product_name}'
    body = message + f'\nCheck the link: {url}'

    email_msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(
        from_addr=user_email,
        to_addrs=user_email,
        msg=email_msg
    )
    print('The email has been sent!')
    server.quit()

check_price(best_price)