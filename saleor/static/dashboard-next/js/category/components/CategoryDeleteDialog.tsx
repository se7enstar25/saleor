import Button from "material-ui/Button";
import Dialog, {
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle
} from "material-ui/Dialog";
import { withStyles } from "material-ui/styles";
import Typography from "material-ui/Typography";
import * as React from "react";

import i18n from "../../i18n";

const decorate = withStyles(theme => ({
  deleteButton: {
    "&:hover": {
      backgroundColor: theme.palette.error.main
    },
    backgroundColor: theme.palette.error.main,
    color: theme.palette.error.contrastText
  }
}));

interface CategoryDeleteDialogProps {
  name: string;
  opened?: boolean;
  productCount?: number;
  onClose?();
  onConfirm?();
}

const CategoryDeleteDialog = decorate<CategoryDeleteDialogProps>(props => {
  const {
    children,
    classes,
    name,
    opened,
    onConfirm,
    onClose,
    productCount,
    ...dialogProps
  } = props;
  return (
    <Dialog open={opened} {...dialogProps}>
      <DialogTitle>
        {i18n.t("Delete category", { context: "title" })}
      </DialogTitle>
      <DialogContent>
        <DialogContentText
          dangerouslySetInnerHTML={{
            __html: i18n.t(
              "Are you sure you want to remove <strong>{{name}}</strong>?",
              { name }
            )
          }}
        />
        {productCount &&
          productCount > 0 && (
            <DialogContentText>
              {i18n.t(
                "There are {{count}} product(s) in this category that will also be removed.",
                {
                  count: productCount
                }
              )}
            </DialogContentText>
          )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>
          {i18n.t("Cancel", { context: "button" })}
        </Button>
        <Button
          className={classes.deleteButton}
          variant="raised"
          onClick={onConfirm}
        >
          {i18n.t("Delete category", { context: "button" })}
        </Button>
      </DialogActions>
    </Dialog>
  );
});

export default CategoryDeleteDialog;
