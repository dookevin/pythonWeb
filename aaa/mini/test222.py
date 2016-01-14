# coding:utf-8
from django import forms
class UploadFileForm(forms.Form):
  title = forms.CharField(max_length=50)
  file = forms.FileField() #处理图片时可用 image=forms.ImageField()
#
#处 理这个form的视图收到了在request.FILES中的文件数据。
#从上述form来的数据可能通过request.FILES['file']来存 取。
#特别注意的是，只有当request方法是POST,且发送request的<form>有属性 enctype="multipart/form-data"时，
#request.FILES中包含文件数据，否则request.FILES为空。
#以下视图函数：
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect,requires_csrf_token,csrf_exempt

@csrf_exempt
def upload_file(request):
    print '>>>>>11111111111'
    if request.method == 'POST':
        try:
            
            form = UploadFileForm(request.POST, request.FILES)
    #        if form.is_valid():
            f = request.FILES['file']
            print 'FFFFFFFF',f
            handle_uploaded_file(f)
        except Exception,e:
            print e
    
    return HttpResponse('success')

FILE_PATH = "D:/images/"
def handle_uploaded_file(f):
    try:
        
        p = FILE_PATH+f.name
        destination = open(p, 'wb+')
        for chunk in f.chunks():
            
            destination.write(chunk)
        
        destination.close()
    except Exception,e:
        print e
        
    



