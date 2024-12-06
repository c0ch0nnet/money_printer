from rest_framework.permissions import BasePermission


# class RequestPermission(BasePermission):
#     def has_permission(self, request, view):
#         if "destroy" == view.action:
#             return bool(request.user and request.user.is_staff)
#
#         return bool(request.user and request.user.is_authenticated)


class RequestPermission(BasePermission):
    def has_permission(self, request, view):
        if "destroy" == view.action:
            return request.user.is_staff

        return True
