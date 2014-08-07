from scrapy.utils.serialize import ScrapyJSONEncoder

from kafka.client import KafkaClient
from kafka.producer import SimpleProducer


class KafkaPipeline(object):
    """Publishes a serialized item into a Kafka topic"""
    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic

        self.encoder = ScrapyJSONEncoder()

    def process_item(self, item, spider):
        # put spider name in item
        item = dict(item)
        item['spider'] = spider.name
        msg = self.encoder.encode(item)
        self.producer.send_messages(self.topic, msg)

    @classmethod
    def from_settings(cls, settings):
        k_hosts = settings.get('SCRAPY_KAFKA_HOSTS', ['localhost:9092'])
        topic = settings.get('KAFKA_ITEM_PIPELINE_TOPIC', 'scrapy_kafka_item')
        kafka = KafkaClient(k_hosts)
        conn = SimpleProducer(kafka)
        return cls(conn, topic)
