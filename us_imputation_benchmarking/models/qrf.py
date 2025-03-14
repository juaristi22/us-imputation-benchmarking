from us_imputation_benchmarking.utils import qrf
import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Any, Union
from us_imputation_benchmarking.config import RANDOM_STATE


class QRF:
    """
    Quantile Random Forest model for imputation.

    This model uses a Quantile Random Forest to predict quantiles.
    The underlying QRF implementation is from utils.qrf.
    """
    def __init__(self, seed: int = RANDOM_STATE):
        """Initialize the QRF model.

        Args:
            seed: Random seed for reproducibility.
        """
        self.qrf = qrf.QRF(seed=seed)
        self.predictors: Optional[List[str]] = None
        self.imputed_variables: Optional[List[str]] = None

    def fit(
        self,
        X: pd.DataFrame,
        predictors: List[str],
        imputed_variables: List[str],
        **qrf_kwargs: Any,
    ) -> "QRF":
        """Fit the QRF model to the training data.

        Args:
            X: DataFrame containing the training data.
            predictors: List of column names to use as predictors.
            imputed_variables: List of column names to impute.
            **qrf_kwargs: Additional keyword arguments to pass to QRF.

        Returns:
            The fitted model instance.
        """
        self.predictors = predictors
        self.imputed_variables = imputed_variables

        self.qrf.fit(X[predictors], X[imputed_variables], **qrf_kwargs)
        return self

    def predict(
        self, test_X: pd.DataFrame, quantiles: List[float]
    ) -> Dict[float, np.ndarray]:
        """Predict values at specified quantiles using the QRF model.

        Args:
            test_X: DataFrame containing the test data.
            quantiles: List of quantiles to predict.

        Returns:
            Dictionary mapping quantiles to predicted values.
        """
        imputations: Dict[float, np.ndarray] = {}

        for q in quantiles:
            imputation = self.qrf.predict(
                test_X[self.predictors], mean_quantile=q
            )
            imputations[q] = imputation

        return imputations
