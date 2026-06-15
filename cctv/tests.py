from django.test import TestCase
from .models import Branch, Camera
from .forms import CameraForm

class CCTVTestCase(TestCase):
    def setUp(self):
        self.branch = Branch.objects.create(name="Test Branch")

    def test_camera_mediamtx_path(self):
        camera = Camera.objects.create(
            branch=self.branch,
            name="Main Entrance Camera",
            rtsp_url="rtsp://example.com/stream"
        )
        self.assertEqual(camera.mediamtx_path, "main-entrance-camera")

    def test_camera_form_valid(self):
        form_data = {
            'branch': self.branch.id,
            'name': 'Office Cam',
            'rtsp_url': 'rtsp://example.com/office',
            'active': True
        }
        form = CameraForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_toggle_camera_active(self):
        camera = Camera.objects.create(
            branch=self.branch,
            name="Toggle Cam",
            rtsp_url="rtsp://example.com/stream",
            active=True
        )
        response = self.client.post(f'/cctv/toggle-active/{camera.id}/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Camera.objects.get(id=camera.id).active)

    def test_delete_camera(self):
        camera = Camera.objects.create(
            branch=self.branch,
            name="Delete Cam",
            rtsp_url="rtsp://example.com/stream"
        )
        response = self.client.post(f'/cctv/delete-camera/{camera.id}/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Camera.objects.filter(id=camera.id).exists())

    def test_edit_camera_ajax_get(self):
        camera = Camera.objects.create(
            branch=self.branch,
            name="Edit Cam",
            rtsp_url="rtsp://example.com/stream",
            active=True
        )
        response = self.client.get(f'/cctv/edit-camera/{camera.id}/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['camera']['name'], 'Edit Cam')


