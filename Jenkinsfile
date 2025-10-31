pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        PATH = "${VENV_DIR}/bin:${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                python3 -m venv $VENV_DIR
                source $VENV_DIR/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Install Playwright browsers') {
            steps {
                sh '''
                source $VENV_DIR/bin/activate
                python -m playwright install chromium
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                source $VENV_DIR/bin/activate
                pytest tests/ --alluredir=reports
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                    allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'reports']]
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
            junit 'reports/**/*.xml'
        }
        failure {
            echo '❌ Tests failed!'
        }
        success {
            echo '✅ Tests passed successfully!'
        }
    }
}
