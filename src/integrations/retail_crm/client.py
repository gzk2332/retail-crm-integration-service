import json
import logging
from typing import Any

import httpx
from fastapi import HTTPException, status

from core.settings import get_settings
from integrations.retail_crm.constants import OK_STATUS_CODES
from integrations.retail_crm.endpoints import Endpoint

logger = logging.getLogger(__name__)

settings = get_settings()


class RetailCRMApiClient:
    CORE_PARAMS = {'page', 'limit', 'apiKey', 'site'}

    def __init__(self) -> None:
        self._api_url = settings.RetailCRM.API_URL
        self._api_prefix = settings.RetailCRM.API_PREFIX
        self._api_version = settings.RetailCRM.API_VERSION
        self._api_key = settings.RetailCRM.API_KEY

    def _make_url(self, endpoint: str) -> str:
        return f'{self._api_url}/{self._api_prefix}/{self._api_version}/{endpoint}'

    async def _make_request(
        self,
        method: str,
        url: str,
        params: dict,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> dict[str, Any]:
        logger.info('Send request to %s with params=%s, data=%s', url, params, data)

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    headers=headers,
                )

        except httpx.ConnectError as err:
            logger.error('RetailCRM connection error: Cannot reach server at %s', url)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='CRM service unavailable'
            ) from err

        except httpx.TimeoutException as err:
            logger.error('RetailCRM timeout error: Request to %s timed out', url)
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail='CRM response timeout') from err

        except Exception as err:
            logger.exception('Unexpected error while calling RetailCRM: %s', err)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal integration error'
            ) from err

        return self._parse_response(response=response)

    def _get_form_headers(self) -> dict[str, str]:
        return {'Content-Type': 'application/x-www-form-urlencoded'}

    def _serialize_payload(self, data: dict) -> dict[str, str]:
        serialized_data = {}

        for key, value in data.items():
            if isinstance(value, dict | list):
                serialized_data[key] = json.dumps(value, ensure_ascii=False)
            else:
                serialized_data[key] = value

        return serialized_data

    def _parse_response(self, response: httpx.Response) -> dict[str, Any]:
        try:
            json_response = response.json()

        except json.JSONDecodeError as exc:
            logger.warning('Decode error: %s', exc)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot decode response') from exc

        if response.status_code not in OK_STATUS_CODES:
            error_msg = json_response.get('errorMsg', 'Request failed')
            logger.warning('HTTP error [%d]: %s', response.status_code, error_msg)
            raise HTTPException(status_code=response.status_code, detail=error_msg)

        if not json_response.get('success', False):
            error_msg = json_response.get('errorMsg', 'RetailCRM error')
            logger.warning('API error: %s', error_msg)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

        return json_response

    def _prepare_params(self, filters: dict[str, Any]) -> dict[str, Any]:
        params = {}
        for key, value in filters.items():
            if key in self.CORE_PARAMS:
                params[key] = value
            else:
                params[f'filter[{key}]'] = value

        return params

    async def make_request(self, data: dict | None, filters: dict | None, endpoint: Endpoint) -> dict[str, Any]:
        url = self._make_url(endpoint=endpoint.path)
        headers = {}
        params = {'apiKey': self._api_key}

        if filters:
            params.update(self._prepare_params(filters=filters))

        method = endpoint.method.upper()
        if method == 'POST' and data:
            headers = self._get_form_headers()
            data = self._serialize_payload(data=data)

        return await self._make_request(data=data, params=params, method=method, url=url, headers=headers)
