import base64
import json
from copy import deepcopy
from unittest.mock import patch
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Workbook, Activity, ActivityProgress, Drawing

TEST_STORAGES = deepcopy(settings.STORAGES)
TEST_STORAGES['staticfiles'] = {
    'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
}

SAMPLE_PNG_BASE64 = (
    "data:image/png;base64,"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII="
)


@override_settings(SECURE_SSL_REDIRECT=False, STORAGES=TEST_STORAGES)
class ProgressAndAchievementsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='estudiante1',
            password='password123',
            first_name='Mateo'
        )
        self.client.login(username='estudiante1', password='password123')

        self.wb = Workbook.objects.create(
            title='Lectura Inicial',
            category='lectoescritura',
            grade_level='inicial',
            emoji_icon='1f4d6',
            color_theme='primary',
            order=1,
        )
        self.act1 = Activity.objects.create(
            workbook=self.wb,
            activity_number=1,
            title='Vocal A',
            instruction='Elige la vocal',
            activity_type='fill_vowel',
            correct_answer='A',
        )
        self.act2 = Activity.objects.create(
            workbook=self.wb,
            activity_number=2,
            title='Vocal E',
            instruction='Elige la vocal',
            activity_type='fill_vowel',
            correct_answer='E',
        )

    def test_home_progress_and_achievements(self):
        ActivityProgress.objects.create(user=self.user, activity=self.act1, completed=True)
        response = self.client.get(reverse('activities:home'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['completed_count'], 1)
        self.assertEqual(response.context['total_activities'], 2)
        self.assertEqual(response.context['overall_percentage'], 50)
        self.assertEqual(response.context['unlocked_achievements_count'], 1)

    def test_workbook_list_progress_bar(self):
        ActivityProgress.objects.create(user=self.user, activity=self.act1, completed=True)
        ActivityProgress.objects.create(user=self.user, activity=self.act2, completed=True)
        response = self.client.get(reverse('activities:workbook_list'))

        self.assertEqual(response.status_code, 200)
        wb_context = response.context['workbooks'][0]
        self.assertEqual(wb_context.completed_activities, 2)
        self.assertEqual(wb_context.progress_percent, 100)
        self.assertTrue(wb_context.is_completed)


@override_settings(SECURE_SSL_REDIRECT=False, STORAGES=TEST_STORAGES)
class PrimaryLanguageActivitiesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='primaria1',
            password='password123',
            first_name='Sofía'
        )
        self.client.login(username='primaria1', password='password123')
        self.wb = Workbook.objects.create(
            title='Comprensión Lectora',
            category='comprension',
            grade_level='primaria',
            order=5,
        )

    def test_error_hunter_validation(self):
        act = Activity.objects.create(
            workbook=self.wb,
            activity_number=1,
            title='Cazadores',
            instruction='Corrige',
            activity_type='error_hunter',
            extra_data={
                'segments': [
                    {'text': 'El ', 'is_error': False},
                    {'text': 'cabayo', 'is_error': True, 'correction': 'caballo'},
                ]
            }
        )
        url = reverse('activities:check_activity', args=[act.id])

        bad_res = self.client.post(url, json.dumps({'corrections': {}}), content_type='application/json')
        self.assertFalse(bad_res.json()['correct'])

        ok_res = self.client.post(url, json.dumps({'corrections': {'1': 'caballo'}}), content_type='application/json')
        self.assertTrue(ok_res.json()['correct'])
        self.assertTrue(ActivityProgress.objects.filter(user=self.user, activity=act, completed=True).exists())

    def test_comic_fill_validation(self):
        act = Activity.objects.create(
            workbook=self.wb,
            activity_number=2,
            title='Cómic',
            instruction='Inventa',
            activity_type='comic_fill',
            extra_data={'panels': [{'character_name': 'Luna'}, {'character_name': 'Zorg'}]}
        )
        url = reverse('activities:check_activity', args=[act.id])

        bad_res = self.client.post(url, json.dumps({'dialogues': ['Hola', '']}), content_type='application/json')
        self.assertFalse(bad_res.json()['correct'])

        ok_res = self.client.post(url, json.dumps({'dialogues': ['¡Hola!', '¡Bienvenido!']}), content_type='application/json')
        self.assertTrue(ok_res.json()['correct'])

    def test_word_soup_validation(self):
        act = Activity.objects.create(
            workbook=self.wb,
            activity_number=3,
            title='Sopa',
            instruction='Busca',
            activity_type='word_search',
            extra_data={'mode': 'soup', 'words': [{'word': 'RAIZ'}, {'word': 'FLOR'}]}
        )
        url = reverse('activities:check_activity', args=[act.id])

        ok_res = self.client.post(url, json.dumps({'found_words': ['RAIZ', 'FLOR']}), content_type='application/json')
        self.assertTrue(ok_res.json()['correct'])


@override_settings(SECURE_SSL_REDIRECT=False, STORAGES=TEST_STORAGES)
class DrawingGalleryManagementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='artista1', password='password123')
        self.other_user = User.objects.create_user(username='artista2', password='password123')
        self.client.login(username='artista1', password='password123')

        raw_png = base64.b64decode(SAMPLE_PNG_BASE64.split(';base64,')[1])
        with patch('django.core.files.storage.Storage.save', side_effect=lambda name, content, **kw: name):
            self.drawing1 = Drawing.objects.create(
                user=self.user,
                title='Dibujo 1',
                image=SimpleUploadedFile('d1.png', raw_png, content_type='image/png')
            )
            self.drawing2 = Drawing.objects.create(
                user=self.user,
                title='Dibujo 2',
                image=SimpleUploadedFile('d2.png', raw_png, content_type='image/png')
            )
            self.other_drawing = Drawing.objects.create(
                user=self.other_user,
                title='Ajeno',
                image=SimpleUploadedFile('d3.png', raw_png, content_type='image/png')
            )

    @patch('django.core.files.storage.Storage.delete')
    @patch('django.core.files.storage.Storage.save', side_effect=lambda name, content, **kw: name)
    def test_edit_existing_drawing(self, mock_save, mock_delete):
        url = reverse('activities:save_drawing')
        res = self.client.post(
            url,
            json.dumps({
                'drawing_id': self.drawing1.id,
                'title': 'Dibujo 1 Editado',
                'image': SAMPLE_PNG_BASE64,
            }),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.drawing1.refresh_from_db()
        self.assertEqual(self.drawing1.title, 'Dibujo 1 Editado')
        self.assertEqual(Drawing.objects.filter(user=self.user).count(), 2)

    @patch('django.core.files.storage.Storage.delete')
    def test_delete_selected_drawings(self, mock_delete):
        url = reverse('activities:delete_drawings')
        res = self.client.post(
            url,
            json.dumps({'drawing_ids': [self.drawing1.id, self.other_drawing.id]}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['deleted_count'], 1)
        self.assertFalse(Drawing.objects.filter(id=self.drawing1.id).exists())
        self.assertTrue(Drawing.objects.filter(id=self.drawing2.id).exists())
        self.assertTrue(Drawing.objects.filter(id=self.other_drawing.id).exists())

@override_settings(SECURE_SSL_REDIRECT=False, STORAGES=TEST_STORAGES)
class PrimaryScienceActivitiesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ciencia_primaria',
            password='password123',
            first_name='Valeria'
        )
        self.client.login(username='ciencia_primaria', password='password123')
        self.wb = Workbook.objects.create(
            title='Ciencias y Experimentos',
            category='ciencias',
            grade_level='primaria',
            order=7,
        )

    def test_science_experiment_validation(self):
        act = Activity.objects.create(
            workbook=self.wb,
            activity_number=1,
            title='Huevo Flotante',
            instruction='Experimenta',
            activity_type='science_experiment',
            extra_data={
                'correct_hypothesis': 'El huevo flotará en la superficie.',
                'explanation': 'El agua salada es más densa.'
            }
        )
        url = reverse('activities:check_activity', args=[act.id])

        # Falta observación
        bad_obs = self.client.post(
            url,
            json.dumps({'hypothesis': 'El huevo flotará en la superficie.', 'observation': ''}),
            content_type='application/json'
        )
        self.assertFalse(bad_obs.json()['correct'])

        # Hipótesis correcta y observación registrada
        ok_res = self.client.post(
            url,
            json.dumps({
                'hypothesis': 'El huevo flotará en la superficie.',
                'observation': 'El huevo subió hasta la superficie en el vaso con sal.'
            }),
            content_type='application/json'
        )
        self.assertTrue(ok_res.json()['correct'])
        self.assertIn('densa', ok_res.json()['explanation'])

    def test_category_sort_validation(self):
        act = Activity.objects.create(
            workbook=self.wb,
            activity_number=2,
            title='Vertebrados e Invertebrados',
            instruction='Clasifica',
            activity_type='category_sort',
            extra_data={
                'categories': [
                    {'id': 'c1', 'name': 'Vertebrados'},
                    {'id': 'c2', 'name': 'Invertebrados'},
                ],
                'elements': [
                    {'id': 'e1', 'name': 'Perro', 'category_id': 'c1'},
                    {'id': 'e2', 'name': 'Mariposa', 'category_id': 'c2'},
                ]
            }
        )
        url = reverse('activities:check_activity', args=[act.id])

        bad_res = self.client.post(
            url,
            json.dumps({'assignments': {'e1': 'c2', 'e2': 'c1'}}),
            content_type='application/json'
        )
        self.assertFalse(bad_res.json()['correct'])

        ok_res = self.client.post(
            url,
            json.dumps({'assignments': {'e1': 'c1', 'e2': 'c2'}}),
            content_type='application/json'
        )
        self.assertTrue(ok_res.json()['correct'])