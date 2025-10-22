
pipeline {
    agent any

    environment {
        ALLURE_RESULTS_DIR = 'allure-results'
        ALLURE_REPORT_DIR = 'allure-report'
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📦 Cloning repository...'
                checkout scm
            }
        }

        stage('Install Python') {
            steps {
                echo '🐍 Installing Python...'
                sh '''
                    # For Ubuntu/Debian
                    if command -v apt-get &> /dev/null; then
                        apt-get update
                        apt-get install -y python3 python3-pip python3-venv
                    # For CentOS/RHEL
                    elif command -v yum &> /dev/null; then
                        yum install -y python3 python3-pip
                    # For Alpine
                    elif command -v apk &> /dev/null; then
                        apk add python3 py3-pip
                    else
                        echo "Unsupported OS"
                        exit 1
                    fi

                    python3 --version
                    pip3 --version
                '''
            }
        }

        stage('Cleanup') {
            steps {
                echo '🧹 Cleaning up previous runs...'
                sh '''
                    rm -rf ${ALLURE_RESULTS_DIR} ${ALLURE_REPORT_DIR} junit-*.xml venv || true
                '''
            }
        }

        stage('Setup Environment') {
            steps {
                echo '⚙️ Setting up Python environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    playwright install
                '''
            }
        }

        stage('Run Python Tests') {
            steps {
                echo '🧪 Running Playwright + Pytest tests...'
                sh '''
                    set -e
                    . venv/bin/activate

                    mkdir -p ${ALLURE_RESULTS_DIR}
                    export PYTHONPATH=${WORKSPACE}

                    pytest tests \
                        --alluredir=${ALLURE_RESULTS_DIR} \
                        --junitxml=junit-tests.xml \
                        -v \
                        --tb=short
                '''
            }
            post {
                always {
                    echo '🧾 Test execution completed'
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo '📊 Generating Allure report...'
                sh '''
                    if [ -d "${ALLURE_RESULTS_DIR}" ] && [ "$(ls -A ${ALLURE_RESULTS_DIR})" ]; then
                        docker run --rm \
                            -v "${WORKSPACE}/${ALLURE_RESULTS_DIR}:/app/allure-results" \
                            -v "${WORKSPACE}/${ALLURE_REPORT_DIR}:/app/allure-report" \
                            frankescobar/allure-docker-service:2.29.0 \
                            allure generate /app/allure-results -o /app/allure-report --clean || true
                    else
                        echo "No allure results found, skipping report generation"
                    fi
                '''
            }
        }

        stage('Publish Results') {
            steps {
                echo '📋 Publishing test results...'
                junit allowEmptyResults: true, testResults: 'junit-*.xml'

                script {
                    if (fileExists("${ALLURE_REPORT_DIR}/index.html")) {
                        echo "✅ Allure HTML report: ${env.BUILD_URL}artifact/${ALLURE_REPORT_DIR}/index.html"
                    }
                }

                archiveArtifacts artifacts: "${ALLURE_RESULTS_DIR}/**, ${ALLURE_REPORT_DIR}/**, junit-*.xml",
                                 fingerprint: true,
                                 allowEmptyArchive: true
            }
        }

    }

    post {
        success {
            echo '✅ Tests passed successfully!'
        }
        failure {
            echo '❌ Tests failed! Check logs above for details.'
        }
        cleanup {
            cleanWs()
        }
    }
}