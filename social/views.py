from .models import User, Post, Comment, Follow, Like, Notification
from django.shortcuts import render, redirect

def splash(request):
    return render(request,'splash.html')

def login(request):

    message = ""

    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']

        try:

            user = User.objects.get(
                email=email,
                password=password
            )

            request.session['user_id'] = user.id

            return redirect('/home/')

        except User.DoesNotExist:

            message = "Invalid email or password"

    return render(
        request,
        'login.html',
        {'message': message}
    )
def register(request):

    message = ""

    if request.method == 'POST':

        name = request.POST['name']

        email = request.POST['email']

        password = request.POST['password']

        User.objects.create(

            name=name,

            email=email,

            password=password

        )

        message = "Account created successfully 🎉"

    return render(

        request,

        'register.html',

        {'message': message}

    )
def home(request):

    current_user_id = request.session.get('user_id')

    if not current_user_id:
        return redirect('/login/')

    current_user = User.objects.get(id=current_user_id)

    if request.method == 'POST':

        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

        if content or image:

            Post.objects.create(
                user=current_user,
                content=content,
                image=image
            )

    following_ids = Follow.objects.filter(
        follower=current_user
    ).values_list('following_id', flat=True)

    posts = Post.objects.filter(
        user__id__in=list(following_ids) + [current_user.id]
    ).order_by('-created_at')

    return render(
        request,
        'home.html',
        {
            'posts': posts,
            'comments': Comment.objects.all()
        }
    )
def like_post(request, post_id):

    current_user_id = request.session.get('user_id')

    if not current_user_id:
        return redirect('/login/')

    current_user = User.objects.get(id=current_user_id)

    post = Post.objects.get(id=post_id)

    like = Like.objects.filter(
        user=current_user,
        post=post
    )

    if like.exists():

        like.delete()

        if post.likes > 0:
            post.likes -= 1

    else:

        Like.objects.create(
            user=current_user,
            post=post
        )

        post.likes += 1

        if post.user != current_user:

            Notification.objects.create(
                user=post.user,
                sender=current_user,
                message=f"{current_user.name} liked your post."
            )

    post.save()

    return redirect('/home/')
def add_comment(request, post_id):

    if request.method == 'POST':

        text = request.POST['text'].strip()

        if text:

            post = Post.objects.get(id=post_id)

            Comment.objects.create(
                post=post,
                text=text
            )

            current_user = User.objects.get(
                id=request.session['user_id']
            )

            if post.user != current_user:

                Notification.objects.create(
                    user=post.user,
                    sender=current_user,
                    message=f"{current_user.name} commented on your post."
                )

    return redirect('/home/')
def logout(request):

    request.session.flush()

    return redirect('/login/')

def profile(request, user_id):

    profile_user = User.objects.get(id=user_id)

    posts = Post.objects.filter(user=profile_user)

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    current_user_id = request.session.get('user_id')

    is_own_profile = False
    is_following = False

    if current_user_id:

        current_user = User.objects.get(id=current_user_id)

        if current_user.id == profile_user.id:
            is_own_profile = True
        else:
            is_following = Follow.objects.filter(
                follower=current_user,
                following=profile_user
            ).exists()

    return render(
        request,
        'profile.html',
        {
            'profile_user': profile_user,
            'posts': posts,
            'followers_count': followers_count,
            'following_count': following_count,
            'is_own_profile': is_own_profile,
            'is_following': is_following,
        }
    )
def edit_profile(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/login/')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':

        user.name = request.POST['name']
        user.bio = request.POST['bio']

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()

        return redirect(f'/profile/{user.id}/')

    return render(
        request,
        'edit_profile.html',
        {
            'user': user
        }
    )

def follow_user(request, user_id):

    if request.method != "POST":
        return redirect("/search/")

    current_user_id = request.session.get('user_id')

    if not current_user_id:
        return redirect('/login/')

    current_user = User.objects.get(id=current_user_id)
    target_user = User.objects.get(id=user_id)

    if current_user != target_user:

        follow = Follow.objects.filter(
            follower=current_user,
            following=target_user
        )

        if follow.exists():

            follow.delete()

        else:

            Follow.objects.create(
                follower=current_user,
                following=target_user
            )

            Notification.objects.create(
                user=target_user,
                sender=current_user,
                message=f"{current_user.name} started following you."
            )

    return redirect(f"/profile/{user_id}/")
def search(request):

    current_user_id = request.session.get('user_id')

    if not current_user_id:
        return redirect('/login/')

    query = request.GET.get('q', '')

    if query:
        users = User.objects.exclude(
            id=current_user_id
        ).filter(
            name__icontains=query
        )
    else:
        users = User.objects.none()

    return render(
        request,
        'search.html',
        {
            'users': users,
            'query': query
        }
    )
def delete_post(request, post_id):

    current_user_id = request.session.get('user_id')

    if not current_user_id:
        return redirect('/login/')

    post = Post.objects.get(id=post_id)

    if post.user.id == current_user_id:
        post.delete()

    return redirect('/home/')
def edit_post(request, post_id):

    current_user_id = request.session.get('user_id')

    if not current_user_id:
        return redirect('/login/')

    post = Post.objects.get(id=post_id)

    if post.user.id != current_user_id:
        return redirect('/home/')

    if request.method == 'POST':
        post.content = request.POST['content']
        post.save()
        return redirect('/home/')

    return render(
        request,
        'edit_post.html',
        {
            'post': post
        }
    )
def notifications(request):

    current_user_id = request.session.get('user_id')

    if not current_user_id:
        return redirect('/login/')

    current_user = User.objects.get(id=current_user_id)

    notifications = Notification.objects.filter(
        user=current_user
    ).order_by('-created_at')

    return render(
        request,
        'notifications.html',
        {
            'notifications': notifications
        }
    )
def followers(request, user_id):

    user = User.objects.get(id=user_id)

    followers = Follow.objects.filter(
        following=user
    )

    return render(
        request,
        'followers.html',
        {
            'profile_user': user,
            'followers': followers
        }
    )


def following(request, user_id):

    user = User.objects.get(id=user_id)

    following = Follow.objects.filter(
        follower=user
    )

    return render(
        request,
        'following.html',
        {
            'profile_user': user,
            'following': following
        }
    )