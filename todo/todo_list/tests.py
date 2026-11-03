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
