"""Stream type classes for tap-cegid."""

from __future__ import annotations

from singer_sdk import typing as th

from tap_cegid.client import CegidStream


class CustomerOrdersStream(CegidStream):
    """Cegid customer orders stream."""

    name = "customer-orders"
    path = "/customer-documents/v1?documentType=CustomerOrder"

    schema = th.PropertiesList(
        th.Property(
            "header",
            th.ObjectType(
                th.Property(
                    "active",
                    th.BooleanType,
                    description="Whether the customer order is active.",
                ),
                th.Property(
                    "storeId",
                    th.StringType,
                    description="The store ID.",
                ),
            ),
            description="Customer order headers.",
        ),
    ).to_dict()
