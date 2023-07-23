from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Snack
from django.urls import reverse

class SnackTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'test',
            email= 'test@test.com',
            password = 'test@12345'
        )
        self.snack = Snack.objects.create(
            title = "Wings",
            description="with hot sauce",
            purchaser = self.user,
        )
        
    def test_str_method(self):
        self.assertEqual(str(self.snack),'Wings')
        
    def test_detail_view(self):
        url = reverse('snack_detail',args=[self.snack.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'snack_detail.html')
        
    def test_create_view(self):
        url = reverse('snack_create')
        data={
            "title":"Wings",
            "description":"with hot sauce",
            "purchaser":self.user.id
        }
        response = self.client.post(path = url, data = data, follow = True)
        self.assertTemplateUsed(response, 'snack_detail.html')
        self.assertEqual(len(Snack.objects.all()),2)
        self.assertRedirects(response, reverse('snack_detail',args=[2]))
        
    def test_update_view(self):
        url = reverse('snack_update', args=[self.snack.id])
        data = {
            "title": "Updated Wings",
            "description": "Updated description",
            "purchaser": self.user.id
        }
        response = self.client.post(url, data=data, follow=True)
        self.assertRedirects(response, reverse('snack_list'))
        

    def test_delete_view(self):
        url = reverse('snack_delete', args=[self.snack.id])
        response = self.client.post(url, follow=True)
        self.assertTemplateUsed(response, 'snack_list.html')
        self.assertEqual(len(Snack.objects.all()), 0)