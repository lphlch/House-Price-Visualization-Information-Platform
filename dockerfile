FROM python
WORKDIR /citypriceweb
ADD /CityPrice .
RUN pip install -r requirements.txt
# EXPOSE 8000:8000 3306:3306
# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]