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
        bat '''
        sonar-scanner -Dsonar.projectKey=devops1 \
                      -Dsonar.host.url=http://localhost:9000 \
                      -Dsonar.token=squ_8cbb0c4e469f3f7e165b497d4a487b39eb7f8b46
        '''
    }
}


        stage('Docker Build') {
            steps {
                bat 'docker build -t prathibha22bcd36/todo_app .'
            }
        }

        stage('Docker Push') {
            steps {
                bat 'docker push prathibha22bcd36/todo_app'
            }
        }

        stage('Deploy Container') {
            steps {
                bat 'docker run -d -p 5000:5000 prathibha22bcd36/todo_app'
            }
        }
    }
}
