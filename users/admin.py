from django.contrib import admin
from users.models import User, Payments


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "is_active",
        "avatar",
        "phone_number",
        "city",
    )


admin.site.register(User, UserAdmin)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "paid_course",
        "paid_lesson",
        "data",
        "payment_count",
        "payment_method",
    )


from django.contrib import admin

# Register your models here.
