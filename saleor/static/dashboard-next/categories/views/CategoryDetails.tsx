import DialogContentText from "@material-ui/core/DialogContentText";
import * as React from "react";

import ActionDialog from "../../components/ActionDialog";
import { createPaginationState } from "../../components/Paginator";
import { WindowTitle } from "../../components/WindowTitle";
import useNavigator from "../../hooks/useNavigator";
import useNotifier from "../../hooks/useNotifier";
import usePaginator from "../../hooks/usePaginator";
import i18n from "../../i18n";
import { getMutationState, maybe } from "../../misc";
import { TypedProductBulkDeleteMutation } from "../../products/mutations";
import { productBulkDelete } from "../../products/types/productBulkDelete";
import { productAddUrl, productUrl } from "../../products/urls";
import { CategoryInput } from "../../types/globalTypes";
import {
  CategoryPageTab,
  CategoryUpdatePage
} from "../components/CategoryUpdatePage/CategoryUpdatePage";
import {
  TypedCategoryDeleteMutation,
  TypedCategoryUpdateMutation
} from "../mutations";
import { TypedCategoryDetailsQuery } from "../queries";
import { CategoryDelete } from "../types/CategoryDelete";
import { CategoryUpdate } from "../types/CategoryUpdate";
import {
  categoryAddUrl,
  categoryListUrl,
  categoryUrl,
  CategoryUrlDialog,
  CategoryUrlQueryParams
} from "../urls";

export interface CategoryDetailsProps {
  params: CategoryUrlQueryParams;
  id: string;
}

export function getActiveTab(tabName: string): CategoryPageTab {
  return tabName === CategoryPageTab.products
    ? CategoryPageTab.products
    : CategoryPageTab.categories;
}

const PAGINATE_BY = 20;

export const CategoryDetails: React.StatelessComponent<
  CategoryDetailsProps
> = ({ id, params }) => {
  const navigate = useNavigator();
  const notify = useNotifier();
  const paginate = usePaginator();

  const handleCategoryDelete = (data: CategoryDelete) => {
    if (data.categoryDelete.errors.length === 0) {
      notify({
        text: i18n.t("Category deleted", {
          context: "notification"
        })
      });
      navigate(categoryListUrl);
    }
  };
  const handleCategoryUpdate = (data: CategoryUpdate) => {
    if (data.categoryUpdate.errors.length > 0) {
      const backgroundImageError = data.categoryUpdate.errors.find(
        error => error.field === ("backgroundImage" as keyof CategoryInput)
      );
      if (backgroundImageError) {
        notify({
          text: backgroundImageError.message
        });
      }
    }
  };

  const changeTab = (tabName: CategoryPageTab) =>
    navigate(
      categoryUrl(id, {
        activeTab: tabName
      })
    );

  const closeModal = () =>
    navigate(
      categoryUrl(id, {
        ...params,
        action: undefined,
        ids: undefined
      }),
      true
    );

  const openModal = (action: CategoryUrlDialog, ids?: string[]) =>
    navigate(
      categoryUrl(id, {
        ...params,
        action,
        ids
      })
    );

  return (
    <TypedCategoryDeleteMutation onCompleted={handleCategoryDelete}>
      {(deleteCategory, deleteResult) => (
        <TypedCategoryUpdateMutation onCompleted={handleCategoryUpdate}>
          {(updateCategory, updateResult) => {
            const paginationState = createPaginationState(PAGINATE_BY, params);
            const formTransitionState = getMutationState(
              updateResult.called,
              updateResult.loading,
              maybe(() => updateResult.data.categoryUpdate.errors)
            );
            const removeDialogTransitionState = getMutationState(
              deleteResult.called,
              deleteResult.loading,
              maybe(() => deleteResult.data.categoryDelete.errors)
            );
            return (
              <TypedCategoryDetailsQuery
                displayLoader
                variables={{ ...paginationState, id }}
                require={["category"]}
              >
                {({ data, loading, refetch }) => {
                  const handleBulkProductDelete = (data: productBulkDelete) => {
                    if (data.productBulkDelete.errors.length === 0) {
                      closeModal();
                      notify({
                        text: i18n.t("Products removed")
                      });
                      refetch();
                    }
                  };

                  const { loadNextPage, loadPreviousPage, pageInfo } = paginate(
                    maybe(() => data.category.products.pageInfo),
                    paginationState,
                    params
                  );

                  return (
                    <>
                      <WindowTitle title={maybe(() => data.category.name)} />
                      <TypedProductBulkDeleteMutation
                        onCompleted={handleBulkProductDelete}
                      >
                        {(productBulkDelete, productBulkDeleteOpts) => {
                          const bulkDeleteMutationState = getMutationState(
                            productBulkDeleteOpts.called,
                            productBulkDeleteOpts.loading,
                            maybe(
                              () =>
                                productBulkDeleteOpts.data.productBulkDelete
                                  .errors
                            )
                          );

                          return (
                            <>
                              <CategoryUpdatePage
                                changeTab={changeTab}
                                currentTab={params.activeTab}
                                category={maybe(() => data.category)}
                                disabled={loading}
                                errors={maybe(
                                  () => updateResult.data.categoryUpdate.errors
                                )}
                                onAddCategory={() =>
                                  navigate(categoryAddUrl(id))
                                }
                                onAddProduct={() => navigate(productAddUrl)}
                                onBack={() =>
                                  navigate(
                                    maybe(
                                      () =>
                                        categoryUrl(data.category.parent.id),
                                      categoryListUrl
                                    )
                                  )
                                }
                                onBulkProductDelete={ids =>
                                  openModal("delete-products", ids)
                                }
                                onCategoryClick={id => () =>
                                  navigate(categoryUrl(id))}
                                onDelete={() => openModal("delete")}
                                onImageDelete={() =>
                                  updateCategory({
                                    variables: {
                                      id,
                                      input: {
                                        backgroundImage: null
                                      }
                                    }
                                  })
                                }
                                onImageUpload={file =>
                                  updateCategory({
                                    variables: {
                                      id,
                                      input: {
                                        backgroundImage: file
                                      }
                                    }
                                  })
                                }
                                onNextPage={loadNextPage}
                                onPreviousPage={loadPreviousPage}
                                pageInfo={pageInfo}
                                onProductClick={id => () =>
                                  navigate(productUrl(id))}
                                onSubmit={formData =>
                                  updateCategory({
                                    variables: {
                                      id,
                                      input: {
                                        backgroundImageAlt:
                                          formData.backgroundImageAlt,
                                        descriptionJson: JSON.stringify(
                                          formData.description
                                        ),
                                        name: formData.name,
                                        seo: {
                                          description: formData.seoDescription,
                                          title: formData.seoTitle
                                        }
                                      }
                                    }
                                  })
                                }
                                products={maybe(() =>
                                  data.category.products.edges.map(
                                    edge => edge.node
                                  )
                                )}
                                saveButtonBarState={formTransitionState}
                                subcategories={maybe(() =>
                                  data.category.children.edges.map(
                                    edge => edge.node
                                  )
                                )}
                              />
                              <ActionDialog
                                confirmButtonState={removeDialogTransitionState}
                                onClose={() => closeModal}
                                onConfirm={() =>
                                  deleteCategory({ variables: { id } })
                                }
                                open={params.action === "delete"}
                                title={i18n.t("Delete category", {
                                  context: "modal title"
                                })}
                                variant="delete"
                              >
                                <DialogContentText
                                  dangerouslySetInnerHTML={{
                                    __html: i18n.t(
                                      "Are you sure you want to remove <strong>{{ categoryName }}</strong>?",
                                      {
                                        categoryName: maybe(
                                          () => data.category.name
                                        ),
                                        context: "modal message"
                                      }
                                    )
                                  }}
                                />
                              </ActionDialog>
                              <ActionDialog
                                open={params.action === "delete-products"}
                                confirmButtonState={bulkDeleteMutationState}
                                onClose={closeModal}
                                onConfirm={() =>
                                  productBulkDelete({
                                    variables: { ids: params.ids }
                                  })
                                }
                                title={i18n.t("Remove products")}
                                variant="delete"
                              >
                                <DialogContentText
                                  dangerouslySetInnerHTML={{
                                    __html: i18n.t(
                                      "Are you sure you want to remove <strong>{{ number }}</strong> products?",
                                      {
                                        number: maybe(
                                          () => params.ids.length.toString(),
                                          "..."
                                        )
                                      }
                                    )
                                  }}
                                />
                              </ActionDialog>
                            </>
                          );
                        }}
                      </TypedProductBulkDeleteMutation>
                    </>
                  );
                }}
              </TypedCategoryDetailsQuery>
            );
          }}
        </TypedCategoryUpdateMutation>
      )}
    </TypedCategoryDeleteMutation>
  );
};
export default CategoryDetails;
