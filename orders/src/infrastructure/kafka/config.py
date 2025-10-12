from src.config.kafka import kafka_config

config = {
    'bootstrap.servers': kafka_config.bootstrap_server,

    'auto.offset.reset': 'earliest'
}
