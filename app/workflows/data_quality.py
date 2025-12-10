def get_data_quality_workflow():
    """
    Implements the Data Quality Pipeline:

    1. Profile data
    2. Identify anomalies
    3. Generate rules
    4. Apply rules
    5. Loop until anomaly_count <= threshold
    """

    nodes = [
        {"name": "profile", "fn": "profile_data"},
        {"name": "identify", "fn": "identify_anomalies"},
        {"name": "generate_rules", "fn": "generate_rules"},
        {"name": "apply", "fn": "apply_rules"}
    ]

    edges = [
        {"from_node": "profile", "to_node": "identify"},
        {"from_node": "identify", "to_node": "generate_rules"},
        {"from_node": "generate_rules", "to_node": "apply"},

        # Loop until anomalies are small
        {
            "from_node": "apply",
            "to_node": "profile",
            "condition": "state.get('anomaly_count', 999) > state.get('threshold', 1)"
        }
    ]

    return {
        "name": "data_quality_pipeline",
        "nodes": nodes,
        "edges": edges,
        "start_node": "profile"
    }
