#%%
import numpy as np


def peak_value(series):
    """Return the maximum value and the gait cycle % at which it occurs."""
    if series is None:
        return None, None
    idx = series.idxmax()
    return round(series.max(), 2), idx


def trough_value(series):
    """Return the minimum value and the gait cycle % at which it occurs."""
    if series is None:
        return None, None
    idx = series.idxmin()
    return round(series.min(), 2), idx


def range_of_motion(series):
    """Peak-to-trough range."""
    if series is None:
        return None
    return round(series.max() - series.min(), 2)


def loading_rate(series, stance_end=60):
    """
    Approximate average loading rate over the first 20% of stance.
    Meaningful for vGRF or moment data.
    """
    if series is None:
        return None
    early_stance = series.iloc[:20]
    rate = (early_stance.max() - early_stance.iloc[0]) / 20
    return round(rate, 4)


def symmetry_index(left_series, right_series):
    """
    Symmetry Index (%) between left and right limb.
    SI = 0% is perfect symmetry.
    """
    if left_series is None or right_series is None:
        return None
    left_peak = left_series.max()
    right_peak = right_series.max()
    if (left_peak + right_peak) == 0:
        return None
    si = abs(left_peak - right_peak) / ((left_peak + right_peak) / 2) * 100
    return round(si, 2)


def compute_summary(data, data_type, shoe, joint_side, axis):
    """
    Return a dict of key metrics for a given shoe/joint/axis combo.
    joint_side should be e.g. 'Left Knee'
    """
    from data_loader import get_series

    series = get_series(data, data_type, shoe, joint_side, axis)
    if series is None:
        return {}

    peak, peak_idx = peak_value(series)
    trough, trough_idx = trough_value(series)
    
    result={
        'Peak': peak,
        'Trough': trough,
        'Range': range_of_motion(series),
    }
    if data_type== 'grf':
        result['Loading Rate'] = loading_rate(series)
    return result