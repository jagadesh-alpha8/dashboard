from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.dashboard,
        name='cctv_dashboard'
    ),

    path(
        'add-branch/',
        views.add_branch,
        name='add_branch'
    ),

    path(
        'add-camera/',
        views.add_camera,
        name='add_camera'
    ),
    path(
        'camera/<int:id>/',
        views.camera_detail,
        name='camera_detail'
    ),
    path(
        'edit-camera/<int:id>/',
        views.edit_camera,
        name='edit_camera'
    ),
    path(
        'delete-camera/<int:id>/',
        views.delete_camera,
        name='delete_camera'
    ),
    path(
        'toggle-active/<int:id>/',
        views.toggle_camera_active,
        name='toggle_camera_active'
    )
]