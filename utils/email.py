from templated_email import send_templated_mail

DEFAULT_FROM_EMAIL = 'SmartPad <notifications@smartpad.ph>'

class SendEmail:

    def send(template, data):
        send_templated_mail(template_name=template,
            from_email      = data['from_email'] if hasattr(data, 'from_email') else DEFAULT_FROM_EMAIL,
            recipient_list  = data['recipient_list'],
            context         = data['context'],
            create_link     = True
        )
