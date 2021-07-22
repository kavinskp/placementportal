from django.contrib.auth.models import Permission, ContentType, Group
from Accounts.models import StaffAccount
from Curriculum.models import Regulation

Permission.objects.all().delete()
ContentType.objects.all().delete()

all_permission = (('Accounts', StaffAccount, 'can_allot_hod', 'Can allot hod'),
                  ('Accounts', StaffAccount, 'can_approve_faculty', 'Can approve Faculties'),
                  ('Accounts', StaffAccount, 'can_approve_student', 'Can approve Students'),
                  ('Accounts', StaffAccount, 'can_assign_po', 'Can assign Placement Officer'),
                  ('Accounts', StaffAccount, 'can_assign_pr', 'Can assign Placement Representatives'),
                  ('Accounts', StaffAccount, 'can_assign_poc', 'Can assign Point Of Contact'),
                  ('Curriculam', Regulation, 'can_update_batches', 'Can update Batch Details'),
                  )
for permission in all_permission:
    content_type = ContentType.objects.get_or_create(app_label=permission[0], model=str(permission[1]))

for permission in all_permission:
    content_type = ContentType.objects.get(app_label=permission[0], model=permission[1])
    Permission.objects.create(codename=permission[2],
                              name=permission[3],
                              content_type=content_type)

allocate_perms = (('Principal', 'can_allot_hod'),
                  ('Principal', 'can_approve_faculty'),
                  ('HOD', 'can_approve_faculty'),
                  ('Faculty', 'can_approve_student'),
                  ('Principal', 'can_view_batches'),
                  ('Principal', 'can_create_batches'),
                  ('Principal', 'can_update_batches'),
                  ('HOD', 'can_view_batches'),
                  ('Principal', 'can_assign_po'),
                  ('HOD', 'can_assign_pr'),
                  ('PO', 'can_assign_poc')
                  )

for perm in allocate_perms:
    g = Group.objects.get(name=perm[0])
    g.permissions.add(Permission.objects.get(codename=perm[1]))

print('All Permissions created & assigned to group')
