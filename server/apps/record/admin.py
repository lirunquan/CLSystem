from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(LoginRecord)
admin.site.register(EmailCertificationRecord)
admin.site.register(EmailSentRecord)
admin.site.register(CertificationSentRecord)
admin.site.register(ChangePasswordRecord)
admin.site.register(VerifyCodeSentRecord)
admin.site.register(CommitCodeRecord)
admin.site.register(CommitChoiceRecord)
admin.site.register(CommitCompletionRecord)
admin.site.register(CompileSrcRecord)
admin.site.register(JudgeRecord)
