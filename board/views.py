from django.db.models import Max, F
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from board.models import Board, Comment

def list(request):
    # 페이지 번호, 디폴트 = 1페이지
    pagenum = int(request.GET.get('pagenum',1))
    # 검색어, 디폴트 = 공백(전체 게시물)
    kwd = str(request.GET.get('kwd',''))

    # 페이징 처리
    currentpage = pagenum
    pagesize = 5
    pageblock = 3
    startrow = (currentpage-1)*pagesize+1
    # 검색 필터
    count = Board.objects.filter(title__contains=kwd).count()

    pagecount = count // pagesize
    if count % pagesize != 0:
        pagecount+=1
    startpage = ((currentpage-1)//pageblock)*pageblock+1
    endpage = startpage+pageblock-1

    if endpage > pagecount:
        endpage = pagecount

    starttoend = range(startpage,endpage+1)

    # 게시물 리스트 + 검색 필터
    boardlist = Board.objects.all().filter(title__contains=kwd).order_by('-groupno','orderno')[startrow-1:startrow-1+pagesize]
    data = {
        'startpage':startpage,
        'endpage':endpage,
        'pageblock':pageblock,
        'pagecount':pagecount,
        'boardlist':boardlist,
        'starttoend':starttoend,
        'pagenum':pagenum,
        'kwd':kwd
    }

    return render(request, 'board/list.html', data)

def write(request):

    # 인증
    authuser = request.session.get('authuser')
    if authuser is None:
        return HttpResponseRedirect('/board')

    return render(request, 'board/write.html')

# 대표 게시물
def write_one(request):

    # 인증
    authuser = request.session.get('authuser')
    if authuser is None:
        return HttpResponseRedirect('/board')

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
    return HttpResponseRedirect('/board')

# 게시물 보기 + 댓글 등록 및 리스트 추출
def view(request):
    # 특정 게시물 정보 호출
    Board.objects.filter(id=request.GET['id']).update(hit=F('hit')+1)
    board = Board.objects.get(id=request.GET['id'])

    pagenum = int(request.GET.get('pagenum',1))
    kwd = str(request.GET.get('kwd', ''))

    # 댓글 리스트
    commentlist = Comment.objects.all().filter(board_id=request.GET['id'])

    data = {
        'board':board,
        'commentlist':commentlist,
        'pagenum':pagenum,
        'kwd': kwd
    }
    return render(request, 'board/view.html', data)

# 글 수정 페이지 이동
def modify(request):

    # 인증
    authuser = request.session.get('authuser')
    if authuser is None:
        return HttpResponseRedirect('/board')

    board = Board.objects.get(id=request.GET['id'])
    data = {
        'board': board
    }
    return render(request, 'board/modify.html', data)

# 글 수정
def modify_one(request):

    # 인증
    authuser = request.session.get('authuser')
    if authuser is None:
        return HttpResponseRedirect('/board')

    Board.objects.filter(id=request.POST['id']).update(title=request.POST['title'], content=request.POST['content'])
    return HttpResponseRedirect('/board/modify?id='+request.POST['id'])

# 답글 작성 페이지 이동 = 기존 write
def rewrite(request):

    # 인증
    authuser = request.session.get('authuser')
    if authuser is None:
        return HttpResponseRedirect('/board')

    data = {
        'id':request.GET['id']
    }
    return render(request, 'board/rewrite.html', data)

# 답글 작성
def rewrite_one(request):

    # 인증
    authuser = request.session.get('authuser')
    if authuser is None:
        return HttpResponseRedirect('/board')

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
    return HttpResponseRedirect('/board')

# 글 삭제
def delete(request):

    # 인증
    authuser = request.session.get('authuser')
    if authuser is None:
        return HttpResponseRedirect('/board')

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

    return HttpResponseRedirect('/board')

# 댓글 입력 및 삭제
def comment(request, commentid):

    # 인증
    authuser = request.session.get('authuser')
    if authuser is None:
        return HttpResponseRedirect('/board')

    # 댓글 입력
    if commentid is None:
        comment = Comment()
        comment.content = request.GET['content']
        comment.board_id = request.GET['boardid']
        comment.user_id = authuser['id']
        comment.save()
    # 댓글 삭제
    else:
        comment = Comment.objects.get(id=commentid)
        comment.delete()

    # 댓글 리스트 추출
    commentlist = Comment.objects.all().filter(board_id=request.GET['boardid'])

    id = []
    content = []
    regdate = []
    user = []
    for c in commentlist:
        id.append(c.id)
        content.append(c.content)
        regdate.append(c.regdate)
        user.append(c.user.name)

    # json 형태인 dict 자료형으로 리턴
    result={
        'result':'success',
        'id':id,
        'content':content,
        'regdate':regdate,
        'user':user,
        'nowuser':request.session['authuser']['name']
    }

    return JsonResponse(result)

# get, post action 동시 처리
# def test(request, id):
#     if id is None:
#         print("get")
#     else:
#         print("post")
#     pass