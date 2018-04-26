import Card from "material-ui/Card";
import blue from "material-ui/colors/blue";
import { withStyles } from "material-ui/styles";
import Table, { TableBody, TableCell, TableRow } from "material-ui/Table";
import * as React from "react";

import PageHeader from "../../../components/PageHeader";
import Skeleton from "../../../components/Skeleton";
import i18n from "../../../i18n";

interface ProductVariantNavigationProps {
  variants?: Array<{
    id: string;
    name: string;
  }>;
  current?: string;
  loading?: boolean;
  onRowClick?(id: string);
}

const decorate = withStyles(theme => ({
  card: {
    marginTop: theme.spacing.unit * 2,
    [theme.breakpoints.down("sm")]: {
      marginTop: theme.spacing.unit
    }
  },
  link: {
    color: blue[500],
    cursor: "pointer"
  }
}));
const ProductVariantNavigation = decorate<ProductVariantNavigationProps>(
  ({ classes, variants, current, loading, onRowClick }) => (
    <Card className={classes.card}>
      <PageHeader title={i18n.t("Variants")} />
      <Table>
        <TableBody>
          {loading ? (
            <TableRow>
              <TableCell>
                <Skeleton />
              </TableCell>
            </TableRow>
          ) : variants.length > 0 ? (
            variants.map(variant => (
              <TableRow key={variant.id}>
                <TableCell
                  className={onRowClick ? classes.link : ""}
                  onClick={onRowClick ? onRowClick(variant.id) : () => {}}
                >
                  {variant.name}
                </TableCell>
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell>{i18n.t("This product has no variants")}</TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </Card>
  )
);
export default ProductVariantNavigation;
