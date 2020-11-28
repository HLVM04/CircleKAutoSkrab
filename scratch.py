import requests, json, argparse, os

phoneNumbersFile = 'phonenumbers.json'
headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41',
        'content-type': 'application/json',
        'Accept': '*/*',
        'Origin': 'https://skrab.circlek.one',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://skrab.circlek.one/',
        'Accept-Language': 'da,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,ko;q=0.6,de;q=0.5,no;q=0.4',
    }


def do2FA(phone_number):
    if len(phone_number) != 8:
        print("That's not a danish phone number")
        return "Error: That's not a danish phone number"

    data = '{"id":"L2ZyZ2d2YXRmL3F4X2ZyZ2d2YXRmLmN1Yw==","pid":"' + phone_number + '"}'
    response = requests.post('https://skrab.circlek.one/lib/php/login/twofactor.php', headers=headers, data=data)
    print(phone_number)
    print(response.json())
    return response.status_code


def addPhoneNumberWith2FACode(phone_number, tfa_code):
    data = '{"id":"L2ZyZ2d2YXRmL3F4X2ZyZ2d2YXRmLmN1Yw==","pid":"' + phone_number + '","permission":false,"referrer":"direct","device":{"brand":"Apple","model":"","browser":"Chrome","browser_version":"87.0","os":"Mac","os_version":"11.0"},"code":' + tfa_code + '}'
    response = requests.post('https://skrab.circlek.one/lib/php/login/login.php', headers=headers, data=data)
    if 'error' in response.json():
        print('Error: ' + response.json()['error'])
        return 'Error: ' + response.json()['error']

    cid = response.json()['cid']

    data = '{"id":"L2ZyZ2d2YXRmL3F4X2ZyZ2d2YXRmLmN1Yw==","cid":"' + cid + '"}'
    response = requests.post('https://skrab.circlek.one/lib/php/login/check_login.php', headers=headers, data=data)

    if response.json()['login']:
        if os.path.exists(phoneNumbersFile):
            with open(phoneNumbersFile, 'w+') as json_file:
                json_file.write(json.dumps({}))

        with open(phoneNumbersFile) as json_file:
            phone_numbers = json.load(json_file)

        phone_numbers.update({phone_number: cid})

        with open(phoneNumbersFile, 'w+') as json_file:
            json.dump(phone_numbers, json_file)
        
        print('Success adding ' + phone_number + ' with cid ' + cid + ' to database!')
        return 'Success'
    else:
        return 'Error: Failed login'


def addPhoneNumber(phone_number):
    if len(phone_number) != 8:
        print("That's not a danish phone number")
        return

    data = '{"id":"L2ZyZ2d2YXRmL3F4X2ZyZ2d2YXRmLmN1Yw==","pid":"' + phone_number + '"}'
    requests.post('https://skrab.circlek.one/lib/php/login/twofactor.php', headers=headers, data=data)

    tfaCode = str(input('Type your 2FA code from SMS: '))

    addPhoneNumberWith2FACode(phone_number, tfaCode)


def most_frequent(list):
    counter = 0
    num = list[0]
      
    for i in list:
        curr_frequency = list.count(i)
        if curr_frequency > counter:
            counter = curr_frequency 
            num = i 
  
    return num 


def scratchAll():
    with open(phoneNumbersFile) as json_file:
        phone_numbers = json.load(json_file)
    
    for phone_number, cid in phone_numbers.items():
        data = '{"id":"L2ZyZ2d2YXRmL3F4X2ZyZ2d2YXRmLmN1Yw==","cid":"' + cid + '","name":"scratch"}'
        response = requests.post('https://skrab.circlek.one/lib/php/scratch/start.php', headers=headers, data=data)

        if 'error' in response.json():
            print('Failed to scratch number: ' + phone_number)
            continue
        
        if not ('items' in response.json()):
            print('Phone number ' + phone_number + ' already scratched')
            continue

        sid = response.json()['sid']
        most_frequent_number = most_frequent(response.json()['items'])
        count = response.json()['items'].count(most_frequent_number)
        
        if count > 2:
            print("Phone number " + phone_number + " won!")
        else:
            print("Phone number " + phone_number + " did not win :(")

        data = '{"id":"L2ZyZ2d2YXRmL3F4X2ZyZ2d2YXRmLmN1Yw==","cid":"' + cid + '","name":"scratch","sid":"' + sid + '","time":1606217181}'
        response = requests.post('https://skrab.circlek.one/lib/php/scratch/end.php', headers=headers, data=data)

        if not response.json()['success']:
            print('Error ending the scratch :(')


def printNumbers():
    with open(phoneNumbersFile) as json_file:
        print(json.dumps(json.load(json_file), indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="hmm idk")
    parser.add_argument('-add', type=int)
    parser.add_argument('-showNumbers', action='store_true')
    parser.add_argument('-scratch', action='store_true')

    args = parser.parse_args()
    if args.add is not None:
        addPhoneNumber(str(args.add))
    
    if args.showNumbers:
        printNumbers()

    if args.scratch:
        scratchAll()
