from django.contrib import admin
from .models import *


@admin.register(Card_Profile)
class Card_ProfileAdmin(admin.ModelAdmin):
    list_display = ("profile", "role")


class InvestmentInline(admin.StackedInline):
    model = Investment
    extra = 1


@admin.register(StartUp_Profile)
class StartUp_Profile_Admin(admin.ModelAdmin):
    inlines = [InvestmentInline]
    list_display = ("pk","name", "ceo", "views", "activate", "create")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("external_id", "username",
                    "surname", "name", "phone", "create")
    search_fields = ("username__startswith", "external_id__startswith",
                     "surname__startswith", "name__startswith", "phone__startswith", "create__startswith")

@admin.register(DatingCard_StartUp)
class DatingCard_StartUp_Admin(admin.ModelAdmin):
    list_display = ("pk", "start_up", "card", "show_role")

@admin.register(Team)
class Team_Admin(admin.ModelAdmin):
    list_display = ("start_up", "card", "role", "create")

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("name","create")


@admin.register(SeeStartUP)
class SeeStartupAdmin(admin.ModelAdmin):
    list_display = ("start_up", "profile", "create")

@admin.register(SeeCardProfile)
class SeeCardProfileAdmin(admin.ModelAdmin):
    list_display = ("card", "profile", "create")


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ("start_up", "name", "value", "create")
