import os
import tempfile
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=RuntimeWarning)

from evidently import Report
from evidently.presets import DataDriftPreset

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_target_path() -> Path:
    """Returns /tmp path on Render/Linux, or local data/ directory on Windows."""
    if os.name == "nt":
        target_dir = BASE_DIR / "data"
    else:
        target_dir = Path(tempfile.gettempdir()) / "customer_churn_analytics"

    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / "drift_report.html"


def get_mock_baseline_data(n_samples: int = 1000) -> pd.DataFrame:
    """Generates synthetic baseline data matching the model training distribution."""
    np.random.seed(42)
    tenure_months = np.random.randint(1, 72, size=n_samples)
    monthly_charges = np.random.uniform(20.0, 120.0, size=n_samples)
    total_charges = tenure_months * monthly_charges + np.random.normal(
        0, 50, size=n_samples
    )
    total_charges = np.maximum(total_charges, monthly_charges)
    support_tickets = np.random.poisson(lam=1.5, size=n_samples)

    return pd.DataFrame(
        {
            "tenure_months": tenure_months,
            "monthly_charges": monthly_charges,
            "total_charges": total_charges,
            "support_tickets": support_tickets,
        }
    )


def generate_drift_report(current_data: pd.DataFrame = None) -> Path:
    """Generates an HTML report checking for data drift between baseline and production data."""
    features = [
        "tenure_months",
        "monthly_charges",
        "total_charges",
        "support_tickets",
    ]

    reference_df = get_mock_baseline_data()[features]

    if current_data is None:
        current_data = reference_df.copy()
        current_data["support_tickets"] = current_data["support_tickets"] + 1
        current_data["monthly_charges"] = current_data["monthly_charges"] * 1.05

    current_df = current_data[features]

    report = Report(metrics=[DataDriftPreset()])
    snapshot = report.run(current_data=current_df, reference_data=reference_df)

    target_file = get_target_path()
    snapshot.save_html(str(target_file))

    if target_file.exists() and target_file.stat().st_size > 0:
        print(f"SUCCESS: Drift report saved to {target_file}")
        return target_file
    else:
        raise RuntimeError("save_html ran but output file is missing or empty.")


if __name__ == "__main__":
    generate_drift_report()
