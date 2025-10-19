import logging
from threading import Event, Thread
from time import sleep

from confluent_kafka import Producer

from src.config.kafka import order_producer_config

logger = logging.getLogger(__name__)

order_producer = Producer(order_producer_config)


def producer_teardown():
    logger.info("Flushing Kafka producer...")
    order_producer.flush(5)


stop_polling_event = Event()


def polling_loop(poll_t: float = 0.1, sleep_t: float = 0.1):
    while not stop_polling_event.is_set():
        order_producer.poll(poll_t)
        sleep(sleep_t)


def polling_loop_start():
    polling_loop_thread = Thread(target=polling_loop, daemon=True)

    logger.info("Starting producer polling thread...")
    polling_loop_thread.start()


def polling_loop_stop():
    logger.info("Stoping producer polling thread...")
    stop_polling_event.set()

