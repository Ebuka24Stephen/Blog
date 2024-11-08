from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib import messages
from  django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

@login_required(login_url="user/login/")
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'my_posts.html', {'posts':posts})


@login_required(login_url="user/login/")
def post_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'post_list.html', {'posts':posts})

@login_required(login_url="user/login/")
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    total_like = post.total_likes()
    comments = post.comments.all()
    comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            if request.headers.get('HX-Request') == 'true':
                response = JsonResponse({"message":"Comment added"})
                response['HX-Refresh'] = "true"
                return response
            return redirect('post_detail')        
        else:
            messages.error(request, 'Error')
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post':post, 'form':form, 'comments':comments, 'comment':comment, 'total_like':total_like})
@login_required(login_url="user/login/")

def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this post.')
        if request.headers.get('HX-Request') == 'true':
            response = JsonResponse({"message": "Can't update this post"})
            response['HX-Refresh'] = "true"  
            return response
        return redirect('post_list')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            if request.headers.get('HX-Request') == 'true':
                response = JsonResponse({"message": "Post Updated"})
                response['HX-Refresh'] = "true"  
                return response
            return redirect('post_list')

        else:
            messages.error(request, 'Error updating post.')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_update.html', {'form': form, 'post': post})




def search_post(request):
    query = request.GET.get('q', '')
    if query:
        results = Post.objects.filter(title__icontains=query)
    else:
        results = Post.objects.none()
    return render(request, "search_results.html", {"results": results})


@login_required(login_url="user/login/")
def post_like(request, id):
    post = get_object_or_404(Post, id=id)  
    if request.user not in post.like.all():
        post.like.add(request.user)  
        
    else:
        post.like.remove(request.user)
    if request.headers.get('HX-Request') == 'true':
        response = JsonResponse({"message": "Post Liked"})
        response['HX-Refresh'] = "true"  
        return response
    response = JsonResponse({"message": "Post Liked"})

    
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    post_id = comment.post.id  
    comment.delete()
    if request.headers.get('HX-Request') == 'true':
        response = JsonResponse({"message": "Post Liked"})
        response['HX-Refresh'] = "true"  
        return response
    return redirect('post_detail', post_id=post_id)


@login_required(login_url="user/login/")
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES) 
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user 
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('post_list')
        else:
            messages.error(request, "Error creating post. Please correct the errors below.")
    else:
        form = PostForm()  

    return render(request, 'create_post.html', {'form': form})
