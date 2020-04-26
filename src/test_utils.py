"""Module with test utilities."""

from aiohttp.test_utils import TestClient as AIOHTTPTestClient


class TestClient(AIOHTTPTestClient):

    headers = {}

    async def _request(self, method, path, **kwargs):
        """
        Apply self.headers to request's headers.
        It really helpful if you need to send some headers on each request.
        """
        headers = kwargs.pop('headers', {})
        headers.update(self.headers)

        resp = await self._session.request(
            method, self.make_url(path), headers=headers, **kwargs
        )
        # save it to close later
        self._responses.append(resp)
        return resp
