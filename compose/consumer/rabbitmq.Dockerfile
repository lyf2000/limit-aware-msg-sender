FROM rabbitmq:3.12.7-management

RUN rabbitmq-plugins enable rabbitmq_consistent_hash_exchange