pipeline {
    agent any
    environment {
        DOCKERHUB_IMAGE = 'yourdockerhubuser/worktask'
    }
    stages {
        stage('Build') {
            steps {
                sh 'docker-compose build'
            }
        }
        stage('Unit Test') {
            steps {
                sh 'docker run --rm api pytest test_api.py'
            }
        }
        stage('Push Images') {
            steps {
                sh 'docker tag worktask_api $DOCKERHUB_IMAGE-api'
                sh 'docker tag worktask_frontend $DOCKERHUB_IMAGE-frontend'
                sh 'docker push $DOCKERHUB_IMAGE-api'
                sh 'docker push $DOCKERHUB_IMAGE-frontend'
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh 'helm upgrade --install worktask ./helmchart'
            }
        }
    }
}