import mimetypes
import os

from django.http import HttpResponse
from django.shortcuts import render
from license_plate_table.models import License_plate
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from profile_and_site_settings.models import WhiteList
import json

import cv2
import imutils
import numpy as np
import pytesseract
import sys


# if sys.platform == 'win32':
#     pytesseract.pytesseract.tesseract_cmd = r'D:\\Programs\\Tesseract\\tesseract.exe'

def view_license_recognition(request):
    if 'upload_photo' in request.POST:
        if image := request.FILES.get('image', False):
            print(request.FILES.get('image'))
            save_photo('license_recognition/static/image', image)
            recognition_result = number_finder(f'license_recognition/static/image/{image.name}')
            new_license_plate = License_plate()
            new_license_plate.license_plate = recognition_result
            new_license_plate.region = 'BY'
            new_license_plate.date_time = datetime.now()
            new_license_plate.user_name = '-'
            new_license_plate.source = 'image'
            image_data = open(f"license_recognition/static/image/{image.name}", "rb").read()
            new_license_plate.field_name = SimpleUploadedFile(name=f"{image.name}", content=image_data, )
            new_license_plate.save()
            return render(request, 'license_recognition/license_recignition.html',
                          {'rec_res': recognition_result,
                           'path_to_file': f'/static/image/{image.name}'})
    if 'add_owner' in request.POST:
        lic_plate = request.POST.get('lic_plate', 'unknown')
        region = request.POST.get('region', 'BY')
        owner = request.POST.get('owner', 'unknown')
        white_list = WhiteList()
        white_list.license_plate = lic_plate
        white_list.user_name = owner
        white_list.save()
    if 'save' in request.POST:
        lic_plate = request.POST.get('lic_plate', 'unknown')
        region = request.POST.get('region', 'BY')
        owner = request.POST.get('owner', 'unknown')
        # load_json(lic_plate, region, owner)
        json_save_one(lic_plate, region, owner)
        # Открываем файл JSON на запись
        return download_file()

    return render(request, 'license_recognition/license_recignition.html')


def number_finder(image_name: str):
    """
        Detect license plate and convert license plate number to image.
        :arg1: img path.
        :return: tuple with image name and responsed number or None.
        """

    img = cv2.imread(image_name, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (600, 400))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)

    edged = cv2.Canny(gray, 30, 200)
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screen_cnt = None

    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.018 * peri, True)

        if len(approx) == 4:
            screen_cnt = approx
            break

    detected = False if screen_cnt is None else True

    if detected:
        cv2.drawContours(img, [screen_cnt], -1, (255, 0, 0), 4)

    mask = np.zeros(gray.shape, np.uint8)
    try:
        new_image = cv2.drawContours(mask, [screen_cnt], 0, 255, -1)
    except Exception as exc:
        img_name = image_name.split(check_slash())[-1]
        return (img_name, None)

    new_image = cv2.bitwise_and(img, img, mask=mask)

    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

    license_plate = pytesseract.image_to_string(Cropped, config='--psm 11')

    # This block illustrate image and cropped image
    img = cv2.resize(img, (500, 300))
    Cropped = cv2.resize(Cropped, (400, 200))
    # cv2.imshow('car', img)
    # cv2.imshow('Cropped', Cropped)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    img_name = image_name.split(check_slash())[-1]

    filename_responsed = f'responsed_images{check_slash()}responsed_{img_name}'
    cv2.imwrite(filename_responsed, img)

    filename_cropped = f'cropped_images{check_slash()}cropped_{img_name}'
    cv2.imwrite(filename_cropped, Cropped)

    license_plate = license_plate.strip()
    return (license_plate)



def save_photo(path_to_folder: str, image):
    with open(f'{path_to_folder}/{image.name}', 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)


def download_file():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'res_rec.json'
    filepath = BASE_DIR + '/license_recognition/static/json/' + filename
    path = open(filepath, 'r', encoding="utf-8",)
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def json_save_one(lic_plate, region, owner):
    with open('license_recognition/static/json/res_rec.json', encoding='utf-8') as file_json:
        data = json.load(file_json)
    data['lic_plate'] = lic_plate
    data['region'] = region
    data['owner'] = owner
    with open('license_recognition/static/json/res_rec.json', 'w', encoding='utf-8') as file_json:
        json.dump(data, file_json, indent=4, ensure_ascii=False)


def check_slash():
    return "/" if sys.platform == "Linux" else "\\"
