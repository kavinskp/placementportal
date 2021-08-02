from django.contrib.auth.models import Group, Permission, ContentType
from Accounts.models import UserGroups, UserPermissions, CustomUser, StaffAccount, StudentAccount
from Curriculum.models import Batch, Department

Group.objects.all().delete()
Permission.objects.all().delete()
ContentType.objects.all().delete()

for gp in UserGroups:
    Group.objects.create(name=gp.group_name())
    print('Group created ' + gp.group_name())

permission_set = (
    (UserPermissions.CAN_APPROVE_STAFF, CustomUser),
    (UserPermissions.CAN_APPROVE_STUDENT, CustomUser),
    (UserPermissions.CAN_APPROVE_INTERVIEWER, CustomUser),
    (UserPermissions.CAN_ASSIGN_HOD, Department),
    (UserPermissions.CAN_ASSIGN_FA, Batch),
    (UserPermissions.CAN_UPDATE_BATCHES, Batch),
    (UserPermissions.CAN_ASSIGN_PO, StaffAccount),
    (UserPermissions.CAN_ASSIGN_PR, StudentAccount),
    (UserPermissions.CAN_ASSIGN_POC, StudentAccount),
)
for permission in permission_set:
    ContentType.objects.get_or_create(app_label=permission[0].get_app_label(), model=permission[1].__name__)

for permission in permission_set:
    content_type = ContentType.objects.get(app_label=permission[0].get_app_label(), model=permission[1].__name__)
    Permission.objects.create(codename=permission[0].get_code(),
                              name=permission[0].get_description(),
                              content_type=content_type)

group_permission_set = (
    (UserGroups.PRINCIPAL, UserPermissions.CAN_APPROVE_STAFF),
    (UserGroups.HOD, UserPermissions.CAN_APPROVE_STAFF),
    (UserGroups.HOD, UserPermissions.CAN_APPROVE_STUDENT),
    (UserGroups.FACULTY, UserPermissions.CAN_APPROVE_STUDENT),
    (UserGroups.PLACEMENT_OFFICER, UserPermissions.CAN_APPROVE_INTERVIEWER),
    (UserGroups.PLACEMENT_REPRESENTATIVE, UserPermissions.CAN_APPROVE_INTERVIEWER),
    (UserGroups.PRINCIPAL, UserPermissions.CAN_ASSIGN_HOD),
    (UserGroups.HOD, UserPermissions.CAN_ASSIGN_FA),
    (UserGroups.PRINCIPAL, UserPermissions.CAN_UPDATE_BATCHES),
    (UserGroups.PRINCIPAL, UserPermissions.CAN_ASSIGN_PO),
    (UserGroups.HOD, UserPermissions.CAN_ASSIGN_PR),
    (UserGroups.PLACEMENT_OFFICER, UserPermissions.CAN_ASSIGN_POC),
)

for perm in group_permission_set:
    g = Group.objects.get(name=perm[0].group_name())
    g.permissions.add(Permission.objects.get(codename=perm[1].get_code()))
    print(str(g.name) + " " + perm[1].get_description())

print('All Permissions created & assigned to group')
