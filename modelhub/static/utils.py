import json


def format_predictions_for_queue(predictions, aggregated_messages):
    """
    Format predictions for the queue
    """
    regression_predictions = predictions["regressor"]
    classification_predictions = predictions["classifier"]

    messages_with_predictions = []
    for i in range(len(aggregated_messages)):
        message = json.loads(aggregated_messages[i])
        messages_with_predictions.append(
            {
                "timestamp": message["timestamp"],
                "latitude": message["latitude"],
                "longitude": message["longitude"],
                "data_id": message["id"],
                "average_regressor_prediction": regression_predictions[i],
                "anomaly": bool(classification_predictions[i]),
            },
        )
    return messages_with_predictions
