from django.db.models import Max, F
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board

def list(requst, pagenum=1):
    # 페이징 처리
    currentpage = pagenum
    pagesize = 5
    pageblock = 3
    startrow = (currentpage-1)*pagesize+1
    count = Board.objects.count()

    pagecount = count // pagesize
    if count % pagesize != 0:
        pagecount+=1
    startpage = ((currentpage-1)//pageblock)*pageblock+1
    endpage = startpage+pageblock-1

    if endpage > pagecount:
        endpage = pagecount

    starttoend = range(startpage,endpage+1)

    # 게시물 리스트
    boardlist = Board.objects.all().order_by('-groupno','orderno')[startrow-1:startrow-1+pagesize]
    data = {
        'startpage':startpage,
        'endpage':endpage,
        'pageblock':pageblock,
        'pagecount':pagecount,
        'boardlist':boardlist,
        'starttoend':starttoend
    }

    return render(requst, 'board/list.html', data)

def write(request):
    return render(request, 'board/write.html')

# 대표 게시물
def write_one(request):
    board = Board()
    board.title = request.POST['title']
    board.content = request.POST['content']
    # max groupno
    value = Board.objects.aggregate(max_groupno=Max('groupno'))
    max_groupno = 0 if value['max_groupno'] is None else value['max_groupno']
    board.groupno = max_groupno+1
    board.orderno = 1
    board.depth = 1
    board.user_id = request.session['authuser']['id']
    board.save()

    # 기본 1페이지로 이동
    return HttpResponseRedirect('/board/1')

def view(request):
    # 특정 게시물 정보 호출
    Board.objects.filter(id=request.GET['id']).update(hit=F('hit')+1)
    board = Board.objects.get(id=request.GET['id'])
    data = {
        'board':board
    }
    return render(request, 'board/view.html', data)

# 글 수정 페이지 이동
def modify(request):
    board = Board.objects.get(id=request.GET['id'])
    data = {
        'board': board
    }
    return render(request, 'board/modify.html', data)

# 글 수정
def modify_one(request):
    Board.objects.filter(id=request.POST['id']).update(title=request.POST['title'], content=request.POST['content'])
    return HttpResponseRedirect('/board/modify?id='+request.POST['id'])

# 답글 작성 페이지 이동 = 기존 write
def rewrite(request):
    data = {
        'id':request.GET['id']
    }
    return render(request, 'board/rewrite.html', data)

def rewrite_one(request):
    board = Board()
    board.title = request.POST['title']
    board.content = request.POST['content']
    # parent
    parent = Board.objects.get(id=request.POST['parentid'])
    # 같은 그룹 내 update orderno
    Board.objects.filter(groupno=parent.groupno).filter(orderno__gte=parent.orderno+1).update(orderno=F('orderno') + 1)

    # 답글 저장
    board.groupno = parent.groupno
    board.orderno = parent.orderno+1
    board.depth = parent.depth+1
    board.user_id = request.session['authuser']['id']
    board.save()
    return HttpResponseRedirect('/board/1')

def delete(request):
    boardlist = Board.objects.all().filter(groupno=request.GET['groupno']).filter(orderno__gte=request.GET['orderno']).filter(depth__gte=request.GET['depth']).order_by('orderno','depth')
    maxorderno = 1
    # 가장 최상위 글이 아닌 경우
    if request.GET['depth'] != 1 and request.GET['orderno'] != 1:
        # 자기 자신만 삭제하는 경우
        if len(boardlist) == 1:
            maxorderno = boardlist[0].orderno
            print(maxorderno)
        flag = False
        for index, board in enumerate(boardlist):
            # 자기 자신 패스
            if index == 0:
                childdepth = board.depth
                childorderno = board.orderno
            if request.GET['depth'] == childdepth:
                flag = True
                maxorderno = childorderno-1

        if flag == False:
            maxorderno = boardlist[len(boardlist)-1].orderno
    else:
        maxorderno = boardlist[len(boardlist) - 1].orderno

    for index, board in enumerate(boardlist):
        if board.orderno <= maxorderno:
            board.delete()

    return HttpResponseRedirect('/board/1')




























