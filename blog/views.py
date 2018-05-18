from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Post
import blog.chatlib as chatlib
import re

def chatbot(request):
    global chat_subject, conversation, conversation_id, outputs, this_context, answer_context, answer
    button = ''
    if request.method == "POST":
        input_message = request.POST['q']
        me = User.objects.get(username = 'User')
        Post.objects.create(author=me, text=input_message)
        (outputs, this_context) = chatlib.talk_watson(input_message,conversation,outputs,this_context)
        if answer_context == 'question_receiving':
            answer = '질문이 정상적으로 입력되었습니다. 감사합니다. 혹시 또 궁금하신 것이 있으신가요?'
        elif outputs[0][0]=='[': #코드의 첫번째에 '['가 있으면 선택지가 있는 채팅임
            subjects = chatlib.listing_subject(chat_subject, outputs[0])
            answer = '이 중에서 찾는 질문이 있으면 클릭해주세요.'
            for subject in subjects:
                button += '<button class="button button1" type="submit" name="q" value="'+subject+'">'+subject+'</button>'
            button += '<button class="button button1" type="submit" name="q" value="찾는 질문이 없어요">찾는 질문이 없어요</button>'
        elif input_message=='찾는 질문이 없어요':
            answer = '죄송합니다. 원하시는 질문을 남겨주시면 보완해드리겠습니다.'
            answer_context = 'question_receiving'
        else : # 일반적인 답변
            splited = re.split('\[',outputs[0],1)
            if len(splited) == 1:
                answer = outputs[0]
            else:
                answer = splited[0] + '더 보시겠습니까?'
                subjects = chatlib.listing_subject(chat_subject,'['+splited[1])
                for subject in subjects:
                    button += '<button class="button button1" type="submit" name="q" value="'+subject+'">'+subject+'</button>'
                    #button += '<button class="button button1" type="submit" name="q" value="아니에요. 괜찮습니다.">아니에요. 괜찮습니다.</button>'
        me = User.objects.get(username = '커리어클루')
        Post.objects.create(author=me, text=answer, button = button)
    else:
        Post.objects.all().delete()
        chat_subject = chatlib.import_csv()
        (conversation,conversation_id,outputs,this_context) = chatlib.initialize_watson()
        answer = "무엇이 궁금하신가요? 편하게 말씀해주세요 : )"
        answer_context = ''
        try:
            me = User.objects.get(username = '커리어클루')
        except User.DoesNotExist:
            me = User.objects.create_user(username='커리어클루',email='career@careerclue.com',password='abcd2864')
        Post.objects.create(author=me, text=answer)
    posts = Post.objects.all()
    return render(request, 'blog/chatbot.html', {'posts':posts})

