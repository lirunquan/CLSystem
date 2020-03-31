from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(EmailSentRecord)
admin.site.register(CertificationSentRecord)
admin.site.register(VerifyCodeSentRecord)
admin.site.register(CommitCodeRecord)
admin.site.register(CompileSrcRecord)
admin.site.register(JudgeRecord)
admin.site.register(CommitMissionRecord)
