import { parse as parseQs } from "qs";
import * as React from "react";
import { Route, RouteComponentProps, Switch } from "react-router-dom";

import { WindowTitle } from "../components/WindowTitle";
import i18n from "../i18n";
import { shippingZonesListPath } from "./urls";
import ShippingZonesListComponent, {
  ShippingZonesListQueryParams
} from "./views/ShippingZonesList";

const ShippingZonesList: React.StatelessComponent<RouteComponentProps<{}>> = ({
  location
}) => {
  const qs = parseQs(location.search.substr(1));
  const params: ShippingZonesListQueryParams = {
    after: qs.after,
    before: qs.before
  };
  return <ShippingZonesListComponent params={params} />;
};

export const ShippingRouter: React.StatelessComponent = () => (
  <>
    <WindowTitle title={i18n.t("Shipping")} />
    <Switch>
      <Route exact path={shippingZonesListPath} component={ShippingZonesList} />
    </Switch>
  </>
);
export default ShippingRouter;
