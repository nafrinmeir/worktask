pipeline {
    agent any

    parameters {
        string(name: 'VERSION', defaultValue: '2.0.0', description: 'Docker image and Kubernetes version')
    }

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        DOCKER_IMAGE_PREFIX = 'meirnafrin/worktask'
        DOCKER_REGISTRY = 'https://index.docker.io/v1/'
        //KUBE_CONFIG_PATH = 'C:/Users/MyPc/.kube/config'
        KUBE_CONFIG_PATH = 'C:/Users/Meir Nafrin/.kube/config'
        //KUBECONFIG='C:/Users/Meir Nafrin/.kube/config'


        
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/nafrinmeir/worktask.git'
            }
        }




        stage('Build and Run Docker Images') {
            steps {
                script {
                    bat "docker-compose down"
                    bat "docker-compose up -d --build"
                }
            }
        }
        

        stage('Push Docker Images') {
            steps {
                script {
                    withDockerRegistry([credentialsId: 'docker_hub_user', url: DOCKER_REGISTRY]) {
                        bat """
                            docker-compose config --services | for /f "delims=" %%I in ('more') do (
                                docker tag %DOCKER_IMAGE_PREFIX%-%%I %DOCKER_IMAGE_PREFIX%-%%I:%VERSION%
                                docker push %DOCKER_IMAGE_PREFIX%-%%I:%VERSION%
                            )
                        """
                    }
                }
            }
        }

        stage('Unit Test') {
            steps {
                bat """
                echo Running unit tests
                docker-compose exec api python -m unittest test_api.py
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withEnv(["KUBECONFIG=${KUBE_CONFIG_PATH}"]) {
                        bat """
                            helm install taskapp ./helmchart --set frontend.version=${params.VERSION} --set api.version=${params.VERSION} --set mongo.version=${params.VERSION}
                            ping localhost -4 -n 5
                            kubectl get all
                            ping localhost -4 -n 5
                            kubectl get pods -o wide
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
