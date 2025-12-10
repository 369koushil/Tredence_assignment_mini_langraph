from app.engine.registry import tool_registry
import statistics


def profile_data(state: dict):
    data = state.get("data", [])
    if not data:
        state["mean"] = 0
        state["stddev"] = 0
        return {"mean": 0, "stddev": 0}

    mean = sum(data) / len(data)
    stddev = statistics.pstdev(data)

    state["mean"] = mean
    state["stddev"] = stddev

    return {
        "mean": round(mean, 3),
        "stddev": round(stddev, 3)
    }


def identify_anomalies(state: dict):
    data = state.get("data", [])
    mean = state.get("mean", 0)
    stddev = state.get("stddev", 1)

    anomalies = []
    for v in data:
        if abs(v - mean) > 2 * stddev:
            anomalies.append(v)

    state["anomalies"] = anomalies
    state["anomaly_count"] = len(anomalies)

    return {"anomaly_count": len(anomalies)}


def generate_rules(state: dict):
    mean = state.get("mean", 0)
    stddev = state.get("stddev", 0)

    lower = mean - 3 * stddev
    upper = mean + 3 * stddev

    state["lower_bound"] = lower
    state["upper_bound"] = upper

    return {
        "rule": f"keep values between {round(lower,3)} and {round(upper,3)}"
    }


def apply_rules(state: dict):
    data = state.get("data", [])
    lower = state.get("lower_bound")
    upper = state.get("upper_bound")

    cleaned = [v for v in data if lower <= v <= upper]

    state["data"] = cleaned
    state["cleaned_count"] = len(cleaned)

    return {"cleaned_count": len(cleaned)}


tool_registry.register("profile_data", profile_data)
tool_registry.register("identify_anomalies", identify_anomalies)
tool_registry.register("generate_rules", generate_rules)
tool_registry.register("apply_rules", apply_rules)
