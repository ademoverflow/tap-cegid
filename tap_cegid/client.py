"""REST client handling, including CegidStream base class."""

from __future__ import annotations

import decimal
import typing as t

from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseOffsetPaginator
from singer_sdk.streams import RESTStream

from tap_cegid.utils.authenticate import get_token

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class CegidPaginator(BaseOffsetPaginator):
    """Cegid paginator class."""

    def has_more(self, response: requests.Response) -> bool:
        """Check if there are more records to fetch."""
        data = response.json()
        return len(data) > 0


class CegidStream(RESTStream):
    """Cegid stream class."""

    # Update this value if necessary or override `parse_response`.
    records_jsonpath = "$[*]"

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return f"{self.config['api_url']}/{self.config['folder_id']}/api"

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        tokens = get_token(
            self.config.get("username", ""),
            self.config.get("password", ""),
        )

        if not tokens:
            message = "No tokens were returned from the API."
            raise RuntimeError(message)
        access_token = tokens.get("access_token", None)

        if not access_token:
            message = "No access token was returned from the API."
            raise RuntimeError(message)

        return BearerTokenAuthenticator.create_for_stream(self, token=access_token)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")  # noqa: ERA001
        return {
            "Content-Type": "application/json",
        }

    def get_new_paginator(self) -> BaseOffsetPaginator:
        """Return a new paginator object."""
        return CegidPaginator(start_value=0, page_size=100)

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        # Parse response body and return a set of records.
        yield from extract_jsonpath(
            self.records_jsonpath,
            input=response.json(parse_float=decimal.Decimal),
        )

    def post_process(
        self,
        row: dict,
        context: Context | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # Delete this method if not needed.
        return row
