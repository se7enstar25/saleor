/* tslint:disable */
// This file was automatically generated and should not be edited.

import { AddressCountry, OrderEventsEmails, OrderEvents, FulfillmentStatus, PaymentStatusEnum, OrderStatus } from "./../../types/globalTypes";

// ====================================================
// GraphQL mutation operation: OrderLineDelete
// ====================================================

export interface OrderLineDelete_draftOrderLineDelete_errors {
  __typename: "Error";
  field: string | null;
  message: string | null;
}

export interface OrderLineDelete_draftOrderLineDelete_order_billingAddress {
  __typename: "Address";
  id: string;
  city: string;
  cityArea: string;
  companyName: string;
  country: AddressCountry;
  countryArea: string;
  firstName: string;
  lastName: string;
  phone: string | null;
  postalCode: string;
  streetAddress1: string;
  streetAddress2: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_events_user {
  __typename: "User";
  email: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_events {
  __typename: "OrderEvent";
  id: string;
  amount: number | null;
  date: any | null;
  email: string | null;
  emailType: OrderEventsEmails | null;
  message: string | null;
  quantity: number | null;
  type: OrderEvents | null;
  user: OrderLineDelete_draftOrderLineDelete_order_events_user | null;
}

export interface OrderLineDelete_draftOrderLineDelete_order_fulfillments_lines_edges_node_orderLine {
  __typename: "OrderLine";
  id: string;
  productName: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_fulfillments_lines_edges_node {
  __typename: "FulfillmentLine";
  id: string;
  orderLine: OrderLineDelete_draftOrderLineDelete_order_fulfillments_lines_edges_node_orderLine;
  quantity: number;
}

export interface OrderLineDelete_draftOrderLineDelete_order_fulfillments_lines_edges {
  __typename: "FulfillmentLineCountableEdge";
  node: OrderLineDelete_draftOrderLineDelete_order_fulfillments_lines_edges_node;
}

export interface OrderLineDelete_draftOrderLineDelete_order_fulfillments_lines {
  __typename: "FulfillmentLineCountableConnection";
  edges: OrderLineDelete_draftOrderLineDelete_order_fulfillments_lines_edges[];
}

export interface OrderLineDelete_draftOrderLineDelete_order_fulfillments {
  __typename: "Fulfillment";
  id: string;
  lines: OrderLineDelete_draftOrderLineDelete_order_fulfillments_lines | null;
  status: FulfillmentStatus;
  trackingNumber: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_lines_edges_node_unitPrice_gross {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_lines_edges_node_unitPrice_net {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_lines_edges_node_unitPrice {
  __typename: "TaxedMoney";
  gross: OrderLineDelete_draftOrderLineDelete_order_lines_edges_node_unitPrice_gross;
  net: OrderLineDelete_draftOrderLineDelete_order_lines_edges_node_unitPrice_net;
}

export interface OrderLineDelete_draftOrderLineDelete_order_lines_edges_node {
  __typename: "OrderLine";
  id: string;
  productName: string;
  productSku: string;
  quantity: number;
  quantityFulfilled: number;
  unitPrice: OrderLineDelete_draftOrderLineDelete_order_lines_edges_node_unitPrice | null;
  thumbnailUrl: string | null;
}

export interface OrderLineDelete_draftOrderLineDelete_order_lines_edges {
  __typename: "OrderLineCountableEdge";
  node: OrderLineDelete_draftOrderLineDelete_order_lines_edges_node;
}

export interface OrderLineDelete_draftOrderLineDelete_order_lines {
  __typename: "OrderLineCountableConnection";
  edges: OrderLineDelete_draftOrderLineDelete_order_lines_edges[];
}

export interface OrderLineDelete_draftOrderLineDelete_order_shippingAddress {
  __typename: "Address";
  id: string;
  city: string;
  cityArea: string;
  companyName: string;
  country: AddressCountry;
  countryArea: string;
  firstName: string;
  lastName: string;
  phone: string | null;
  postalCode: string;
  streetAddress1: string;
  streetAddress2: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_shippingMethod {
  __typename: "ShippingMethod";
  id: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_shippingPrice_gross {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_shippingPrice {
  __typename: "TaxedMoney";
  gross: OrderLineDelete_draftOrderLineDelete_order_shippingPrice_gross;
}

export interface OrderLineDelete_draftOrderLineDelete_order_subtotal_gross {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_subtotal {
  __typename: "TaxedMoney";
  gross: OrderLineDelete_draftOrderLineDelete_order_subtotal_gross;
}

export interface OrderLineDelete_draftOrderLineDelete_order_total_gross {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_total_tax {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_total {
  __typename: "TaxedMoney";
  gross: OrderLineDelete_draftOrderLineDelete_order_total_gross;
  tax: OrderLineDelete_draftOrderLineDelete_order_total_tax;
}

export interface OrderLineDelete_draftOrderLineDelete_order_totalAuthorized {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_totalCaptured {
  __typename: "Money";
  amount: number;
  currency: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_user {
  __typename: "User";
  id: string;
  email: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order_availableShippingMethods {
  __typename: "ShippingMethod";
  id: string;
  name: string;
}

export interface OrderLineDelete_draftOrderLineDelete_order {
  __typename: "Order";
  id: string;
  billingAddress: OrderLineDelete_draftOrderLineDelete_order_billingAddress | null;
  created: any;
  events: (OrderLineDelete_draftOrderLineDelete_order_events | null)[] | null;
  fulfillments: (OrderLineDelete_draftOrderLineDelete_order_fulfillments | null)[];
  lines: OrderLineDelete_draftOrderLineDelete_order_lines | null;
  number: string | null;
  paymentStatus: PaymentStatusEnum | null;
  shippingAddress: OrderLineDelete_draftOrderLineDelete_order_shippingAddress | null;
  shippingMethod: OrderLineDelete_draftOrderLineDelete_order_shippingMethod | null;
  shippingMethodName: string | null;
  shippingPrice: OrderLineDelete_draftOrderLineDelete_order_shippingPrice | null;
  status: OrderStatus;
  subtotal: OrderLineDelete_draftOrderLineDelete_order_subtotal | null;
  total: OrderLineDelete_draftOrderLineDelete_order_total | null;
  totalAuthorized: OrderLineDelete_draftOrderLineDelete_order_totalAuthorized | null;
  totalCaptured: OrderLineDelete_draftOrderLineDelete_order_totalCaptured | null;
  user: OrderLineDelete_draftOrderLineDelete_order_user | null;
  availableShippingMethods: (OrderLineDelete_draftOrderLineDelete_order_availableShippingMethods | null)[] | null;
}

export interface OrderLineDelete_draftOrderLineDelete {
  __typename: "DraftOrderLineDelete";
  errors: (OrderLineDelete_draftOrderLineDelete_errors | null)[] | null;
  order: OrderLineDelete_draftOrderLineDelete_order | null;
}

export interface OrderLineDelete {
  draftOrderLineDelete: OrderLineDelete_draftOrderLineDelete | null;
}

export interface OrderLineDeleteVariables {
  id: string;
}
