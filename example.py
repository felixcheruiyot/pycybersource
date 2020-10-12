from cybersource.processor import *

merchantid = 'ecomr005134'
password = 'f5atiK3mC734nUTTR9mUEZX0QuEtvI0nVXjQtUSG9KQWI8yUWktTppATkD/5/E+Y6S0DD0I9GK9tCNk3dZcI1/80tvgxSUFurLwEbp4/guEiXM5uNgSJO7SZXz8COmD9sujgfVCpX8f1COoLCbNwBaa5GkgyRvbePnvWN4J/BgsljFczjrGom0LOL/aAGpN9ycCvedSVYP9T/yr19CMPFo/spdc2KuwjJPdTmkHYmuub/FJqBXotoa/oHnJdGZu/xl/2XK9pVVBaTagJ++/AtFWzfZDCJq6hyqp7+jH5ItJdhVmCB9IIRljljLYhZ60qWvAgzZa88NfUozR9uiDZSw=='

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
