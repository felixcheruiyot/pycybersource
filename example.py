from cybersource.processor import *

password = '<YOUR-PASSWORD>'
merchantid = '<YOUR-MERCHANT-ID>'

payload = {"card": {}, "charge": {}, "billing": {}}
payload["card"]['account_number'] = '4242424242424242'
payload["card"]['exp_month'] = '05'
payload["card"]['exp_year'] = '2023'
payload["card"]['cvv'] = '123'

payload["charge"]['currency'] = 'USD'
payload["charge"]['total'] = 100.50

payload["billing"]['first_name'] = 'Felix'
payload["billing"]['last_name'] = 'Cheruiyot'
payload["billing"]['email'] = 'felix@intasend.com'
payload["billing"]['phone_number'] = '2747127050808'

payload["billing"]['address1'] = 'Nine Planets, Kahawa Wendani'
# payload["billing"]['address2'] = 'Bldg 1-100'
payload["billing"]['city'] = 'Nairobi'
payload["billing"]['state'] = 'Nairobi'
payload["billing"]['zipcode'] = '00100'
payload["billing"]['country'] = 'KE'
payload["billing"]['cid'] = '0123456789'


if __name__ == "__main__":
    p = Processor(merchantid, password, test=True)
    resp = p.charge_card(payload)
    print(f"Response>>>: {resp}")

    # Expected response example of returned successful message
    # {
    #     'merchantReferenceCode': '7',
    #     'requestID': '5965984446106112304012',
    #     'decision': 'ACCEPT',
    #     'reasonCode': 100,
    #     'requestToken': 'Axj/7wSTQ2qqjJfcayOMABEg3cM3Dhy1ZtIkGw5Z2myiOEcAnbQFRHCOATtukDp0IDZhk0ky9GLAdmiDCTQ2qqjJfcayOMAAGAYA',
    #     'purchaseTotals': {
    #         'currency': 'USD'
    #     },
    #     'ccAuthReply': {
    #         'reasonCode': 100,
    #         'amount': '100.50',
    #         'authorizationCode': '888888',
    #         'avsCode': '1',
    #         'cvCode': None,
    #         'authorizedDateTime': '2020-08-05T03:34:04Z',
    #         'processorResponse': '100',
    #         'reconciliationID': '783889534DAX93Z6',
    #         'paymentNetworkTransactionID': '123456789619999'
    #     },
    #     'card': {
    #         'cardType': '001'
    #     },
    #     'pos': {
    #         'terminalID': '111111'
    #     }
    # }
