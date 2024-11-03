pipeline {
    agent any

    environment {
        DATABASE_URL = "mongodb://localhost:27017/testdb"
        DOCKER_IMAGE = "your-dockerhub-repo/caribconnect_els:latest"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/devartblake/CaribConnect_ELS.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install uv'
                sh 'uv install'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Push Docker Image') {
            environment {
                DOCKER_CREDENTIALS_ID = 'docker-credentials'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    sh "echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin"
                    sh "docker push $DOCKER_IMAGE"
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                sshagent(['ssh-key-id']) {
                    sh '''
                    ssh $SERVER_USER@$SERVER_HOST << 'EOF'
                    docker pull $DOCKER_IMAGE
                    docker stop caribconnect_container || true
                    docker rm caribconnect_container || true
                    docker run -d --name caribconnect_container -p 8000:8000 $DOCKER_IMAGE
                    EOF
                    '''
                }
            }
        }
    }
}
