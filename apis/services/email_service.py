# emails/services.py
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from django.utils import timezone
from apis.models import EmailProviderSetting, EmailLog
from apis.exceptions import ServiceError
import logging

logger = logging.getLogger("color_logger")


class EmailService:
    @staticmethod
    def send_email_with_template(
        template_name: str,
        context: dict,
        subject: str,
        to_emails: list[str],
    ):
        
        provider = EmailProviderSetting.objects.filter(is_active=True).first()
        if not provider:
            raise ServiceError("No active email provider configured", status_code=503)

        body = render_to_string(f"emails/{template_name}", context)

        email_log = EmailLog.objects.create(
            subject=subject,
            body=body,
            to=to_emails,
            email_provider=provider,
            from_email=provider.from_email,
        )

        try:
            if provider.provider_type == "smtp":
                connection = get_connection(
                    backend="django.core.mail.backends.smtp.EmailBackend",
                    host=provider.host,
                    port=provider.port,
                    username=provider.username,
                    password=provider.password,
                    use_tls=provider.use_tls,
                    use_ssl=provider.use_ssl,
                )
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=provider.from_email,
                    to=to_emails,
                    connection=connection,
                )
                email.content_subtype = "html"
                email.send()
                logger.info(f"Email sent to {to_emails}")

            elif provider.provider_type == "sendgrid":
                import sendgrid
                from sendgrid.helpers.mail import Mail

                sg = sendgrid.SendGridAPIClient(api_key=provider.api_key)
                mail = Mail(
                    from_email=provider.from_email,
                    to_emails=to_emails,
                    subject=subject,
                    html_content=body,
                )
                response = sg.send(mail)
                if response.status_code not in [200, 202]:
                    raise ServiceError(
                        f"SendGrid returned {response.status_code}",
                        status_code=response.status_code,
                    )
                logger.info(f"Email sent to {to_emails}")
            else:
                raise ServiceError("Unsupported email provider type", status_code=400)

            email_log.status = "sent"
            email_log.sent_at = timezone.now()
            email_log.save()

        except ServiceError as e:
            # Custom exception already raised — just update log
            email_log.status = "failed"
            email_log.error_message = e.message
            email_log.save()
            logger.error(f"Email failed to send to {to_emails}: {e}")
            

        except Exception as e:
            # Convert any other errors into ServiceError
            email_log.status = "failed"
            email_log.error_message = str(e)
            email_log.save()
            logger.error(f"Email failed to send to {to_emails}: {e}")
    

    def resend_email(self, email_log_id: int):
        email_log = EmailLog.objects.get(id=email_log_id)
        self.send_email_with_template(
            email_log.subject,
            email_log.body,
            email_log.to,
            email_log.email_provider,
        )
            
    
