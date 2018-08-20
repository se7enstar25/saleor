import * as React from "react";

import {
  PartialMutationProviderProps,
  PartialMutationProviderRenderProps
} from "../..";
import {
  VariantImageUnassignMutation,
  VariantImageUnassignMutationVariables
} from "../../gql-types";
import { TypedVariantImageUnassignMutation } from "../mutations";

interface VariantImageUnassignProviderProps
  extends PartialMutationProviderProps {
  id: string;
  children: PartialMutationProviderRenderProps<
    VariantImageUnassignMutation,
    VariantImageUnassignMutationVariables
  >;
}

const VariantImageUnassignProvider: React.StatelessComponent<
  VariantImageUnassignProviderProps
> = ({ id, children, onError, onSuccess }) => (
  <TypedVariantImageUnassignMutation onCompleted={onSuccess} onError={onError}>
    {(mutate, { data, loading, error }) => {
      return children({
        data,
        error,
        loading,
        mutate
      });
    }}
  </TypedVariantImageUnassignMutation>
);

export default VariantImageUnassignProvider;
