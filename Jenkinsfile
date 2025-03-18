pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git credentialsId: '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', 
                    url: 'https://github.com/prathibha22bcd/todo_app.git',
                    branch: 'main'
            }
        }
        
        stage('Build & Test') {
            steps {
                sh 'pytest'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                sh 'sonar-scanner'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t -todo_app .'
            }
        }

        stage('Docker Push') {
            steps {
                sh 'docker push todo_app'
            }
        }

        stage('Deploy Container') {
            steps {
                sh 'docker run -d -p 5000:5000 todo_app'
            }
        }
    }
}
