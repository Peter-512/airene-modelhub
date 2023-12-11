class Predictor:
    """
    Predict future values, recognize anomalies, aggregate everything into a json message
    to put on a queue
    """

    def __init__(self) -> None:
        pass

    def predict_batch(self, aggregated_messages):
        """
        Predict values for a batch of messages
        """
        return aggregated_messages
