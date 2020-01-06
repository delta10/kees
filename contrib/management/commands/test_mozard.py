import requests_mock
from django.core.management.base import BaseCommand

from contrib.case_actions.mozard import Action
from core.models import User, Case

class Command(BaseCommand):
    help = 'Run a Mozard test command'

    def add_arguments(self, parser):
        parser.add_argument('--xxb', help='Mozard XXB code', required=True)
        parser.add_argument('--xxc', help='Mozard XXC code', required=True)
        parser.add_argument('--hash', help='Mozard hash code', required=True)

    def handle(self, *args, **options):
        action = Action()

        with requests_mock.mock() as m:
            with open('contrib/mocks/mozard/create_case_response.xml', mode='r') as file:
                mock_response = file.read()

            m.register_uri('POST', 'mock://mozard.organization.test/!suite11.koppelvlak', text=mock_response)

            args = {
                'url': 'mock://mozard.organization.test/!suite11.koppelvlak',
                'xxb': options['xxb'],
                'xxc': options['xxc'],
                'hash': options['hash'],
                'user': User.objects.first()
            }

            action.execute(Case.objects.first(), args)

            last_request = m.request_history[0]
            print(last_request.text)
