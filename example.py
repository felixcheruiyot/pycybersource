from cybersource.processor import *

merchantid = ''
password = ''

payload = {"card": {}, "charge": {},
           "billing": {}, "reference": "INTASEND_ebaed2", "product_name": "Product 1"}
payload["card"]['account_number'] = '4187427415564246'
payload["card"]['exp_month'] = '06'
payload["card"]['exp_year'] = '2022'
payload["card"]['cvv'] = '111'

payload["charge"]['currency'] = 'KES'
payload["charge"]['total'] = 100

payload["billing"]['first_name'] = 'Felix'
payload["billing"]['last_name'] = 'Cheruiyot'
payload["billing"]['email'] = 'felix@intasend.com'
payload["billing"]['phone_number'] = '254723890353'

payload["billing"]['address1'] = 'Nairobi'
payload["billing"]['city'] = 'Nairobi'
payload["billing"]['state'] = 'Nairobi'
payload["billing"]['zipcode'] = '20001'
payload["billing"]['country'] = 'KE'
payload["billing"]['cid'] = 'INTASEND-91921'


if __name__ == "__main__":
    p = Processor(merchantid, password, test=True)
    resp = p.charge_card(payload=payload, ignore_avs=False,
                         xid="6Nv0XmVnFY5eY94YM2U0")
    print(f"Response>>>: {resp}")


# Docs
# Examples: https://developer.cybersource.com/library/documentation/dev_guides/apple_payments/SO_API/html/Topics/ch_soAPI.htm#XREF_25483_Merchant_Decryption
# Fields: https://developer.cybersource.com/library/documentation/dev_guides/apple_payments/SO_API/html/Topics/Request_Fields.htm
