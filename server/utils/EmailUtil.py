from django.core.mail import send_mail, send_mass_mail
from apps.record.models import CertificationSentRecord, EmailSentRecord, VerifyCodeSentRecord
from apps.course.models import Notice
from django.template import loader
from server.settings import DEFAULT_FROM_EMAIL, SERVER_HOST
from utils.manager import Manager


class EmailUtil(Manager):
    def __init__(self, account, identity, receive: list, **kwargs):
        super().__init__()
        self.account = account
        self.identity = identity
        self.token = ''
        self.code = ''
        self.email_receiver = receive
        self.kwargs = kwargs

    def send(self, email_type):
        if email_type == 'certificate':
            if not self.send_certificate_email():
                self.save_sent_record(email_type, False)
                return -1
        if email_type == 'forgot':
            if not self.send_forgot_email():
                self.save_sent_record(email_type, False)
                return -1
        if email_type == 'notice':
            if not self.send_notice_email():
                self.save_sent_record(email_type, False)
                return -1
        self.save_sent_record(email_type)
        return 1

    def load_html(self, html_file, params):
        template = loader.get_template(html_file)
        return template.render(params)

    def send_certificate_email(self):
        self.token = self.get_md5_str()
        self.code = self.get_random_code(length=8)
        url = SERVER_HOST + \
            "/user/email/active/?token={0}&code={1}".format(
                self.token, self.code
            )
        email_content = self.load_html(
            html_file='email/certificate.html',
            params={"active_url": url}
        )
        email_title = "认证邮箱并激活"
        email_sender = DEFAULT_FROM_EMAIL
        ret = send_mail(
            subject=email_title,
            from_email=email_sender,
            message='',
            html_message=email_content,
            recipient_list=self.email_receiver
        )
        return ret == 1

    def send_forgot_email(self):
        self.code = self.get_random_code(length=6)
        content = self.load_html(
            html_file='email/forgot.html',
            params={"code": self.code}
        )
        title = "重设密码验证码"
        email_sender = DEFAULT_FROM_EMAIL
        ret = send_mail(
            subject=title,
            from_email=email_sender,
            message='',
            html_message=content,
            recipient_list=self.email_receiver
        )
        return ret == 1

    def send_notice_email(self):
        n_id = self.kwargs.get('notice_id')
        notice = Notice.objects.filter(id=n_id)
        if len(notice) == 1:
            title = "新公告"
            html_content = self.load_html(
                html_file='email/notice.html',
                params={"notice": notice[0]}
            )
            email_sender = DEFAULT_FROM_EMAIL
            ret = send_mass_mail(
                subject=title,
                from_email=email_sender,
                message='',
                html_message=html_content,
                recipient_list=self.email_receiver
            )
            return ret == 1
        return -1

    def save_sent_record(self, email_type, success=True):
        if email_type == 'certificate':
            record = CertificationSentRecord(
                account=self.account,
                identity=self.identity,
                recipients=';'.join(self.email_receiver),
                token=self.token,
                active_code=self.code,
                email_type=email_type,
                success=success
            )
            record.save()
        if email_type == 'forgot':
            record = VerifyCodeSentRecord(
                account=self.account,
                identity=self.identity,
                recipients=';'.join(self.email_receiver),
                code=self.code,
                email_type=email_type,
                success=success
            )
            record.save()
        if email_type == 'notice':
            record = EmailSentRecord(
                account=self.account,
                identity=self.identity,
                recipients=';'.join(self.email_receiver),
                email_type=email_type,
                success=success
            )
            record.save()
