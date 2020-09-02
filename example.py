from cybersource.processor import *

password = ''
merchantid = ''

payload = {"card": {}, "charge": {},
           "billing": {}, "reference": "INTASKEINV_O2"}
payload["card"]['account_number'] = '4242424242424242'
payload["card"]['exp_month'] = '05'
payload["card"]['exp_year'] = '2023'
payload["card"]['cvv'] = '123'

payload["charge"]['currency'] = 'KES'
payload["charge"]['total'] = 1000

payload["billing"]['first_name'] = 'Felix'
payload["billing"]['last_name'] = 'Cheruiyot'
payload["billing"]['email'] = 'felix@intasend.com'
payload["billing"]['phone_number'] = '2747127050808'

payload["billing"]['address1'] = 'Nine Planets, Kahawa Wendani'
# payload["billing"]['address2'] = 'Bldg 1-100'
payload["billing"]['city'] = 'Nairobi'
# payload["billing"]['state'] = 'Nairobi'
# payload["billing"]['zipcode'] = '00100'
payload["billing"]['country'] = 'KE'
payload["billing"]['cid'] = '0123456789'


if __name__ == "__main__":
    p = Processor(merchantid, password, test=True)
    resp = p.charge_card(payload)
    print(f"Response>>>: {resp}")
