from django.contrib.auth.models import Permission, ContentType, Group

Permission.objects.all().delete()
ContentType.objects.all().delete()

all_permission = (('Accounts', 'Staff', 'can_allot_hod', 'Can allot hod'),
                  ('Accounts', 'Staff', 'can_approve_faculty', 'Can approve Faculties'),
                  ('Accounts', 'Staff', 'can_approve_student', 'Can approve Students'),
                  ('Accounts', 'Staff', 'can_assign_po', 'Can assign Placement Officer'),
                  ('Accounts', 'Staff', 'can_assign_pr', 'Can assign Placement Representatives'),
                  ('Accounts', 'Staff', 'can_assign_poc', 'Can assign Point Of Contact'),
                  )
for permission in all_permission:
    content_type = ContentType.objects.get_or_create(app_label=permission[0], model=permission[1])

for permission in all_permission:
    content_type = ContentType.objects.get(app_label=permission[0], model=permission[1])
    Permission.objects.create(codename=permission[2],
                              name=permission[3],
                              content_type=content_type)

allocate_perms = (('Principal', 'can_allot_hod'),
                  ('HOD', 'can_approve_faculty'),
                  ('Faculty', 'can_approve_student'),
                  ('Principal', 'can_assign_po'),
                  ('HOD', 'can_assign_pr'),
                  ('PO', 'can_assign_poc')
                  )

for perm in allocate_perms:
    g = Group.objects.get(name=perm[0])
    g.permissions.add(Permission.objects.get(codename=perm[1]))

print('All Permissions created & assigned to group')
