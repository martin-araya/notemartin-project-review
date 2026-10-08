from __future__ import annotations

import pandas as pd
from sklearn.tree import DecisionTreeClassifier


def legacy_train(X: pd.DataFrame, y: pd.Series):
    """S1 dead legacy_train.

    No acepta seed; produce modelos no reproducibles.
    Declarado pero nunca invocado por el pipeline actual.
    """
    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model