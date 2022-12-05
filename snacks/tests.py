from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Snack

class SnackTest(TestCase):
    def test_list_view_status(self):
        url = reverse('snack-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_template(self):
        url = reverse('snack-list')
        response = self.client.get(url)
        self.assertTemplateUsed(response,'snack_list.html')

    def setUp(self):

        self.user=get_user_model().objects.create_user(
            username='asad',
            email='hijjawi30@gmail.com',
            password='admintest111')

        self.snack=Snack.objects.create(
            title='cake',
            description="cake is cake",
            purchaser=self.user 
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "cake")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "cake")
        self.assertEqual(f"{self.snack.purchaser}", "asad")
        self.assertEqual(self.snack.description, "cake is cake")

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cake")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack-detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, "snack_details.html")
    

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack-create"),
            {"title":"nuts","description":"driving me nuts","purchaser": self.user.id,}, follow=True
        )

        self.assertRedirects(response, reverse("snack-detail", args="2"))
        self.assertContains(response, "nuts")

    
    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack-delete", args="1"))
        self.assertEqual(response.status_code, 200)

    
    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack-update", args="1"),
            {"title": "chocolate","description":"yummers","purchaser":self.user.id}
        )

        self.assertRedirects(response, reverse("snack-detail", args="1"))