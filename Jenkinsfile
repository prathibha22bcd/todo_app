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
                bat 'C:\\Users\\LENOVO\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\pytest.exe'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                bbat 'sonar-scanner -Dsonar.login=squ_8cbb0c4e469f3f7e165b497d4a487b39eb7f8b46'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t -todo_app .'
            }
        }

        stage('Docker Push') {
            steps {
                bat 'docker push todo_app'
            }
        }

        stage('Deploy Container') {
            steps {
                bat 'docker run -d -p 5000:5000 todo_app'
            }
        }
    }
}
