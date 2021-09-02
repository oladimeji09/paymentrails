#@auto-fold regex /./
import json, hmac, hashlib, time, requests as r,sys,pandas as pd,names, json
from requests.auth import AuthBase
import env
baseURL = 'https://api.paymentrails.com/v1/'
api_key = env.paymentrails_api_key
secret_key= env.paymentrails_secret_key
#DOCS https://dashboard.paymentrails.com/docs
# Create custom authentication for Payment Rails API

class PaymentRailsAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        # print("PATH", request.path_url)
        timestamp = str(int(time.time()))
        message = '\n'.join([timestamp, request.method, request.path_url, (request.body or ''), ''])
        signature = hmac.new(bytes(self.secret_key, 'latin-1'), bytes(message, 'latin-1'), digestmod=hashlib.sha256).hexdigest()

        request.headers.update({
            'Authorization': 'prsign %s:%s' % (self.api_key, signature),
            'X-PR-Timestamp': timestamp,
        })

        # print(request.headers)
        return request

auth = PaymentRailsAuth(api_key, secret_key)

def create_recipient(payload):
    """Create recipients and return there id"""
    # payload = {"type": "individual", "firstName": "you", "lastName": "getme", "email": "yougetme@outlook.com"}
    resp = r.post(baseURL + 'recipients', auth=auth,data =payload)
    return resp.json().get('recipient') if resp.status_code == 200 else  resp.json().get('errors')

def list_recipient(search_term=''):
    """List all recipients, or use the search_term to search by name, email (username and domain-name) and referenceId"""
    list =[]
    resp = r.get(baseURL + 'recipients?&pageSize=1000&search={}'.format(search_term), auth=auth)
    page_limit = 1
    while page_limit < resp.json().get('meta').get('pages')+1   :
        print('Page ' +str(page_limit))
        resp = r.get(baseURL + 'recipients?&pageSize=1000&page={}&search={}'.format(page_limit,search_term), auth=auth)
        for item in resp.json().get('recipients'):
            list.append(item)
        page_limit += 1
    return list if resp.status_code == 200 else  resp.json().get('errors')

def delete_recipient(r_id):
    """Delete recipients and return True"""
    resp = r.delete(baseURL +'recipients/{}'.format(r_id), auth=auth)
    return resp.json().get('ok') if resp.status_code == 200 else  resp.json().get('errors')

def payments_recipient(r_id):
    """Retrieve payments to this recipient"""
    resp = r.get(baseURL +'recipients/{}/payments'.format(r_id), auth=auth)
    return resp.json().get('payments') if resp.status_code == 200 else  resp.json().get('errors')

def create_account(r_id,payload):
    """Create recipient account and return True"""
    # payload = {"type": "bank-transfer","currency": "GBP", "country": "GB","accountHolderName": "Oladimeji Olaolorun","accountNum": "43709442","branchId": "202748"}
    resp = r.post(baseURL +'recipients/{}/accounts'.format(r_id), auth=auth, data=payload)
    return resp.json().get('account') if resp.status_code == 200 else  resp.json().get('errors')

def get_account(r_id,a_id):
    """Retrieve a recipient’s payout method """
    resp = r.get(baseURL +'recipients/{}/accounts/{}'.format(r_id,a_id), auth=auth)
    return resp.json().get('account') if resp.status_code == 200 else  resp.json().get('errors')

def delete_account(r_id,a_id):
    """Delete recipients account and return True"""
    resp = r.delete(baseURL +'recipients/{}/accounts/{}'.format(r_id,a_id), auth=auth)
    return resp.json().get('ok') if resp.status_code == 200 else  resp.json().get('errors')

def create_batch(payload):
    """Create recipient batch payment"""
    # payload = {"amount": "65", "memo": "TESING", "currency": "GBP", "description": "new batch"}
    # payload = {"amount": "65", "memo": "TESING", "currency": "GBP", "description": "test", "payments[].": {"recipient": {"id": "R-MegD1T1zhQnFptKZkMGzJd", "amount":"3434"}}}
    resp = r.post(baseURL +'batches', auth=auth, data=payload)
    return resp.json().get('batch') if resp.status_code == 200 else  resp.json().get('errors')

def get_batch(b_id):
    """Retrieve recipients batch payment """
    resp = r.get(baseURL +'batches/{}'.format(b_id), auth=auth)
    return resp.json().get('batch') if resp.status_code == 200 else  resp.json().get('errors')

def delete_batch(b_id):
    """Retrieve recipients batch payment """
    resp = r.delete(baseURL +'batches/{}'.format(b_id), auth=auth)
    return resp.json().get('ok') if resp.status_code == 200 else  resp.json().get('errors')

def list_batch(search_term=''):
    """List all batches"""
    list =[]
    resp = r.get(baseURL + 'batches/?&pageSize=1000&search={}'.format(search_term), auth=auth)
    page_limit = 1
    while page_limit < resp.json().get('meta').get('pages')+1   :
        print('Page ' +str(page_limit))
        resp = r.get(baseURL + 'batches?&pageSize=1000&page={}&search={}'.format(page_limit,search_term), auth=auth)
        for item in resp.json().get('batches'):
            list.append(item)
        page_limit += 1
    return list if resp.status_code == 200 else  resp.json().get('errors')

def create_payment(b_id,payload): # TODO: not completed
    """Create recipient batch payment"""
    # payload ={"payments":[{"recipient":{"id": "R-MegD1T1zhQnFptKZkMGzJd"},"sourceAmount":"100.10","memo":"Freelance payment", "currency": "GBP"}]}
    # payload ={"payments":[{"recipient":{"id": r_id},"sourceAmount":"100.10","memo":"Freelance payment", "currency": "GBP"}]}
    # payload =  {"amount":"10","currency":"GBP","recipient":{"id":"R-MegD1T1zhQnFptKZkMGzJd"}}
    resp = r.post(baseURL +'batches/{}/payments'.format(b_id), auth=auth, data= payload)
    resp.json()
    return resp.json().get('batch') if resp.status_code == 200 else  resp.json().get('errors')

def get_payment(b_id,p_id):
    """Retrieve a payment"""
    resp = r.get(baseURL +'batches/{0}/payments/{1}'.format(b_id,p_id), auth=auth)
    return resp.json().get('payment') if resp.status_code == 200 else  resp.json().get('errors')

def delete_payment(b_id,p_id):
    """Delete a payment"""
    resp = r.delete(baseURL +'batches/{0}/payments/{1}'.format(b_id,p_id), auth=auth)
    return resp.json().get('ok') if resp.status_code == 200 else  resp.json().get('errors')

def list_payment(b_id,search_term=''):
    """List all payments within a batch"""
    list =[]
    resp = r.get(baseURL + 'batches/{}/payments?&pageSize=1000&search={}'.format(b_id,search_term), auth=auth)
    page_limit = 1
    while page_limit < resp.json().get('meta').get('pages')+1   :
        print('Page ' +str(page_limit))
        resp = r.get(baseURL + 'batches/{}/payments?&pageSize=1000&page={}&search={}'.format(b_id,page_limit,search_term), auth=auth)
        for item in resp.json().get('payments'):
            list.append(item)
        page_limit += 1
    return list if resp.status_code == 200 else  resp.json().get('errors')

def get_batch_fx(b_id):
    """Generate Quote of FX rates"""
    resp = r.post(baseURL +'batches/{}/generate-quote'.format(b_id), auth=auth)
    return resp.json().get('batch') if resp.status_code == 200 else  resp.json().get('errors')

def get_batch_summary(b_id):
    """Retrieve a payment"""
    resp = r.get(baseURL +'batches/{0}/summary'.format(b_id), auth=auth)
    return resp.json().get('batchSummary') if resp.status_code == 200 else  resp.json().get('errors')

def process_batch(b_id):
    """Process the batch"""
    resp = r.post(baseURL +'batches/{}/start-processing'.format(b_id), auth=auth)
    return resp.json().get('batch') if resp.status_code == 200 else  resp.json().get('errors')

# NOTE: testing
for i in range(600):
    firstName = names.get_first_name()
    lastName =names.get_last_name()
    payload = {"type": "individual", "firstName": firstName , "lastName": lastName, "email": "{}@outlook.com".format(firstName+lastName)}
    create_recipient(payload)
    time.sleep(1)
