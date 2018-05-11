from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm
from .forms import ChatForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
import blog.chatlib as chatlib

def post_list(request):
	posts = Post.objects.all()
	return render(request, 'blog/post_list.html', {'posts':posts})

def chatbot(request):
    if request.method == "POST":
        input_message = request.POST['q']
        me = User.objects.get(username = 'User')
        Post.objects.create(author=me, title='', text=input_message)
        chat_subject = chatlib.import_csv()
        (conversation,conversation_id,outputs,this_context) = chatlib.initialize_watson()
        (outputs, this_context) = chatlib.talk_watson(input_message,conversation,outputs,this_context)
        me = User.objects.get(username = '커리어클루')
        Post.objects.create(author=me, title='', text=outputs[0])
    else:
        Post.objects.all().delete()
        chat_subject = chatlib.import_csv()
        (conversation,conversation_id,outputs,this_context) = chatlib.initialize_watson()
        (outputs, this_context) = chatlib.talk_watson('안녕하세요',conversation,outputs,this_context)
        try:
            me = User.objects.get(username = '커리어클루')
        except User.DoesNotExist:
            me = User.objects.create_user(username='커리어클루',email='career@careerclue.com',password='abcd2864')
        Post.objects.create(author=me, title='', text=outputs[0])
    posts = Post.objects.all()
    return render(request, 'blog/chatbot.html', {'posts':posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post':post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        post = form.save(commit=False)
        post.published_date = timezone.now()
        post.author = User.objects.get(username = 'admin')
        post.save()
        return redirect('post_detail', pk=post.pk) #render(request, 'blog/post_edit.html', {'form': form})
        #return redirect('post_detail', pk=post.pk)
    else:
        print('else')
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance = post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail',pk=post.pk)
	else:
		form = PostForm(instance = post)
	return render(request, 'blog/post_edit.html', {'form':form})

def create(request):
    if request.method=='POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/feedback/list')
    else:
        form = FeedbackForm()
 
    return render(request, 'feedback.html', {'form': form})


