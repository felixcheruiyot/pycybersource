import suds
from suds.client import Client
from suds.sax.attribute import Attribute
from suds.sax.element import Element

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.ERROR)


class CyberSourceBaseException(Exception):
    def __init__(self, error_code, value):
        self.error_code = error_code
        self.value = value

    def __unicode__(self):
        return "{0} (Error code: {1})".format(repr(self.value), self.error_code)

    def __str__(self):
        return self.__unicode__()


class CyberSourceError(CyberSourceBaseException):
    pass


class CyberScourceFailure(CyberSourceBaseException):
    pass


class SchemaValidationError(CyberSourceBaseException):
    def __init(self):
        self.error_code = -1
        self.value = "suds encountered an error validating your data against this service's WSDL schema. Please double-check for missing or invalid values, filling all required fields."


CYBERSOURCE_RESPONSES = {
    '100': 'Successful transaction',
    '101': 'The request is missing one or more required fields',
    '102': 'One or more fields in the request contains invalid data',
    '104': 'The merchantReferenceCode sent with this authorization request matches the merchantReferenceCode of another authorization request that you sent in the last 15 minutes',
    '110': 'Only a partial amount was approved',
    '150': 'We could not complete your request because of a general system failure. Please contact your bank to enable online payments using the card or try with a different card',
    '151': 'Error: The request was received but there was a server timeout. This error does not include timeouts between the client and the server',
    '152': 'Error: The request was received, but a service did not finish running in time',
    '201': 'The issuing bank has questions about the request. You do not receive an authorization code in the reply message, but you might receive one verbally by calling the processor',
    '202': 'Expired card. You might also receive this if the expiration date you provided does not match the date the issuing bank has on file',
    '203': 'We could not complete your request because of a general decline response by your issuing bank. Please contact your bank to help resolve the issue and then retry again',
    '204': 'We could not complete your request because of insufficient funds in the account',
    '205': 'Stolen or lost card',
    '207': 'Issuing bank unavailable',
    '208': 'Inactive card or card not authorized for card-not-present transactions',
    '209': 'Invalid card details',
    '200': 'The authorization request was approved by the issuing bank but declined by processor because it did not pass the Address Verification System (AVS) check. ',
    '210': 'The card has reached the credit limit. ',
    '211': 'Invalid card verification number',
    '213': 'We cannot process the transaction. Account is in fraud watch status. Please contact your bank',
    '221': 'The customer matched an entry on the processor\'s negative file',
    '230': 'The authorization request was approved by the issuing bank but declined by CyberSource because it did not pass the CVN check',
    '231': 'Invalid account number',
    '232': 'The card type is not accepted by the payment processor',
    '233': 'General decline by the processor',
    '234': 'There is a problem with your CyberSource merchant configuration',
    '235': 'The requested amount exceeds the originally authorized amount. Occurs, for example, if you try to capture an amount larger than the original authorization amount. This reason code only applies if you are processing a capture through the API',
    '236': 'Processor Failure',
    '238': 'The authorization has already been captured. This reason code only applies if you are processing a capture through the API',
    '239': 'The requested transaction amount must match the previous transaction amount. This reason code only applies if you are processing a capture or credit through the API',
    '240': 'The card type sent is invalid or does not correlate with the credit card number',
    '241': 'The request ID is invalid. This reason code only applies when you are processing a capture or credit through the API',
    '242': 'You requested a capture through the API, but there is no corresponding, unused authorization record. Occurs if there was not a previously successful authorization request or if the previously successful authorization has already been used by another capture request. This reason code only applies when you are processing a capture through the API',
    '243': 'The transaction has already been settled or reversed',
    '246': 'The capture or credit is not voidable because the capture or credit information has already been submitted to your processor. Or, you requested a void for a type of transaction that cannot be voided. This reason code applies only if you are processing a void through the API',
    '247': 'You requested a credit for a capture that was previously voided. This reason code applies only if you are processing a void through the API',
    '250': 'Error: The request was received, but there was a timeout at the payment processor',
    '251': 'The customer has exceeded the debit cards limit on frequency of use, number of PIN entry tries, or maximum amount for the day. Request a different card or other form of payment',
    '252': 'The card cannot be used for PINless debit transactions. Request a different card or other form of payment',
    '254': 'Stand-alone credits are not allowed',
    '262': 'The request is still in progress. Wait for a response from processor',
    '263': 'Mass transit transaction (MTT) was declined. When the transaction amount is less than the transit chargeback threshold, and the other mandated checks are performed, you can capture the authorization. Your acquirer can provide information about mandated checks and transit chargeback thresholds. ',
    '476': 'We could not authenticate your request. Please retry again and ensure your enter the right one-time password sent by your bank. If you have any issue receiving this password, please contact your issuing bank',
    '478': 'Strong customer authentication (SCA) is required for this transaction',
    '481': 'Payment authentication failed. Please contact your issuing bank to enable 3D support for your card if not yet available',
    '520': 'The authorization request was approved by the issuing bank but declined by processor based on your Smart Authorization settings',
}

class Processor(object):

    def __init__(self, merchantid, password, certificate=None, private_key=None, test=False):
        service_url = 'https://ics2wsa.ic3.com/commerce/1.x/transactionProcessor/CyberSourceTransaction_1.181.wsdl'
        if test:
            service_url = 'https://ics2wstesta.ic3.com/commerce/1.x/transactionProcessor/CyberSourceTransaction_1.181.wsdl'
        self.client = Client(service_url)

        self.password = password
        self.merchantid = merchantid

    def create_headers(self):
        wssens = (
            'wsse', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd')
        mustAttribute = Attribute('SOAP-ENV:mustUnderstand', '1')

        security = Element('Security', ns=wssens)
        security.append(mustAttribute)
        security.append(Attribute(
            'xmlns:wsse', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd'))

        usernametoken = Element('UsernameToken', ns=wssens)

        username = Element('Username', ns=wssens).setText(self.merchantid)

        passwordType = Attribute(
            'Type', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wssusername-token-profile-1.0#PasswordText')
        password = Element('Password', ns=wssens).setText(self.password)
        password.append(passwordType)

        usernametoken.append(username)
        usernametoken.append(password)

        security.append(usernametoken)

        self.client.set_options(soapheaders=security)

    def sales_items(self, charge, reference, product_name="Service Fee"):
        self.item = self.client.factory.create('ns0:item')
        self.item._id = 0
        self.item.unitPrice = charge.get('total')
        self.item.quantity = 1
        self.item.productName = product_name
        self.item.referenceData_1_number = reference
        self.item.referenceData_1_code = "ISRef"

    def set_payment_amount(self, charge):
        '''
            currency = None
            discountAmount = None
            taxAmount = None
            dutyAmount = None
            grandTotalAmount = None
            freightAmount = None
            foreignAmount = None
            foreignCurrency = None
            exchangeRate = None
            exchangeRateTimeStamp = None
            additionalAmountType0 = None
            additionalAmount0 = None
            additionalAmountType1 = None
            additionalAmount1 = None
            additionalAmountType2 = None
            additionalAmount2 = None
            additionalAmountType3 = None
            additionalAmount3 = None
            additionalAmountType4 = None
            additionalAmount4 = None
            serviceFeeAmount = None
        '''

        currency = charge.get('currency')
        grandTotalAmount = charge.get('total')

        self.payment = self.client.factory.create('ns0:PurchaseTotals')
        self.payment.currency = currency
        self.payment.grandTotalAmount = grandTotalAmount

    def set_card_info(self, card_details):
        '''
            fullName = None
            accountNumber = None
            expirationMonth = None
            expirationYear = None
            cvIndicator = None
            cvNumber = None
            cardType = None
            issueNumber = None
            startMonth = None
            startYear = None
            pin = None
            accountEncoderID = None
            bin = None
        '''
        accountNumber = card_details.get('account_number')
        expirationMonth = card_details.get('exp_month')
        expirationYear = card_details.get('exp_year')
        cvNumber = card_details.get('cvv')

        if not all([accountNumber, expirationMonth, expirationYear, cvNumber]):
            raise CyberSourceError(
                '', 'Not all credit card info was gathered')

        self.card = self.client.factory.create('ns0:Card')

        self.card.accountNumber = accountNumber
        self.card.expirationMonth = expirationMonth
        self.card.expirationYear = expirationYear

    def billing_info(self, details):
        '''
            title = None
            firstName = None
            middleName = None
            lastName = None
            suffix = None
            buildingNumber = None
            street1 = None
            street2 = None
            street3 = None
            street4 = None
            city = None
            county = None
            state = None
            postalCode = None
            country = None
            company = None
            companyTaxID = None
            phoneNumber = None
            email = None
            ipAddress = None
            customerPassword = None
            ipNetworkAddress = None
            hostname = None
            domainName = None
            dateOfBirth = None
            driversLicenseNumber = None
            driversLicenseState = None
            ssn = None
            customerID = None
            httpBrowserType = None
            httpBrowserEmail = None
            httpBrowserCookiesAccepted = None
            nif = None
            personalID = None
            language = None
            name = None
        '''
        title = details.get('title')
        firstName = details.get('first_name')
        lastName = details.get('last_name')
        street1 = details.get('address1')
        street2 = details.get('address2')
        city = details.get('city')
        state = details.get('state')
        postalCode = details.get('zipcode')
        country = details.get('country', 'US')
        customerID = details.get('cid')
        email = details.get('email')
        phoneNumber = details.get('phone_number')

        self.bill_to = self.client.factory.create('ns0:BillTo')

        self.bill_to.title = title
        self.bill_to.firstName = firstName
        self.bill_to.lastName = lastName
        self.bill_to.street1 = street1
        self.bill_to.street2 = street2
        self.bill_to.city = city
        self.bill_to.state = state
        self.bill_to.postalCode = postalCode
        self.bill_to.country = country
        self.bill_to.customerID = customerID
        self.bill_to.email = email
        self.bill_to.phoneNumber = phoneNumber

    def check_response_for_cybersource_error(self, enrollment_check=False):
        if self.response.reasonCode != 100 and not enrollment_check:
            raise CyberSourceError(self.response.reasonCode,
                                   CYBERSOURCE_RESPONSES.get(str(self.response.reasonCode), 'Unknown Failure'))
        if enrollment_check and self.response.reasonCode not in [100, 475]:
            raise CyberSourceError(self.response.reasonCode,
                                   CYBERSOURCE_RESPONSES.get(str(self.response.reasonCode), 'Unknown Failure'))

    def set_default_options(self, payload):
        reference = payload.get('reference')
        product_name = payload.get("product_name")
        self.check = None
        self.create_headers()
        self.set_card_info(payload.get("card"))
        self.create_headers()
        self.set_payment_amount(payload.get("charge"))
        self.sales_items(payload.get("charge"), reference, product_name)
        self.set_card_info(payload.get("card"))
        self.billing_info(payload.get("billing"))

        options = dict(
            merchantID=self.merchantid,
            merchantReferenceCode=reference,
            billTo=self.bill_to,
            purchaseTotals=self.payment,
            item=self.item
        )

        if payload.get("invoiceHeader"):
            invoiceHeaderPayload = payload.get("invoiceHeader")
            invoiceHeader = self.client.factory.create('ns0:invoiceHeader')
            invoiceHeader.submerchantID = invoiceHeaderPayload.get(
                "submerchantID")
            invoiceHeader.salesOrganizationID = invoiceHeaderPayload.get(
                "salesOrganizationID")
            invoiceHeader.merchantDescriptor = invoiceHeaderPayload.get(
                "merchantDescriptor")
            invoiceHeader.merchantDescriptorCity = invoiceHeaderPayload.get(
                "merchantDescriptorCity")
            invoiceHeader.merchantDescriptorContact = invoiceHeaderPayload.get(
                "merchantDescriptorContact")
            invoiceHeader.merchantDescriptorCountry = invoiceHeaderPayload.get(
                "merchantDescriptorCountry")
            invoiceHeader.merchantDescriptorPostalCode = invoiceHeaderPayload.get(
                "merchantDescriptorPostalCode")
            invoiceHeader.merchantDescriptorStreet = invoiceHeaderPayload.get(
                "merchantDescriptorStreet")
            options["invoiceHeader"] = invoiceHeader
        if payload.get("mcc"):
            options["merchantCategoryCode"] = payload.get("mcc")
        if payload.get("deviceFingerprintID"):
            options["deviceFingerprintID"] = payload.get("deviceFingerprintID")

        return options

    def payer_authentication_setup(self, payload):
        """
        Payer authentication setup - 3Ds 2.x step 1
        """
        try:
            options = self.set_default_options(payload)
            payerAuthSetupService = self.client.factory.create(
                'ns0:payerAuthSetupService')
            payerAuthSetupService._run = "true"
            options['payerAuthSetupService'] = payerAuthSetupService
            options['card'] = self.card
            self.response = self.client.service.runTransaction(**options)
        except suds.WebFault as ex:
            raise SchemaValidationError('500', str(ex))

        self.check_response_for_cybersource_error()
        return self.obj_to_dict(self.response)

    def check_enrollment(self, payload):
        try:
            options = self.set_default_options(payload)
            ccAuthService = self.client.factory.create(
                'ns0:ccAuthService')
            if payload.get("aggregatorID"):
                ccAuthService.aggregatorID = payload.get("aggregatorID")
            ccAuthService._run = "true"
            options['ccAuthService'] = ccAuthService

            payerAuthEnrollService = self.client.factory.create(
                'ns0:payerAuthEnrollService')
            payerAuthEnrollService.referenceID = payload.get(
                "payerAuthEnrollRefID")
            if payload.get("invoiceHeader"):
                if payload.get("invoiceHeader").get("merchantDescriptor"):
                    payerAuthEnrollService.merchantName = payload.get(
                        "invoiceHeader").get("merchantDescriptor")
            if payload.get("mcc"):
                payerAuthEnrollService.MCC = payload.get("mcc")
            payerAuthEnrollService._run = "true"
            options['payerAuthEnrollService'] = payerAuthEnrollService

            ccCaptureService = self.client.factory.create(
                'ns0:ccCaptureService')
            ccCaptureService._run = "true"
            options['ccCaptureService'] = ccCaptureService

            options['card'] = self.card
            self.response = self.client.service.runTransaction(**options)
        except suds.WebFault as ex:
            raise SchemaValidationError('500', str(ex))

        self.check_response_for_cybersource_error(enrollment_check=True)
        return self.obj_to_dict(self.response)

    def checkout(self, payload):
        try:
            options = self.set_default_options(payload)
            ccAuthService = self.client.factory.create(
                'ns0:ccAuthService')
            if payload.get("aggregatorID"):
                ccAuthService.aggregatorID = payload.get("aggregatorID")
            ccAuthService._run = "true"
            options['ccAuthService'] = ccAuthService

            payerAuthValidateService = self.client.factory.create(
                'ns0:payerAuthValidateService')
            payerAuthValidateService.authenticationTransactionID = payload.get(
                "authenticationTransactionID")
            payerAuthValidateService._run = "true"
            options['payerAuthValidateService'] = payerAuthValidateService

            ccCaptureService = self.client.factory.create(
                'ns0:ccCaptureService')
            ccCaptureService._run = "true"
            options['ccCaptureService'] = ccCaptureService

            options['card'] = self.card
            self.response = self.client.service.runTransaction(**options)
        except suds.WebFault as ex:
            raise SchemaValidationError('500', str(ex))

        self.check_response_for_cybersource_error()
        return self.obj_to_dict(self.response)

    def obj_to_dict(self, obj):
        """
        Read objects and return dictionary version of the same
        """
        if not hasattr(obj, "__dict__"):
            return obj
        result = {}
        for key, val in obj.__dict__.items():
            if key.startswith("_"):
                continue
            element = []
            if isinstance(val, list):
                for item in val:
                    element.append(self.obj_to_dict(item))
            else:
                element = self.obj_to_dict(val)
            result[key] = element
        return result
