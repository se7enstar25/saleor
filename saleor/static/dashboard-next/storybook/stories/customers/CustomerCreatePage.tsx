import { storiesOf } from "@storybook/react";
import * as React from "react";

import CustomerCreatePage, {
  CustomerCreatePageFormData,
  CustomerCreatePageProps
} from "../../../customers/components/CustomerCreatePage";
import Decorator from "../../Decorator";
import { formError } from "../../misc";

const props: CustomerCreatePageProps = {
  countries: [
    { __typename: "CountryDisplay", code: "UK", country: "United Kingdom" },
    { __typename: "CountryDisplay", code: "PL", country: "Poland" }
  ],
  disabled: false,
  errors: [],
  onBack: () => undefined,
  onSubmit: () => undefined
};

storiesOf("Views / Customers / Create customer", module)
  .addDecorator(Decorator)
  .add("default", () => <CustomerCreatePage {...props} />)
  .add("loading", () => <CustomerCreatePage {...props} disabled={true} />)
  .add("form errors", () => (
    <CustomerCreatePage
      {...props}
      errors={([
        "city",
        "cityArea",
        "companyName",
        "country",
        "countryArea",
        "email",
        "firstName",
        "lastName",
        "note",
        "phone",
        "postalCode",
        "streetAddress1",
        "streetAddress2"
      ] as Array<keyof CustomerCreatePageFormData>).map(field =>
        formError(field)
      )}
    />
  ));
