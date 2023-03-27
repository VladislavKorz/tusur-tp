from django.http import FileResponse, Http404
from django.urls import reverse
from django.db import models
import datetime

class Specialization(models.Model):
    name = models.TextField("Название специализации")
    create = models.DateTimeField("Создал", auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Специализации'
        verbose_name = 'Специализация'

class Profile(models.Model):    
    external_id = models.PositiveIntegerField(verbose_name='Внешний ID пользователя', unique=True)
    username = models.CharField(verbose_name='Имя пользователя ТГ', max_length=80, null=True)
    surname = models.CharField(verbose_name='Фамилия', max_length=100, blank=True, null=True)
    name = models.CharField(verbose_name='Имя', max_length=100, blank=True, null=True)
    middle_name = models.CharField(verbose_name='Отчество', max_length=100, blank=True, null=True)
    description = models.TextField("Описание", blank=True, null=True)
    phone = models.CharField("Номер телефона", max_length=12, blank=True, null=True)
    photo = models.ImageField("Фото", upload_to="users/profile/photo", blank=True, null=True)
    location_lat = models.FloatField("Локация X", blank=True, null=True)
    location_lon = models.FloatField("Локация Y", blank=True, null=True)
    activate = models.BooleanField("Бот активен?", default=True, blank=True)
    update = models.DateTimeField("Изменил", auto_now=True, auto_now_add=False, null=True)
    create = models.DateTimeField("Создал", auto_now=False, auto_now_add=True, null=True)

    def get_statistic():
        #количество профилей
        return(len(Profile.objects.all()))

    def __str__(self):
        return f'{self.surname} {self.name}'

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'

class StartUp_Profile(models.Model):
    ceo = models.ForeignKey("users.Profile", verbose_name="Организатор", on_delete=models.CASCADE, null=True, related_name='startUp_user')
    name = models.CharField("Название стартапа", max_length=250, null=True)
    description = models.TextField("Описание", null=True)
    needed_to = models.TextField("Что нужно для реализации", null=True)
    logo = models.ImageField("Логотип", upload_to="users/StartUp_Profile/logo", blank=True, null=True)
    presentation = models.FileField("Презентация", upload_to="users/StartUp_Profile/presentation", max_length=100, null=True, blank=True)
    idea = models.TextField("Идея стартап проекта", null=True)
    specialization = models.ManyToManyField("users.Specialization", verbose_name="Специализация")
    views = models.IntegerField("Количество просмотров", default=0)
    activate = models.BooleanField("Прошел модерацию?", default=False, blank=True)
    update = models.DateTimeField("Изменил", auto_now=True, auto_now_add=False, null=True)
    create = models.DateTimeField("Создал", auto_now=False, auto_now_add=True, null=True)

    def get_all_moderated_startups():
        return len(StartUp_Profile.objects.filter(activate__exact = True))

    def get_statistic():
        #количество стратапов
        return(len(StartUp_Profile.objects.all()))
    

    def get_absolute_url(self):
        return reverse("about_startup", args=[self.pk])

    def get_create_url(self, tg_user_id):
        return reverse("add_startup", args=[tg_user_id])

    def __str__(self):
        return f'{self.ceo} - {self.name}'

    class Meta:
        verbose_name_plural = 'Стартапы'
        verbose_name = 'Стартап'

class Card_Profile(models.Model):
    ROLE_CHOICES = (
        ("M", "Ментор"),
        ("E", "Эксперт"),
        ("I", "Инвестор"),
    )
    profile = models.ForeignKey("users.Profile", verbose_name="Профиль", on_delete=models.CASCADE, null=True, related_name='card')
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    specialization = models.ManyToManyField(
        "users.Specialization", verbose_name="Специализация", blank=True)
    description = models.TextField("Описание", blank=True, null=True)
    cv = models.FileField("Резюме", upload_to="users/Card_Profile/cv",
                          max_length=100, blank=True, null=True)
    update = models.DateTimeField(
        "Изменил", auto_now=True, auto_now_add=False, null=True)
    create = models.DateTimeField(
        "Создал", auto_now=False, auto_now_add=True, null=True)

    def get_statistic():
        #количество карт профилей
        return(len(Card_Profile.objects.all()))
    
    def get_cv(self):
        print(self.cv)
        if self.cv:
            return FileResponse(open(self.cv, 'rb'), content_type='application/pdf')
        else:
            return None

    def __str__(self):
        return f'{self.profile.name} {self.profile.surname}'

    class Meta:
        verbose_name_plural = 'Карты профиля'
        verbose_name = 'Карта профиля'


class Team(models.Model):
    start_up = models.ForeignKey(
        "users.StartUp_Profile", verbose_name="Стартап проект", on_delete=models.CASCADE)
    card = models.ForeignKey(
        "users.Card_Profile", verbose_name="Пользователь", on_delete=models.CASCADE)
    role = models.CharField("Роль в стартапе", max_length=50, null=True)

    create = models.DateTimeField(
        "Добавил", auto_now=False, auto_now_add=True, null=True)

        

    class Meta:
        verbose_name_plural = 'Команды'
        verbose_name = 'Команда'
    


class SeeStartUP(models.Model):
    start_up = models.ForeignKey(
        "users.StartUp_Profile", verbose_name="Стартап проект", on_delete=models.CASCADE, related_name='viewed')
    profile = models.ForeignKey(
        "users.Profile", verbose_name="Пользователь", on_delete=models.CASCADE)
    create = models.DateTimeField(
        "Посмотрел", auto_now=False, auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = 'Просмотренные стартапы'
        verbose_name = 'Просмотреный стартап'

class SeeCardProfile(models.Model):
    card = models.ForeignKey(
        "users.Card_Profile", verbose_name="Профиль пользователя", on_delete=models.CASCADE, related_name='viewedCard')
    profile = models.ForeignKey(
        "users.Profile", verbose_name="Пользователь", on_delete=models.CASCADE)
    create = models.DateTimeField(
        "Посмотрел", auto_now=False, auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = 'Просмотренные карты профиля'
        verbose_name = 'Просмотреный карты профиля'


class DatingCard_StartUp(models.Model):
    start_up = models.ForeignKey(
        "users.StartUp_Profile", verbose_name="Стартап проект", on_delete=models.CASCADE)
    card = models.ForeignKey(
        "users.Card_Profile", verbose_name="Пользователь", on_delete=models.CASCADE)
    match_start_up = models.BooleanField(
        "Стартап лайкнул профиль", default=False)
    match_profile = models.BooleanField(
        "Профиль лайкнул стартап", default=False)
    match_start_up_datetime = models.DateTimeField(null=True, blank=True)
    match_profile_datetime = models.DateTimeField(null=True, blank=True)

    def show_role(self):
        for role in Card_Profile.ROLE_CHOICES:
            if self.card.role in role:
                return role[1]
    show_role.short_description = "Роль"
    def get_statistic():
        #количество успешных матчей
        return(len(Card_Profile.objects.all()))

    def __str__(self):
        return f'{self.start_up} - {self.card}'

    class Meta:
        verbose_name_plural = 'Матчи'
        verbose_name = 'Матч'

class Investment(models.Model):
    start_up = models.ForeignKey("users.StartUp_Profile", verbose_name="Стартап проект", on_delete=models.CASCADE, related_name='investment')
    name = models.CharField("Название", max_length=50) 
    value = models.IntegerField("Значение")
    create = models.DateTimeField("Посмотрел", auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.start_up}'


    class Meta:
        verbose_name_plural = 'Инвестиции'
        verbose_name = 'Инвестиции'
