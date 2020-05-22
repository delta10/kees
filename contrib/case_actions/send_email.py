from smtplib import SMTPException
from django.core.mail import send_mail
from django.template import Template, Context


class Action:
    name = 'Send email'

    def render_template(self, case, args, argument):
        context = Context({
            'case': case,
            'args': args
        })

        template = Template(args.get(argument, ''))
        return template.render(context)

    def execute(self, case, args):
        subject = self.render_template(case, args, 'subject')
        message = self.render_template(case, args, 'message')

        try:
            send_mail(
                subject,
                message,
                args.get('email_from', None),
                args['email_to'],
                fail_silently=False
            )

            case.logs.create(
                event='send_email',
                metadata={
                    'email_to': args['email_to'],
                    'subject': subject,
                    'message': message
                }
            )

            return True
        except (SMTPException, ConnectionRefusedError) as e:
            case.logs.create(
                event='send_email',
                metadata={
                    'error': 'Could not send e-mail due to exception: {}'.format(e)
                }
            )

            return False
