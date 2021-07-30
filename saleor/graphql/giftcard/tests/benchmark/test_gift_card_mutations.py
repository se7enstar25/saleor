from datetime import date, timedelta

import graphene
import pytest

from .....giftcard.models import GiftCard
from ....tests.utils import get_graphql_content
from ...enums import GiftCardExpiryTypeEnum

CREATE_GIFT_CARD_MUTATION = """
    mutation giftCardCreate(
        $balance: PriceInput!, $userEmail: String, $tag: String,
        $expirySettings: GiftCardExpirySettingsInput!, $note: String
    ){
        giftCardCreate(input: {
                balance: $balance, userEmail: $userEmail, tag: $tag,
                expirySettings: $expirySettings, note: $note }) {
            giftCard {
                id
                code
                displayCode
                isActive
                expiryDate
                expiryType
                expiryPeriod {
                    amount
                    type
                }
                tag
                created
                lastUsedOn
                initialBalance {
                    currency
                    amount
                }
                currentBalance {
                    currency
                    amount
                }
                createdBy {
                    email
                }
                usedBy {
                    email
                }
                createdByEmail
                usedByEmail
                app {
                    name
                }
                product {
                    name
                }
                events {
                    type
                    user {
                        email
                    }
                    app {
                        name
                    }
                    balance {
                        initialBalance {
                            amount
                            currency
                        }
                        oldInitialBalance {
                            amount
                            currency
                        }
                        currentBalance {
                            amount
                            currency
                        }
                        oldCurrentBalance {
                            amount
                            currency
                        }
                    }
                }
            }
            errors {
                field
                message
                code
            }
        }
    }
"""


@pytest.mark.django_db
@pytest.mark.count_queries(autouse=False)
def test_create_never_expiry_gift_card(
    staff_api_client,
    customer_user,
    permission_manage_gift_card,
    permission_manage_users,
    permission_manage_apps,
    count_queries,
):
    # given
    initial_balance = 100
    currency = "USD"
    expiry_type = GiftCardExpiryTypeEnum.NEVER_EXPIRE.name
    tag = "gift-card-tag"
    variables = {
        "balance": {
            "amount": initial_balance,
            "currency": currency,
        },
        "userEmail": customer_user.email,
        "tag": tag,
        "note": "This is gift card note that will be save in gift card event.",
        "expirySettings": {
            "expiryType": expiry_type,
        },
    }

    # when
    response = staff_api_client.post_graphql(
        CREATE_GIFT_CARD_MUTATION,
        variables,
        permissions=[
            permission_manage_gift_card,
            permission_manage_users,
            permission_manage_apps,
        ],
    )

    # then
    content = get_graphql_content(response)
    data = content["data"]["giftCardCreate"]["giftCard"]

    assert data


UPDATE_GIFT_CARD_MUTATION = """
    mutation giftCardUpdate(
        $id: ID!, $input: GiftCardUpdateInput!
    ){
        giftCardUpdate(id: $id, input: $input) {
            giftCard {
                id
                code
                displayCode
                isActive
                expiryDate
                expiryType
                expiryPeriod {
                    amount
                    type
                }
                tag
                created
                lastUsedOn
                initialBalance {
                    currency
                    amount
                }
                currentBalance {
                    currency
                    amount
                }
                createdBy {
                    email
                }
                usedBy {
                    email
                }
                createdByEmail
                usedByEmail
                app {
                    name
                }
                product {
                    name
                }
                events {
                    type
                    user {
                        email
                    }
                    app {
                        name
                    }
                    balance {
                        initialBalance {
                            amount
                            currency
                        }
                        oldInitialBalance {
                            amount
                            currency
                        }
                        currentBalance {
                            amount
                            currency
                        }
                        oldCurrentBalance {
                            amount
                            currency
                        }
                    }
                    expiry {
                        expiryType
                        oldExpiryType
                        expiryPeriod {
                            type
                            amount
                        }
                        oldExpiryPeriod {
                            type
                            amount
                        }
                        expiryDate
                        oldExpiryDate
                    }
                }
            }
            errors {
                field
                message
                code
            }
        }
    }
"""


@pytest.mark.django_db
@pytest.mark.count_queries(autouse=False)
def test_update_gift_card(
    staff_api_client,
    gift_card,
    permission_manage_gift_card,
    permission_manage_users,
    permission_manage_apps,
    count_queries,
):
    # given
    initial_balance = 100.0
    expiry_type = GiftCardExpiryTypeEnum.EXPIRY_DATE.name
    date_value = date.today() + timedelta(days=365)
    tag = "new-gift-card-tag"
    variables = {
        "id": graphene.Node.to_global_id("GiftCard", gift_card.pk),
        "input": {
            "balanceAmount": initial_balance,
            "tag": tag,
            "expirySettings": {
                "expiryType": expiry_type,
                "expiryDate": date_value,
            },
        },
    }

    # when
    response = staff_api_client.post_graphql(
        UPDATE_GIFT_CARD_MUTATION,
        variables,
        permissions=[
            permission_manage_gift_card,
            permission_manage_users,
            permission_manage_apps,
        ],
    )

    # then
    content = get_graphql_content(response)
    data = content["data"]["giftCardUpdate"]["giftCard"]
    assert data


MUTATION_GIFT_CARD_BULK_ACTIVATE = """
    mutation GiftCardBulkActivate($ids: [ID]!) {
        giftCardBulkActivate(ids: $ids) {
            count
            errors {
                code
                field
            }
        }
    }
"""


@pytest.mark.django_db
@pytest.mark.count_queries(autouse=False)
def test_gift_card_bulk_activate_by_staff(
    staff_api_client,
    gift_cards_for_benchmarks,
    permission_manage_gift_card,
    count_queries,
):
    # given
    for card in gift_cards_for_benchmarks:
        card.is_active = False
    GiftCard.objects.bulk_update(gift_cards_for_benchmarks, ["is_active"])

    ids = [
        graphene.Node.to_global_id("GiftCard", card.pk)
        for card in gift_cards_for_benchmarks
    ]
    variables = {"ids": ids}

    # when
    response = staff_api_client.post_graphql(
        MUTATION_GIFT_CARD_BULK_ACTIVATE,
        variables,
        permissions=(permission_manage_gift_card,),
    )

    # then
    content = get_graphql_content(response)
    assert content["data"]["giftCardBulkActivate"]["count"] == len(ids)
