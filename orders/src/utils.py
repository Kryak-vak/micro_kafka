from confluent_kafka import KafkaError, KafkaException


def is_retriable_kafka_error(exception: BaseException) -> bool:
    if isinstance(exception, KafkaException):
        err: KafkaError = exception.args[0]
        return err.retriable()
    return False