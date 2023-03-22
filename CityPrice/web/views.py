import logging

from django import forms
from django.http import JsonResponse
from django.shortcuts import render, redirect

from web import models

logger = logging.getLogger(__name__)


# ------------------- Model Form -------------------
class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add a css style class to the form
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


# ------------------- Main Page -------------------
def index(request):
    return render(request, 'index.html')


# ------------------- Park -------------------
def park(request):
    logger.info('ENTER park page')
    search_name = request.GET.get('search_name')
    if search_name:
        parks = models.Park.objects.filter(name__contains=search_name)
    else:
        search_name = ''
        parks = models.Park.objects.all()

    # print(parks, search_name)
    paginator = Paginator(parks, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        parks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        parks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        parks = paginator.page(paginator.num_pages)
    return render(request, 'park.html', {'parks': parks, 'search_name': search_name})


class ParkForm(BootstrapModelForm):
    area = forms.FloatField(min_value=0)

    class Meta:
        model = models.Park
        fields = '__all__'
        # exclude = ['ID'] # exclude the field ID

    # check if the area is positive
    def clean_area(self):
        area = self.cleaned_data['area']
        if area < 0:
            raise forms.ValidationError('Area must be greater than 0')
        return area


def parkAdd(request):
    # normal way of adding a park
    # if request.method == 'GET':
    #     return render(request, 'park_add.html')
    #
    # name = request.POST.get('inputName')
    # area = request.POST.get('inputArea')
    # location = request.POST.get('inputLocation')
    # district = request.POST.get('inputDistrict')
    #
    # if not all([name, area, location, district]):
    #     return render(request, 'park_add.html', {'error': 'Please fill in all the blanks'})
    #
    # # district existence not checked
    # models.Park.objects.create(name=name, area=area, location=location, district=district)
    #
    # # redirect to park page
    # return redirect('/park/')
    #
    # # todo: redirect to parkAdd page when multiple-add choice is checked
    #
    # Model Form way of adding a park

    form = ParkForm()
    if request.method == 'GET':
        return render(request, 'park_add.html', {'form': form})

    form = ParkForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/park/')

    # print(form.errors)
    return render(request, 'park_add.html', {'form': form})


def parkAddFromFile(request):
    if request.method == 'POST':
        # fileName = request.POST.get('parkFile')
        file = request.FILES.get('parkFile')
        file_data = file.read().decode('utf-8').splitlines()
        print(file_data)
        logger.info(file_data)

        for park in file_data:
            park = park.split()
            print(park)
            logger.info(park)

            try:
                district_instance = models.District.objects.filter(name=park[3]).first()
                if not district_instance:
                    district_instance = models.District.objects.filter(name='其它').first()
                models.Park.objects.create(name=park[0], area=park[1], location=park[2], district=district_instance)
            except Exception as e:
                print(e)
                logger.error(e)
                return render(request, 'add_from_file_error.html',
                              {'error': 'Please check the file format!\n Format: name area(k) location district',
                               'input': park, 'error_info': e
                               })
        return redirect('/park/')
    return redirect('/park/')


def parkEdit(request, nid):
    obj = models.Park.objects.filter(ID=nid).first()
    if request.method == 'GET':
        form = ParkForm(instance=obj)
        return render(request, 'park_edit.html', {'form': form})

    form = ParkForm(data=request.POST, instance=obj)
    if form.is_valid():
        # additional filed value can be like below
        # form.instance.ID = nid
        form.save()
        return redirect('/park/')
    print(form.errors)
    return render(request, 'park_edit.html', {'form': form})


def parkDelete(request, nid):
    id = nid

    if not id:
        return render(request, 'park.html', {'error': 'Please fill in the ID'})

    # id existence not checked
    models.Park.objects.filter(ID=id).delete()
    return redirect('/park/')
    # # redirect to park page
    # return redirect('/park/')


# ------------------- District -------------------
class DistrictForm(BootstrapModelForm):
    class Meta:
        model = models.District
        fields = '__all__'

    def clean_no(self):
        no = self.cleaned_data['no']
        if not no.isdigit():
            raise forms.ValidationError('District No. must be a number')
        return no

    def clean_population(self):
        population = self.cleaned_data['population']
        if population < 0:
            raise forms.ValidationError('Population must be greater than 0')
        return population

    def clean_area(self):
        area = self.cleaned_data['area']
        if area < 0:
            raise forms.ValidationError('Area must be greater than 0')
        return area


class DistrictAddForm(DistrictForm):
    pass


class DistrictEditForm(DistrictForm):
    no = forms.CharField(max_length=20, disabled=True)


def district(request):
    search_name = request.GET.get('search_name')
    if search_name:
        districts = models.District.objects.filter(name__contains=search_name)
    else:
        search_name = ''
        districts = models.District.objects.all()
    # print(districts, search_name)
    districtForm = DistrictAddForm()

    return render(request, 'district.html', {'districts': districts, 'search_name': search_name, 'form': districtForm})


def districtAdd(request):
    if request.method == 'GET':
        return None

    form = DistrictAddForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed', 'errors': form.errors})


def districtAddFromFile(request):
    if request.method == 'POST':
        # fileName = request.POST.get('districtFile')
        file = request.FILES.get('districtFile')
        file_data = file.read().decode('utf-8').splitlines()
        print(file_data)

        for district in file_data:
            district = district.split()
            # log the district info
            logger.info(district)

            try:
                models.District.objects.create(no=district[0], name=district[1], population=district[2],
                                               area=district[3])
            except Exception as e:
                print(e)
                return render(request, 'add_from_file_error.html',
                              {'error': 'Please check the file format!\n Format: no name population area',
                               'input': district, 'error_info': str(e)})
        return redirect('/district/')
    return redirect('/district/')


def districtDelete(request, nid):
    id = nid

    if not id:
        return render(request, 'district.html', {'error': 'Please fill in the No.'})

    # id existence not checked
    models.District.objects.filter(no=id).delete()
    return redirect('/district/')


def districtEdit(request, nid):
    obj = models.District.objects.filter(no=nid).first()
    if request.method == 'GET':
        form = DistrictEditForm(instance=obj)
        return render(request, 'district_edit.html', {'form': form})

    form = DistrictEditForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/district/')
    print(form.errors)
    return render(request, 'district_edit.html', {'form': form})


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def pageTest(request):
    obj = models.District.objects.all()
    paginator = Paginator(obj, 3)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        obj = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        obj = paginator.page(paginator.num_pages)

    return render(request, 'test.html', {'obj': obj})


# ------------------- House -------------------
class HouseForm(BootstrapModelForm):
    class Meta:
        model = models.Neighbourhood
        fields = '__all__'
        exclude = ['latitude', 'longitude']


class HouseAddForm(HouseForm):
    pass


class HouseEditForm(HouseForm):
    name = forms.CharField(max_length=20, disabled=True)


def house(request):
    search_name = request.GET.get('search_name')
    if search_name:
        houses = models.Neighbourhood.objects.filter(name__contains=search_name)
    else:
        search_name = ''
        houses = models.Neighbourhood.objects.all()
    # print(houses, search_name)
    houseForm = HouseAddForm()
    paginator = Paginator(houses, 25)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        houses = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        houses = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        houses = paginator.page(paginator.num_pages)

    return render(request, 'house.html', {'houses': houses, 'search_name': search_name, 'form': houseForm})


def houseAdd(request):
    if request.method == 'GET':
        return None

    form = HouseForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed', 'errors': form.errors})


def houseAddFromFile(request):
    if request.method == 'POST':
        # fileName = request.POST.get('houseFile')
        file = request.FILES.get('houseFile')
        file_data = file.read().decode('utf-8').splitlines()
        # print('file_data', file_data)

        for house in file_data:
            house = house.split()
            # district name price latitude longitude
            # print(house)
            # logger.info(house)
            try:
                district_instance = models.District.objects.filter(name=house[0]).first()
                if not district_instance:
                    district_instance = models.District.objects.filter(name='其它').first()
                models.Neighbourhood.objects.create(name=house[1], district=district_instance, price=house[2],
                                                    latitude=house[3], longitude=house[4])
            except Exception as e:
                print(e)
                logger.error(e)
                return render(request, 'add_from_file_error.html',
                              {
                                  'error': 'Please check the file format!\n Format: no name district latitude longitude',
                                  'input': house, 'error_info': str(e)
                              })
        return redirect('/house/')
    return redirect('/house/')


def houseEdit(request, nid):
    obj = models.Neighbourhood.objects.filter(ID=nid).first()
    if request.method == 'GET':
        form = HouseForm(instance=obj)
        return render(request, 'house_edit.html', {'form': form})

    form = HouseForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/house/')
    print(form.errors)
    return render(request, 'house_edit.html', {'form': form})


def houseDelete(request, nid):
    id = nid

    if not id:
        return render(request, 'house.html', {'error': 'Please fill in the ID'})

    # id existence not checked
    models.Neighbourhood.objects.filter(ID=id).delete()
    return redirect('/house/')


# ------------------- School -------------------
class SchoolForm(BootstrapModelForm):
    class Meta:
        model = models.School
        fields = '__all__'


class SchoolAddForm(SchoolForm):
    pass


def school(request):
    search_name = request.GET.get('search_name')
    if search_name:
        schools = models.School.objects.filter(name__contains=search_name)
    else:
        search_name = ''
        schools = models.School.objects.all()
    # print(schools, search_name)
    schoolForm = SchoolAddForm()

    return render(request, 'school.html', {'schools': schools, 'search_name': search_name, 'form': schoolForm})


def schoolAdd(request):
    if request.method == 'GET':
        return None

    form = SchoolAddForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed', 'errors': form.errors})


def schoolAddFromFile(request):
    if request.method == 'POST':
        # fileName = request.POST.get('schoolFile')
        file = request.FILES.get('schoolFile')
        file_data = file.read().decode('utf-8').splitlines()
        print(file_data)

        for school in file_data:
            school = school.split()
            print(school)
            logger.info(school)
            try:
                # name location district level
                district_instance = models.District.objects.filter(no=school[2]).first()
                if not district_instance:
                    district_instance = models.District.objects.filter(name='其它').first()

                models.School.objects.create(name=school[0], location=school[1], district=district_instance,
                                             level=school[3])

            except Exception as e:
                print(e)
                return render(request, 'add_from_file_error.html',
                              {'error': 'Please check the file format!\n Format: name location district level',
                               'input': school, 'error_info': e})
        return redirect('/school/')
    return redirect('/school/')


def schoolDelete(request, nid):
    id = nid

    if not id:
        return render(request, 'school.html', {'error': 'Please fill in the ID'})

    # id existence not checked
    models.School.objects.filter(ID=id).delete()
    return redirect('/school/')


def schoolEdit(request, nid):
    obj = models.School.objects.filter(ID=nid).first()
    if request.method == 'GET':
        form = SchoolAddForm(instance=obj)
        return render(request, 'school_edit.html', {'form': form})

    form = SchoolAddForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/school/')
    print(form.errors)
    return render(request, 'school_edit.html', {'form': form})


# ------------------- Hospital -------------------
class HospitalForm(BootstrapModelForm):
    class Meta:
        model = models.Hospital
        fields = '__all__'


class HospitalAddForm(HospitalForm):
    pass


def hospital(request):
    search_name = request.GET.get('search_name')
    if search_name:
        hospitals = models.Hospital.objects.filter(name__contains=search_name)
    else:
        search_name = ''
        hospitals = models.Hospital.objects.all()
    # print(hospitals, search_name)
    hospitalForm = HospitalAddForm()

    return render(request, 'hospital.html', {'hospitals': hospitals, 'search_name': search_name, 'form': hospitalForm})


def hospitalAdd(request):
    if request.method == 'GET':
        return None

    form = HospitalAddForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed', 'errors': form.errors})


def hospitalAddFromFile(request):
    if request.method == 'POST':
        # fileName = request.POST.get('hospitalFile')
        file = request.FILES.get('hospitalFile')
        file_data = file.read().decode('utf-8').splitlines()
        print(file_data)

        for hospital in file_data:
            hospital = hospital.split()
            print(hospital)
            logger.info(hospital)
            try:
                # name location district level
                district_instance = models.District.objects.filter(name=hospital[2]).first()
                if not district_instance:
                    district_instance = models.District.objects.filter(name='其它').first()
                models.Hospital.objects.create(name=hospital[0], location=hospital[1], district=district_instance,
                                               level=hospital[3])
            except Exception as e:
                print(e)
                return render(request, 'add_from_file_error.html',
                              {'error': 'Please check the file format!\n Format: name location district level',
                               'input': hospital, 'error_info': e})
        return redirect('/hospital/')
    return redirect('/hospital/')


def hospitalDelete(request, nid):
    id = nid

    if not id:
        return render(request, 'hospital.html', {'error': 'Please fill in the ID'})

    # id existence not checked
    models.Hospital.objects.filter(ID=id).delete()
    return redirect('/hospital/')


def hospitalEdit(request, nid):
    obj = models.Hospital.objects.filter(ID=nid).first()
    if request.method == 'GET':
        form = HospitalAddForm(instance=obj)
        return render(request, 'hospital_edit.html', {'form': form})

    form = HospitalAddForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/hospital/')
    print(form.errors)
    return render(request, 'hospital_edit.html', {'form': form})


def map(request):
    if request.method == 'GET':
        return render(request, 'map.html')


def mapPoints(request):
    if request.method == 'GET':
        houses = models.Neighbourhood.objects.all()

        # get price, lat, lng
        houses_list = houses.values_list('price', 'latitude', 'longitude')

        # ! no need to use json.dumps
        json_list = [{'lat': house[2], 'lng': house[1], 'count': int(house[0])} for house in houses_list]

        return JsonResponse({'houses': json_list})
