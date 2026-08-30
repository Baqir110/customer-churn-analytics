import pandas as pd


def get_feature_explanations(model, input_df: pd.DataFrame) -> dict:
    scaler = model.named_steps["scaler"]
    classifier = model.named_steps["classifier"]

    scaled_values = scaler.transform(input_df)[0]
    importances = classifier.feature_importances_
    feature_names = input_df.columns.tolist()

    contributions = {}
    for name, val, imp in zip(feature_names, scaled_values, importances):
        contributions[name] = round(float(val * imp), 4)

    return contributions
