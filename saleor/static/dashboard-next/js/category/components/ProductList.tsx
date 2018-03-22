import Cached from "material-ui-icons/Cached";
import MoreVert from "material-ui-icons/MoreVert";
import Avatar from "material-ui/Avatar";
import Button from "material-ui/Button";
import List, {
  ListItem,
  ListItemAvatar,
  ListItemText,
  ListSubheader
} from "material-ui/List";
import { withStyles } from "material-ui/styles";
import Table, {
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableRow
} from "material-ui/Table";
import Typography from "material-ui/Typography";
import * as React from "react";
import { Link } from "react-router-dom";

import { categoryAddUrl } from "../";
import Skeleton from "../../components/Skeleton";
import TablePagination from "../../components/TablePagination";
import i18n from "../../i18n";
import { CategoryPropertiesQuery } from "../gql-types";

const decorate = withStyles(theme => ({
  avatarCell: {
    paddingLeft: theme.spacing.unit * 2,
    paddingRight: 0,
    width: theme.spacing.unit * 5
  }
}));

interface ProductListProps {
  hasNextPage?: boolean;
  hasPreviousPage?: boolean;
  products?: CategoryPropertiesQuery["category"]["products"]["edges"];
  onNextPage();
  onPreviousPage();
}

export const ProductList = decorate<ProductListProps>(
  ({
    classes,
    hasNextPage,
    hasPreviousPage,
    onNextPage,
    onPreviousPage,
    products
  }) => (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell className={classes.avatarCell} />
          <TableCell>{i18n.t("Name", { context: "object" })}</TableCell>
          <TableCell>{i18n.t("Type", { context: "object" })}</TableCell>
        </TableRow>
      </TableHead>
      <TableFooter>
        <TableRow>
          <TablePagination
            colSpan={3}
            hasNextPage={hasNextPage}
            onNextPage={onNextPage}
            hasPreviousPage={hasPreviousPage}
            onPreviousPage={onPreviousPage}
          />
        </TableRow>
      </TableFooter>
      <TableBody>
        {products === undefined ? (
          <TableRow>
            <TableCell className={classes.avatarCell}>
              <Avatar>
                <Cached />
              </Avatar>
            </TableCell>
            <TableCell>
              <Skeleton />
            </TableCell>
            <TableCell>
              <Skeleton />
            </TableCell>
          </TableRow>
        ) : products.length > 0 ? (
          products.map(edge => (
            <TableRow key={edge.node.id}>
              <TableCell className={classes.avatarCell}>
                <Avatar src={edge.node.thumbnailUrl} />
              </TableCell>
              <TableCell>{edge.node.name}</TableCell>
              <TableCell>{edge.node.productType.name}</TableCell>
            </TableRow>
          ))
        ) : (
          <TableRow>
            <TableCell className={classes.avatarCell} />
            <TableCell colSpan={2}>{i18n.t("No products found")}</TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
);

export default ProductList;
