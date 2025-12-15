from django.urls import path, include
from django.conf import settings
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from .views import (
    home,
    login_view,
    logout_view,
    signup_view,
    edit_profile,
    user_profile,
    reset_avatar,
    contact,
    school_map,
    badges,
    community_detail,
    create_post_in_community,
    create_post,
    post_detail,
    toggle_upvote,
    submit_event,
    submit_event_success,
    search,
    feed,
)

urlpatterns = [
    path('', include('myapp.urls')),
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('map/', school_map, name='school_map'),
    path('badges/', badges, name='badges'),

    # Auth
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Redirect old /accounts/login/ to /login/
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=True)),

    # Community
    path('c/<str:name>/', community_detail, name='community_detail'),
    path('c/<str:name>/create/', create_post_in_community, name='create_post_in_community'),

    # Posts
    path('create/', create_post, name='create_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/toggle-upvote/', toggle_upvote, name='toggle_upvote'),

    # Profile
    path('profile/', user_profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/reset-avatar/', reset_avatar, name='reset_avatar'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    
    # Events
    path('events/submit/', submit_event, name='submit_event'),
    path('events/success/', submit_event_success, name='submit_event_success'),

    # Search
    path('search/', search, name='search'),

    # Feed
    path('feed/', feed, name='feed'),
]

# Serve media files in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
