from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Campaign


class CampaignStatusTests(TestCase):
    def test_campaign_is_on_track_below_warning_threshold(self):
        campaign = Campaign(name="Search", budget=Decimal("1000.00"), spend=Decimal("500.00"))

        self.assertEqual(campaign.status, Campaign.Status.OK)

    def test_campaign_is_warning_at_or_above_threshold(self):
        campaign = Campaign(name="Search", budget=Decimal("1000.00"), spend=Decimal("900.00"))

        self.assertEqual(campaign.status, Campaign.Status.WARNING)

    def test_campaign_is_overspent_when_spend_exceeds_budget(self):
        campaign = Campaign(name="Search", budget=Decimal("1000.00"), spend=Decimal("1000.01"))

        self.assertEqual(campaign.status, Campaign.Status.OVERSPENT)


class CampaignAPITests(APITestCase):
    def test_create_list_update_and_delete_campaign(self):
        list_url = reverse("campaign-list")

        create_response = self.client.post(
            list_url,
            {
                "name": "Google Ads",
                "budget": "1000.00",
                "spend": "500.00",
            },
            format="json",
        )

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data["status"], Campaign.Status.OK)

        campaign_id = create_response.data["id"]
        detail_url = reverse("campaign-detail", args=[campaign_id])

        list_response = self.client.get(list_url)

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        update_response = self.client.patch(
            detail_url,
            {"spend": "1200.00"},
            format="json",
        )

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["status"], Campaign.Status.OVERSPENT)

        delete_response = self.client.delete(detail_url)

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Campaign.objects.filter(pk=campaign_id).exists())
