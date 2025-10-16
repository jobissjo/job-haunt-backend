from typing import Any
from apis.models.user import CustomUser
from django.core.exceptions import ObjectDoesNotExist

class UserRepository:

    @staticmethod
    def get_users(
        filters: dict[str, Any] = None,
        prefetch_related: list[str] = None,
        select_related: list[str] = None,
        order_by: list[str] = None
    ):
        users = CustomUser.objects.all()

        if filters:
            users = users.filter(**filters)
        
        if select_related:
            users = users.select_related(*select_related)
        
        if prefetch_related:
            users = users.prefetch_related(*prefetch_related)
        
        if order_by:
            users = users.order_by(*order_by)
        
        return users

    @staticmethod
    def get_user_by_id(
        user_id: int,
        select_related: list[str] = None,
        prefetch_related: list[str] = None
    ) -> CustomUser | None:
        """
        Fetch a single user by ID. Optional select_related/prefetch_related
        can be used if you know you'll access related objects.
        Returns None if user not found.
        """
        try:
            queryset = CustomUser.objects
            if select_related:
                queryset = queryset.select_related(*select_related)
            if prefetch_related:
                queryset = queryset.prefetch_related(*prefetch_related)
            
            return queryset.get(id=user_id)
        except ObjectDoesNotExist:
            return None
