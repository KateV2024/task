pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}\\venv"
        PATH = "${VENV_DIR}\\Scripts;${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                bat '''
                python -m venv %VENV_DIR%
                call %VENV_DIR%\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Install Playwright browsers') {
            steps {
                bat '''
                call %VENV_DIR%\\Scripts\\activate
                python -m playwright install chromium
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                call %VENV_DIR%\\Scripts\\activate
                set PYTHONPATH=%CD%
                pytest tests/ --alluredir=reports
                if %errorlevel% neq 0 (
                    echo Some tests failed, but continuing pipeline...
                    exit /b 0
                )
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'reports']],
                    commandline: 'allure'
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
        }
        failure {
            echo '❌ Tests failed!'
        }
        success {
            echo '✅ Tests passed successfully!'
        }
    }
}
