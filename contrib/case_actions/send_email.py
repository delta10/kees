from smtplib import SMTPException
from django.core.mail import send_mail
from django.template import Template, Context


class Action:
    name = 'Send email'

    def render_template(self, argument):
        context = Context({
            'case': self.case,
            'args': self.args
        })

        template = Template(self.args.get(argument, ''))
        return template.render(context)

    def execute(self, case, args):
        self.case = case
        self.args = args

        subject = self.render_template('subject')
        message = self.render_template('message')

        try:
            result = send_mail(
                subject,
                message,
                self.args.get('email_from', None),
                self.args['email_to'],
                fail_silently=False
            )

            case.logs.create(
                event='send_email',
                description='Sucessfully sent email to {} with subject {} and message {}'.format(
                    self.args['email_to'],
                    subject,
                    message
                )
            )

            return True
        except (SMTPException, ConnectionRefusedError) as e:
            case.logs.create(
                event='send_email',
                description='Could not send e-mail due to exception: {}'.format(e)
            )

            return False
