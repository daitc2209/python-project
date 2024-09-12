pipeline {
    agent any

    environment {
        dockerImageName1 = 'daitc2209/test-jenkins'
        dockerImageName1Version = 'python-project-frontend-v1.1' // Change this manually for service1
        dockerImageName2 = 'daitc2209/test-jenkins'
        dockerImageName2Version = 'python-project-backend-v1.1' // Change this manually for service2
        dockerHubCredentialsId = 'daitc2209' // Define your Docker Hub credentials ID
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    bat 'git clone https://github.com/daitc2209/python-project.git'
                }
            }
        }

        stage('Build Docker Images with Docker Compose') {
            steps {
                echo 'Building Docker images with docker-compose...'
                dir('python-project') {
                    bat 'docker-compose build'
                }
            }
        }

        stage('Tag Docker Images') {
            steps {
                echo 'Tagging Docker images...'
                script {
                    bat "docker tag python-project-frontend:latest ${dockerImageName1}:${dockerImageName1Version}"
                    bat "docker tag python-project-backend:latest ${dockerImageName2}:${dockerImageName2Version}"
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                echo 'Pushing Docker images...'
                script {
                    withCredentials([usernamePassword(credentialsId: dockerHubCredentialsId, usernameVariable: 'daitc@mksmart.com.vn', passwordVariable: '0906088493')]) {
                        bat "docker login -u ${env.DOCKER_USERNAME} -p ${env.DOCKER_PASSWORD}"
                        bat "docker push ${dockerImageName1}:${dockerImageName1Version}"
                        bat "docker push ${dockerImageName2}:${dockerImageName2Version}"
                    }
                }
            }
        }
    }
}
