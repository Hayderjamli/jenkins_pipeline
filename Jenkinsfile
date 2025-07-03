pipeline {
    agent any

    environment {
        IMAGE_NAME = "app-1"
        IMAGE_TAG = "latest"
        REGISTRY = "localhost:8082"     // 🔁 Change to your Nexus Docker Registry
        DOCKER_CREDENTIALS_ID = "nexus-credentials"  // 👈 Matches the ID you created
        NEXUS_IP = '172.24.0.4'
    }

    

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Hayderjamli/jenkins_pipeline.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('Code Quality - SonarQube') {
            steps {
              withSonarQubeEnv('MySonarQubeServer') {
                     script {
                         def scannerHome = tool 'SonarQubeScanner' // Must match tool name
                         sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=fastapi-boilerplate -Dsonar.sources=. -Dsonar.host.url=http://sonarqube-1:9000 -Dsonar.login=sqp_24cb790c9c27246055f9d533a7d6f1b12729d8b2"
                     }
              }
            }
        }

        stage('Push to Nexus') {
            steps {
              withCredentials([usernamePassword(credentialsId: 'nexus-credentials', usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
                sh """
                  echo "$NEXUS_PASS" | docker login -u "$NEXUS_USER" --password-stdin localhost:5000
                  docker tag app-1:latest localhost:5000/app-1:latest
                  docker push localhost:5000/app-1:latest
                """
              }
            }
        }


        stage('Deploy with Docker Compose') {
            steps {
                sh 'docker-compose down && docker-compose up -d --build'
            }
        }
    }
}