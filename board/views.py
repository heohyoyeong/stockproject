from django.shortcuts import render, redirect, get_object_or_404
from board.models import Post
from board.forms import PostForm,CommentForm
import xml.etree.ElementTree as ET
import requests
from board import GetStockCode



def board_main_list(request):
    companyNamedict= GetStockCode.Get_CSV_Maching_dict()
    print("bbbbbbb")
    companyName=request.POST.get('machingstock')
    if companyName != None:
        print(companyName)
        xmldict=GetStockCode.Get_XML_maching_dict()
        corpcode=xmldict[companyName]
        print(corpcode)

    main_list = Post.objects.all().order_by('-id')
    context = {'posts': main_list,'companydict':companyNamedict }
    return render(request, 'bbs.html', context)



# def board_search_stock_list(request,):
#     main_list = Post.objects.all().order_by('-id')
#     context = {'posts': main_list }
#     return render(request, 'bbs.html', context)


def board_create(request):
    print('board_create')
    companyNamedict = GetStockCode.Get_CSV_Maching_dict()
    companyName = request.POST.get('machingstock')
    print(companyName)
    xmlDict=GetStockCode.Get_XML_maching_dict()
    match_code=''
    if companyName is not None:
        match_code=xmlDict[companyName]
        print(match_code)


    if request.method == 'POST':
        post_form = PostForm(request.POST)
        print('포스트로 들오온')
        print(post_form.errors)

        if post_form.is_valid():
            print('폼이상')
            if match_code !='':
                print(post_form)
                post_form.fields['maching_code'].value=match_code
                print(post_form.fields['maching_code'].value)
                print('match code set')
                print(post_form)
            post_form.save()
            return redirect('board:bbs_main')

    else:
        post_form = PostForm()
        print('get으로 들어온다 ')

    return render(request, 'bbs_create.html', {'post_form': post_form, 'companydict':companyNamedict})


def board_detail(request,post_id):

    print("디테일함수 들어옴 ")
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        print("디테일 포스트로 들어옴 ")

    else:
        post_form = PostForm(instance=post)
        for i in post_form.fields:  # 수정이 되지 않도록 처리
            post_form.fields[i].disabled = True
        comment_form = CommentForm()
        print("디테일 엘스 들어옴 ")

    return render(request, 'detail.html', {'post_form': post_form, 'post': post, 'comment_form': comment_form})






# def stock_board(request, company_code):
#     main_list = Post.objects.get(company_code).order_by('-id')
#     context = {'posts': main_list}
#     return render(request, 'bbs.html', context)






