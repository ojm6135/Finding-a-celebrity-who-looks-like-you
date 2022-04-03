from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from search import search_celeb
from . import models
import os
from my_project import settings
import re


def index(request):
    # https://stackoverflow.com/questions/51155947/django-redirect-to-another-view-with-context
    for key in ['celebrity', 'confidence', 'img_src']:
        if key in request.session:
            del request.session[key]
            
    remove_files()
    
    return render(request, 'index.html')


def show_result(request):
    return render(request, 'index.html')


@csrf_exempt
def search(request):
    remove_files()
    
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['choose-file']
        except KeyError:  # 업로드된 파일이 없을 때
            return redirect('/')
        
        # 파일이름의 특수문자, 공백 제거
        file_name = str(uploaded_file)
        file_name = re.sub('[`~!@#$%&()+=,\/:*?\'"<>|;]', '', file_name)
        file_name = re.sub('[\s]', '_', file_name)
        
        # api 사용을 위한 파일 임시저장
        document = models.Document(
            uploadedFile = uploaded_file
        )
        document.save()
        
        # api 사용
        result = search_celeb(f'media/Uploaded_Files/{file_name}')
        
        # api 사용 후 임시저장된 파일 삭제
        # os.remove(os.path.join(settings.MEDIA_ROOT, f'Uploaded_Files/{file_name}'))
        
        celebrity, confidence = result
        
        # https://stackoverflow.com/questions/51155947/django-redirect-to-another-view-with-context
        request.session['celebrity'] = celebrity
        request.session['confidence'] = str(confidence)
        request.session['img_src'] = f'/media/Uploaded_Files/{file_name}'
        
        if isinstance(confidence, int):
            request.session['confidence'] += '%'
            
            
        return redirect('/result')
    
    
def remove_files():
    files = os.listdir('media/Uploaded_Files')
    
    for file in files:
        os.remove(os.path.join(settings.MEDIA_ROOT, f'Uploaded_Files/{file}'))