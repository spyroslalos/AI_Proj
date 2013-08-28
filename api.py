import os, sys, cookielib, requests
from tsDB.settings import BASE_REQ_URL


CA_BUNDLE = '/etc/pki/tls/certs/CERN-bundle.pem'
COOKIE_FILE = '/home/lalos/ssocookie.txt'

def query_batchmon(url=BASE_REQ_URL, params={}):
    os.environ['REQUESTS_CA_BUNDLE'] = CA_BUNDLE
    cj = cookielib.MozillaCookieJar(COOKIE_FILE)
    
    cj.load()
    r = requests.get(url, params=params, verify=False, cookies=cj)
    
    # Let's parse the output and translate it to an list of lists [ [column1, column2,...], [...], ... ]
    results = r.text.strip().split('\n')
    # convert from unicode to utf-8
    results = map(lambda x: x.encode('UTF-8'), results)
    # split lines into columns (another array)
    results = map(str.split, results)
    
    return results

if __name__ == "__main__":
    # Temporary solution to generate cookie
    
    if os.system("cern-get-sso-cookie --nocertverify --krb -u https://batchmon-tsd.cern.ch -o ~/ssocookie.txt -r ") != 0:
        os.system("kinit slalos@CERN.CH")
        if os.system("cern-get-sso-cookie --nocertverify --krb -u https://batchmon-tsd.cern.ch -o ~/ssocookie.txt -r ") != 0:
            print "Error running cern-get-sso-cookie. Try kinit."
        sys.exit(1)
           
    print query_batchmon('https://batchmon-tsd.cern.ch/q?start=1w-ago&m=sum:batchhosts.count&nocache&ascii') 
