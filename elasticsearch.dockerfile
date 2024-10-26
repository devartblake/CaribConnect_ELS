# ElasticSearch Dockerfile (elasticsearch.dockerfile)

# ElasticSearch Dockerfile (elasticsearch.dockerfile)
FROM docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}

# Environment setup
ENV ELASTIC_PASSWORD=${ELASTICSEARCH_PASSWORD}
ENV NODE_NAME=node01
ENV CERTS_DIR=/usr/share/elasticsearch/config/certs
ENV CONFIG_DIR=/usr/share/elasticsearch/config

# Copy the entrypoint script
COPY ./elasticsearch/config/docker-entrypoint.sh /usr/share/elasticsearch/docker-entrypoint.sh
RUN chmod +x /usr/share/elasticsearch/docker-entrypoint.sh

# Set up certs directory with permissions
RUN mkdir -p ${CERTS_DIR} && \
    chown -R elasticsearch:elasticsearch ${CONFIG_DIR}

# Use default entrypoint
USER elasticsearch
ENTRYPOINT ["/usr/share/elasticsearch/docker-entrypoint.sh"]