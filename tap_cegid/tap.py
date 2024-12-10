"""Cegid tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_cegid import streams


class TapCegid(Tap):
    """Cegid tap class."""

    name = "tap-cegid"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "username",
            th.StringType,
            title="Username",
            description="The username to authenticate with the Cegid API.",
        ),
        th.Property(
            "password",
            th.StringType,
            title="Password",
            secret=True,
            description="The password to authenticate with the Cegid API.",
        ),
        th.Property(
            "api_url",
            th.StringType,
            title="API URL",
            description="The URL of the Cegid API client.",
        ),
        th.Property(
            "folder_id",
            th.StringType,
            title="Folder ID",
            description="The folder ID to use for the Cegid API client.",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.CegidStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.CustomerOrdersStream(self),
        ]


if __name__ == "__main__":
    TapCegid.cli()
