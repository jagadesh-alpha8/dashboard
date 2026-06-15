from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Branch, Camera
from .forms import BranchForm, CameraForm


def dashboard(request):
    branches = Branch.objects.all()
    cameras = Camera.objects.all()
    selected_branch = None
    branch_id = request.GET.get('branch')
    
    if branch_id:
        selected_branch = get_object_or_404(Branch, id=branch_id)

    return render(
        request,
        'cctv/dashboard.html',
        {
            'branches': branches,
            'cameras': cameras,
            'selected_branch': selected_branch
        }
    )


def add_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'branch': {
                        'id': branch.id,
                        'name': branch.name
                    }
                })
            return redirect('cctv_dashboard')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                }, status=400)
    else:
        form = BranchForm()

    return render(
        request,
        'cctv/add_branch.html',
        {'form': form}
    )


def add_camera(request):
    if request.method == 'POST':
        form = CameraForm(request.POST)
        if form.is_valid():
            camera = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'camera': {
                        'id': camera.id,
                        'name': camera.name,
                        'rtsp_url': camera.rtsp_url,
                        'active': camera.active,
                        'branch_id': camera.branch.id,
                        'mediamtx_path': camera.mediamtx_path
                    }
                })
            return redirect('cctv_dashboard')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                }, status=400)
    else:
        form = CameraForm()

    return render(
        request,
        'cctv/add_camera.html',
        {'form': form}
    )


def edit_camera(request, id):
    camera = get_object_or_404(Camera, id=id)
    if request.method == 'POST':
        form = CameraForm(request.POST, instance=camera)
        if form.is_valid():
            camera = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'camera': {
                        'id': camera.id,
                        'name': camera.name,
                        'rtsp_url': camera.rtsp_url,
                        'active': camera.active,
                        'branch_id': camera.branch.id,
                        'mediamtx_path': camera.mediamtx_path
                    }
                })
            return redirect('cctv_dashboard')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                }, status=400)
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'camera': {
                    'id': camera.id,
                    'name': camera.name,
                    'rtsp_url': camera.rtsp_url,
                    'active': camera.active,
                    'branch_id': camera.branch.id,
                    'mediamtx_path': camera.mediamtx_path
                }
            })
        form = CameraForm(instance=camera)

    return render(
        request,
        'cctv/add_camera.html',
        {'form': form, 'edit': True, 'camera': camera}
    )


@require_POST
def delete_camera(request, id):
    camera = get_object_or_404(Camera, id=id)
    camera.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect('cctv_dashboard')


@require_POST
def toggle_camera_active(request, id):
    camera = get_object_or_404(Camera, id=id)
    camera.active = not camera.active
    camera.save()
    return JsonResponse({
        'status': 'success',
        'active': camera.active
    })


def camera_detail(request, id):
    camera = get_object_or_404(Camera, id=id)
    return render(
        request,
        'cctv/camera_detail.html',
        {
            'camera': camera
        }
    )