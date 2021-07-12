from django.contrib.auth.models import Group
Group.objects.all().delete()

Group.objects.create(name='Student')
Group.objects.create(name='Principal')
Group.objects.create(name='HOD')
Group.objects.create(name='Faculty')
Group.objects.create(name='PO')
Group.objects.create(name='PR')
Group.objects.create(name='POC')

print('Groups created')