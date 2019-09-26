import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText


def parse_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup


def check_price(best_price, url):
    html_page = parse_html(url)

    product_name = html_page.find(id='productInfo').find('span').get_text()
    price = float(html_page.find('strong', {'class': 'price-label'}).attrs['value'])
    sellers = html_page.select('li.offers-list__offer')
    seller_info = []

    for seller in sellers:
        seller_name = seller.find('div', {'class': 'col-store'}).find('a').attrs['title']
        seller_price_parcels = seller.find('div', {'class': 'col-pricing pricing'}).text.strip()
        seller_link = seller.find('div', {'class': 'col-pricing pricing'}).find('a').attrs['href']

        info = {
            'seller_name': seller_name[3:],
            'seller_price_parcels': seller_price_parcels,
            'seller_link': seller_link,
            }

        seller_info.append(dict(info))

    item_info = {
        'product_name': product_name,
        'url': url,
        'lojas': seller_info,
    }

    if price < best_price:
        message = (f"That is awesome! The price is only R${price}!\nIf you buy {product_name} now you are gona save <b>R${best_price-price}</b>.\n")
        send_mail(message, item_info)

    elif price == best_price:
        message = ("You've made it!\nThe price is right where you wanted it! Buy now for R${price}.\n")
        send_mail(message, item_info)
    else:
        message = (f"Unfortunately it's not time to buy {product_name} yet!\nThe price is R${price}, R${price-best_price} more than you wanted to pay.\n")


def send_mail(message, item_info):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    user_email = 'ENTER YOUR EMAIL'
    user_password = "ENTER YOUR EMAIL'S PASSWORD"

    server.login(user_email, user_password)

    product_name = item_info['product_name']
    url = item_info['url']

    subject = f'PRICE ALERT {product_name}'
    body = message + f'\nCheck the link: {url}'
    items_list = ''

    for item in item_info['lojas']:
        seller_name = item['seller_name'].upper()
        price_parcels = item['seller_price_parcels']
        seller_link = item['seller_link']
        item = f'<dt><b>{seller_name}</b> - <b>{price_parcels}<b></dt><dd>{seller_link}</dd><br>'
        items_list += item

    msg = f"""
    <html>
        <body>
            <h2> PRICE ALERT</h2> 
            <h3><b>{product_name}</b></h3>
            <p><b>{message}</b></p>
            <p>
            <a href='{url}'>Product preview!</a>
            </p>
            <dl>{items_list}</dl>
        </body>
    </html>
    """
    email_content = MIMEText(msg, 'html', 'utf-8')

    server.sendmail(
        from_addr=user_email,
        to_addrs=user_email,
        msg=email_content.as_string()
    )
    server.quit()


def main():
# This script currently only works for zoom webpages
    url = 'ENTER YOUR ZOOM PRODUCT URL'

# Enter the optimum price you desire in reais (R$)
    best_price = 'ENTER YOUR DESIRED PRICE WITHOUT "'"'
    check_price(best_price=best_price, url=url)

main()