import graphene

from ...checkout import AddressType

AddressTypeEnum = graphene.Enum(
    'AddressTypeEnum',
    [(code.upper(), code) for code, name in AddressType.CHOICES])
