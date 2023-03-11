from django import forms
from django.http import JsonResponse
from django.shortcuts import render, redirect

from web import models


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
    search_name = request.GET.get('search_name')
    if search_name:
        parks = models.Park.objects.filter(name__contains=search_name)
    else:
        search_name = ''
        parks = models.Park.objects.all()

    # print(parks, search_name)
    paginator = Paginator(parks, 3) # Show 25 contacts per page

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
        fileName = request.POST.get('parkFile')
        file = request.FILES
        print(file)

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
    paginator = Paginator(obj, 3) # Show 25 contacts per page

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


def house(request):
    search_name = request.GET.get('search_name')
    if search_name:
        houses = models.Neighbourhood.objects.filter(name__contains=search_name)
    else:
        search_name = ''
        houses = models.Neighbourhood.objects.all()
    # print(houses, search_name)

    return render(request, 'house.html', {'houses': houses, 'search_name': search_name})



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
    print('map')
    return render(request, 'map.html')