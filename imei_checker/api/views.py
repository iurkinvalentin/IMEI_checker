import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import logging
from django.core.cache import cache


def check_imei(imei):
    """Проверяет IMEI через внешний API"""
    headers = {"Authorization": f"Bearer {settings.API_AUTH_TOKEN}"}
    try:
        response = requests.post(settings.IMEI_API_URL,
                                 json={"deviceId": imei, "serviceId": 12},
                                 headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(
            f"IMEI check failed: {e}, "
            f"Response: {getattr(e.response, 'text', 'No response')}")
        return {"error": "Service unavailable"}


@method_decorator(csrf_exempt, name='dispatch')
class IMEICheckView(View):
    """Представление для проверки IMEI через POST-запрос"""
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Проверяем, что обязательные параметры переданы
        if "imei" not in data or not data["imei"]:
            return JsonResponse({"error": "imei is required"}, status=400)

        if "token" not in data or not data["token"]:
            return JsonResponse({"error": "token is required"}, status=400)

        imei = data["imei"]
        token = data["token"]

        if token != settings.API_AUTH_TOKEN:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        if not imei.isdigit() or len(imei) not in [15, 17]:
            return JsonResponse({"error": "Invalid IMEI format"}, status=400)

        if cache.get(f"rate_limit_{imei}"):
            return JsonResponse(
                {"error": "Too many requests, try later"}, status=429)
        cache.set(f"rate_limit_{imei}", True, timeout=5)

        response_data = check_imei(imei)
        return JsonResponse(response_data)
