import Typography, { TypographyProps } from "@material-ui/core/Typography";
import * as React from "react";

import { LocaleConsumer } from "../Locale";

export interface MoneyProp {
  amount: number;
  currency: string;
}
interface MoneyProps {
  moneyDetalis: MoneyProp;
  typographyProps?: TypographyProps;
  inline?;
}

export const Money: React.StatelessComponent<MoneyProps> = ({
  moneyDetalis,
  typographyProps,
  inline
}) => (
  <LocaleConsumer>
    {locale => {
      const money = moneyDetalis.amount.toLocaleString(locale, {
        currency: moneyDetalis.currency,
        style: "currency"
      });
      if (typographyProps) {
        return <Typography {...typographyProps}>{money}</Typography>;
      }
      if (inline) {
        return <span>{money}</span>;
      }
      return <>{money}</>;
    }}
  </LocaleConsumer>
);

export default Money;
