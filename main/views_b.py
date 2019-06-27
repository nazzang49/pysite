from django.shortcuts import render

# 원본 백업 파일 = 기능 구현 완료
def index(request):
    return render(request,'main/index.html')