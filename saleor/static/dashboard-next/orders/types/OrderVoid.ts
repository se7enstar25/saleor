/* tslint:disable */
// This file was automatically generated and should not be edited.

import { OrderEventsEmails, OrderEvents, FulfillmentStatus, PaymentChargeStatusEnum, OrderStatus, OrderAction } from "./../../types/globalTypes";

// ====================================================
// GraphQL mutation operation: OrderVoid
// ====================================================

export interface OrderVoid_orderVoid_order_billingAddress_country {
  __typename: "CountryDisplay";
  code: string;
  country: string;
}

export interface OrderVoid_orderVoid_order_billingAddress {
  __typename: "Address";
  city: string;
  cityArea: string;
  companyName: string;
  country: OrderVoid_orderVoid_order_billingAddress_country;
  countryArea: string;
  firstName: string;
  id: string;
  lastName: string;
  phone: string | null;
  postalCode: string;
  streetAddress1: string;
  streetAddress2: string;
}

export interface OrderVoid_orderVoid_order_events_user {
  __typename: "User";
  email: string;
}

export interface OrderVoid_orderVoid_order_events {
  __typename: "OrderEvent";
  id: string;
  amount: number | null;
  date: any | null;
  email: string | null;
  emailType: OrderEventsEmails | null;
  message: string | null;
  quantity: number | null;
  type: OrderEvents | null;
  user: OrderVoid_orderVoid_order_events_user | null;
}

export interface OrderVoid_orderVoid_order_fulfillments_lines_edges_node_orderLine_unitPrice_gross {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderVoid_orderVoid_order_fulfillments_lines_edges_node_orderLine_unitPrice_net {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderVoid_orderVoid_order_fulfillments_lines_edges_node_orderLine_unitPrice {
  __typename: "TaxedMoney";
  gross: OrderVoid_orderVoid_order_fulfillments_lines_edges_node_orderLine_unitPrice_gross;
  net: OrderVoid_orderVoid_order_fulfillments_lines_edges_node_orderLine_unitPrice_net;
}

export interface OrderVoid_orderVoid_order_fulfillments_lines_edges_node_orderLine {
  __typename: "OrderLine";
  id: string;
  productName: string;
  productSku: string;
  quantity: number;
  quantityFulfilled: number;
  unitPrice: OrderVoid_orderVoid_order_fulfillments_lines_edges_node_orderLine_unitPrice | null;
  thumbnailUrl: string | null;
}

export interface OrderVoid_orderVoid_order_fulfillments_lines_edges_node {
  __typename: "FulfillmentLine";
  id: string;
  quantity: number;
  orderLine: OrderVoid_orderVoid_order_fulfillments_lines_edges_node_orderLine;
}

export interface OrderVoid_orderVoid_order_fulfillments_lines_edges {
  __typename: "FulfillmentLineCountableEdge";
  node: OrderVoid_orderVoid_order_fulfillments_lines_edges_node;
}

export interface OrderVoid_orderVoid_order_fulfillments_lines {
  __typename: "FulfillmentLineCountableConnection";
  edges: OrderVoid_orderVoid_order_fulfillments_lines_edges[];
}

export interface OrderVoid_orderVoid_order_fulfillments {
  __typename: "Fulfillment";
  id: string;
  lines: OrderVoid_orderVoid_order_fulfillments_lines | null;
  fulfillmentOrder: number;
  status: FulfillmentStatus;
  trackingNumber: string;
}

export interface OrderVoid_orderVoid_order_lines_unitPrice_gross {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderVoid_orderVoid_order_lines_unitPrice_net {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderVoid_orderVoid_order_lines_unitPrice {
  __typename: "TaxedMoney";
  gross: OrderVoid_orderVoid_order_lines_unitPrice_gross;
  net: OrderVoid_orderVoid_order_lines_unitPrice_net;
}

export interface OrderVoid_orderVoid_order_lines {
  __typename: "OrderLine";
  id: string;
  productName: string;
  productSku: string;
  quantity: number;
  quantityFulfilled: number;
  unitPrice: OrderVoid_orderVoid_order_lines_unitPrice | null;
  thumbnailUrl: string | null;
}

export interface OrderVoid_orderVoid_order_shippingAddress_country {
  __typename: "CountryDisplay";
  code: string;
  country: string;
}

export interface OrderVoid_orderVoid_order_shippingAddress {
  __typename: "Address";
  city: string;
  cityArea: string;
  companyName: string;
  country: OrderVoid_orderVoid_order_shippingAddress_country;
  countryArea: string;
  firstName: string;
  id: string;
  lastName: string;
  phone: string | null;
  postalCode: string;
  streetAddress1: string;
  streetAddress2: string;
}

export interface OrderVoid_orderVoid_order_shippingMethod {
  __typename: "ShippingMethod";
  id: string;
}

export interface OrderVoid_orderVoid_order_shippingPrice_gross {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderVoid_orderVoid_order_shippingPrice {
  __typename: "TaxedMoney";
  gross: OrderVoid_orderVoid_order_shippingPrice_gross;
}

export interface OrderVoid_orderVoid_order_subtotal_gross {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderVoid_orderVoid_order_subtotal {
  __typename: "TaxedMoney";
  gross: OrderVoid_orderVoid_order_subtotal_gross;
}

export interface OrderVoid_orderVoid_order_total_gross {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderVoid_orderVoid_order_total_tax {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderVoid_orderVoid_order_total {
  __typename: "TaxedMoney";
  gross: OrderVoid_orderVoid_order_total_gross;
  tax: OrderVoid_orderVoid_order_total_tax;
}

export interface OrderVoid_orderVoid_order_totalAuthorized {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderVoid_orderVoid_order_totalCaptured {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderVoid_orderVoid_order_user {
  __typename: "User";
  id: string;
  email: string;
}

export interface OrderVoid_orderVoid_order_availableShippingMethods_price {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderVoid_orderVoid_order_availableShippingMethods {
  __typename: "ShippingMethod";
  id: string;
  name: string;
  price: OrderVoid_orderVoid_order_availableShippingMethods_price | null;
}

export interface OrderVoid_orderVoid_order {
  __typename: "Order";
  id: string;
  billingAddress: OrderVoid_orderVoid_order_billingAddress | null;
  created: any;
  events: (OrderVoid_orderVoid_order_events | null)[] | null;
  fulfillments: (OrderVoid_orderVoid_order_fulfillments | null)[];
  lines: (OrderVoid_orderVoid_order_lines | null)[];
  number: string | null;
  paymentStatus: PaymentChargeStatusEnum | null;
  shippingAddress: OrderVoid_orderVoid_order_shippingAddress | null;
  shippingMethod: OrderVoid_orderVoid_order_shippingMethod | null;
  shippingMethodName: string | null;
  shippingPrice: OrderVoid_orderVoid_order_shippingPrice | null;
  status: OrderStatus;
  subtotal: OrderVoid_orderVoid_order_subtotal | null;
  total: OrderVoid_orderVoid_order_total | null;
  actions: (OrderAction | null)[];
  totalAuthorized: OrderVoid_orderVoid_order_totalAuthorized;
  totalCaptured: OrderVoid_orderVoid_order_totalCaptured;
  user: OrderVoid_orderVoid_order_user | null;
  userEmail: string | null;
  availableShippingMethods: (OrderVoid_orderVoid_order_availableShippingMethods | null)[] | null;
}

export interface OrderVoid_orderVoid {
  __typename: "OrderVoid";
  order: OrderVoid_orderVoid_order | null;
}

export interface OrderVoid {
  orderVoid: OrderVoid_orderVoid | null;
}

export interface OrderVoidVariables {
  id: string;
}
