from loguru import logger
from django.shortcuts import render
from .models import StartUp_Profile, Specialization, Profile,Card_Profile,Team,Investment
from django.db.models import Sum

def index(request, tg_user_id):
    spec = Specialization.objects.all()
    context = {"spec": spec,"condition" : False}
    if request.method == "POST":
        response_dict = request.POST
        st_obj = StartUp_Profile()
        st_obj.name = response_dict.get('name_startup')
        st_obj.idea = response_dict.get('idea_startup')
        st_obj.description = response_dict.get('desc_startup')
        st_obj.needed_to = response_dict.get('need_startup')
        st_obj.ceo = Profile.objects.get(external_id=tg_user_id)
        invests_names = response_dict.getlist("name_investments")
        invests_values = response_dict.getlist("value_investments")
        st_obj.save()
        st_obj.specialization.set(Specialization.objects.filter(
            name=response_dict.get('segment')))
        st_obj.save()
        for name,value in list(zip(invests_names,invests_values)):
            inv_obj = Investment(start_up=st_obj, name=name, value=int(value))
            inv_obj.save()
        context["condition"] = True


    return render(request, 'add_startup.html', context=context)


def about_startup(request, startup_id):
    startup = StartUp_Profile.objects.get(id=startup_id)
    startup.views+=1
    context = { "name" : startup.name,
                "ceo_surname" : startup.ceo.surname,
                "ceo_name" : startup.ceo.name,
                "ceo_middle_name" : startup.ceo.middle_name,
                "idea" : startup.idea,
                "needed_to" : startup.needed_to,
                "create" : startup.create,
                "description" : startup.description,
                "views": startup.views,
                "logo" : startup.logo,
                "presentation" : startup.presentation,
                "isCreater":False,
                }
    # startup = StartUp_Profile.objects.filter(activate=True)
    startup.save()
    return render(request, 'more_about_startup.html',context=context)

def base_template(request):
    Data = StartUp_Profile.objects.filter(activate=True).order_by('-views')[:3]
    investments = []
    for el in Data:
        investments.append(Investment.objects.filter(
            start_up=el).aggregate(Sum('value'))['value__sum'])
    Data = list(zip(Data,investments))
    return render(request, 'base.html', {'Data': Data})

def startups_template(request):
    Data = StartUp_Profile.objects.filter(activate=True)
    investments = []
    for el in Data:
        investments.append(Investment.objects.filter(
            start_up=el).aggregate(Sum('value'))['value__sum'])
    Data = list(zip(Data, investments))
    return render(request, 'main.html', {'Data' : Data})

def about_template(request):
    return render(request, 'about_me.html')

def card_template(request,tg_user_id):
    user_Profile = Profile.objects.get(external_id = tg_user_id) 
    spec = Specialization.objects.all()
    rols = [x[1] for x in Card_Profile.ROLE_CHOICES]
    condition = False
    if request.method == "POST":
        resp = request.POST 
        st_obj = Card_Profile()
        st_obj.profile = user_Profile
        for el in Card_Profile.ROLE_CHOICES:
            if resp.get('role') in el:
                st_obj.role = el[0]
        condition = True
        st_obj.cv = resp.get('cv')
        st_obj.description = resp.get('description_startup')
        st_obj.save()
        st_obj.specialization.set(Specialization.objects.filter(
            name=resp.get('segment')))
        st_obj.save()
    return render(request, 'card.html',context={"spec": spec,"rols":rols,"user_Profile" : user_Profile, "condition":condition })


