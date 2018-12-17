import requests

class HttpRequest:
    name = 'xml_soap'

    def execute(case, args):
        print(case)
        #r = requests.post(args['url'])
