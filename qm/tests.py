from django.test import TestCase
from django.urls import reverse


class HistoryViewTests(TestCase):
    def test_history_page_renders(self):
        response = self.client.get(reverse("history"))
        self.assertEqual(response.status_code, 200)


class HomeViewTests(TestCase):
    def test_home_page_shows_step_by_step_visualization(self):
        response = self.client.post(
            reverse("home"),
            {
                "variable_count": 4,
                "minterms": "0,1,2,5,7,8,9,10,13",
                "dont_cares": "3,4,11,12",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Step-by-step Visualization")
        self.assertContains(response, "Initial Grouping")
        self.assertContains(response, "Final Boolean Expression")

    def test_duplicate_minterms_and_overlap_are_rejected(self):
        response = self.client.post(
            reverse("home"),
            {
                "variable_count": 3,
                "minterms": "0,1,1",
                "dont_cares": "1",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Duplicate minterms are not allowed")
        self.assertContains(response, "Minterms and don't cares cannot overlap")

    def test_out_of_range_values_are_rejected(self):
        response = self.client.post(
            reverse("home"),
            {
                "variable_count": 2,
                "minterms": "0,4",
                "dont_cares": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Value 4 is outside the allowed range")
