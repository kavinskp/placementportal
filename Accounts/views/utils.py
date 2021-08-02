from django.contrib.auth.models import Group
from Accounts.models import StaffAccount, StudentAccount
from Curriculum.models import Department,Batch


def getHODsOrderByName(is_active=True):
    return StaffAccount.objects.filter(designation=2, user__is_active=is_active).order_by('user__profile__first_name')


def getStaffUsingStaffId(staff_id, is_active=True):
    return StaffAccount.objects.get(staff_id=staff_id, user__is_active=is_active)


def getFacultiesOrderByName(dep_name=None, is_active=True):
    if dep_name is not None:
        return StaffAccount.objects.filter(designation=3, department__name=dep_name,
                                           user__is_active=is_active).order_by(
            'user__profile__first_name')
    else:
        return StaffAccount.objects.filter(designation=3, user__is_active=is_active).order_by(
            'user__profile__first_name')


def getStaffsOrderByName(dep_name=None, is_active=True):
    if dep_name is not None:
        return StaffAccount.objects.filter(department__name=dep_name, user__is_active=is_active).order_by(
            'user__profile__first_name')
    else:
        return StaffAccount.objects.filter(user__is_active=is_active).order_by(
            'user__profile__first_name')


def getAllPlacementRepresentatives(dep_name=None, is_active=True):
    group = Group.objects.get(name='PR')
    if dep_name is not None:
        return StudentAccount.objects.filter(info__batch__department__name=dep_name,
                                             user__groups=group,
                                             user__is_active=is_active)
    else:
        return StudentAccount.objects.filter(user__groups=group, user__is_active=is_active)


def getAllBatchStudentsSortByName(batch_id, is_active=True):
    return StudentAccount.objects.filter(info__batch=batch_id, user__is_active=is_active).order_by(
        'user__profile__first_name')


def getAllStudentsSortByName(dep_name=None, is_active=True):
    if dep_name is not None:
        return StudentAccount.objects.filter(info__batch__department__name=dep_name,
                                             user__is_active=is_active).order_by(
            'user__profile__first_name')
    else:
        return StudentAccount.objects.filter(user__is_active=is_active).order_by('user__profile__first_name')


def getStudentByRollNO(roll_no, is_active=True):
    return StudentAccount.objects.get(info__roll_no=roll_no, user__is_active=is_active)


def getPlacementOfficers(is_active=True):
    group = Group.objects.get(name='PO')
    return StaffAccount.objects.filter(user__groups=group, user__is_active=is_active)


def getActiveDepartments():
    return Department.objects.all().exclude(name='General')


def getInterviewAllowedBatches():
    return Batch.objects.filter(current_semester__gte=7, in_active=False)