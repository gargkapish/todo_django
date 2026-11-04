from django.test import TestCase
from .models import Task

# Create your tests here.

class TaskTest(TestCase):
    def test_add_edit_delete(self):
        self.client.post('/add/', {'title': 'Buy milk', 'description': '2 litres'})
        task = Task.objects.get()
        self.assertEqual(task.description, '2 litres')
        self.assertFalse(task.done)

        self.client.post(f'/edit/{task.id}/', {'title': 'Buy bread', 'description': 'brown', 'done': 'on'})
        task.refresh_from_db()
        self.assertEqual(task.title, 'Buy bread')
        self.assertTrue(task.done)

        self.client.post(f'/edit/{task.id}/', {'title': 'Buy bread', 'description': 'brown'})
        task.refresh_from_db()
        self.assertFalse(task.done)

        self.client.post(f'/toggle/{task.id}/')
        task.refresh_from_db()
        self.assertTrue(task.done)

        self.assertContains(self.client.get('/'), 'Buy bread')

        self.client.post(f'/delete/{task.id}/')
        self.assertEqual(Task.objects.count(), 0)

    def test_empty_state(self):
        self.assertContains(self.client.get('/'), 'No tasks yet.')

    def test_completed_and_pending_shown_differently(self):
        Task.objects.create(title='Done one', done=True)
        Task.objects.create(title='Pending one')
        Task.objects.create(title='Pending two')
        page = self.client.get('/')
        self.assertContains(page, 'My To-Do List')
        self.assertContains(page, 'class="completed"', count=1)
        self.assertContains(page, 'class="pending"', count=2)

    def test_blank_title_rejected(self):
        page = self.client.post('/add/', {'title': '   ', 'description': ''})
        self.assertEqual(page.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)

    def test_get_cannot_toggle_or_delete(self):
        task = Task.objects.create(title='Keep me')
        self.assertEqual(self.client.get(f'/toggle/{task.id}/').status_code, 405)
        self.assertEqual(self.client.get(f'/delete/{task.id}/').status_code, 405)
        task.refresh_from_db()
        self.assertFalse(task.done)
