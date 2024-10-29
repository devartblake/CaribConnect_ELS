# Dockerfile for MongoDB with Authentication

FROM mongo:latest

# Set environment variables for MongoDB
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=yourpassword

# Create the data directory
RUN mkdir -p /data/db

# Expose MongoDB port
EXPOSE 27017

# Run MongoDB with authentication enabled
CMD ["mongod", "--auth"]