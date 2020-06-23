from django.urls import path
from .views.character_views import Characters, CharacterDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
	# Restful routing
    path('characters/', Characters.as_view(), name='characters'),
    path('characters/<int:pk>/', CharacterDetail.as_view(), name='character_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
