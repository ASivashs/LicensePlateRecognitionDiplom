FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get -y install tesseract-ocr \ 
    && apt-get -y install ffmpeg libsm6 libxext6 

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY /Bootstrap_studio .
COPY /good_images .
COPY /images_jpg .
COPY /license_plate_sign_in_register_interface .
COPY /license_plate_table .
COPY /license_recognition .
COPY /LicensePlateRecognitionInterface .
COPY /profile_and_site_settings .
COPY /responsed_images .
COPY /utilities .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver"]
