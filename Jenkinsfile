pipeline {
    agent {
        docker {
            image 'docker/compose:1.29.2'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        ALLURE_RESULTS_DIR = 'allure-results'
        ALLURE_REPORT_DIR = 'allure-report'
        FRONTEND_URL = 'http://host.docker.internal:3000'
        API_BASE_URL = 'http://host.docker.internal:5000'
        MONGO_URL = 'mongodb://host.docker.internal:27017'
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

        stage('Cleanup') {
            steps {
                echo '🧹 Cleaning previous results...'
                sh '''
                    docker-compose down || true
                    rm -rf ${ALLURE_RESULTS_DIR} ${ALLURE_REPORT_DIR} junit-*.xml || true
                '''
            }
        }

        stage('Start Services') {
            steps {
                echo '🚀 Starting application services...'
                sh '''
                    docker-compose up -d

                    echo "⏳ Waiting for services to start..."
                    sleep 20

                    docker-compose ps

                    # Test connectivity
                    timeout 60 bash -c 'until curl -f http://localhost:3000 > /dev/null 2>&1; do sleep 2; done' || echo "Frontend not ready"
                    timeout 60 bash -c 'until curl -f http://localhost:5000 > /dev/null 2>&1; do sleep 2; done' || echo "Backend not ready"
                '''
            }
        }

        stage('Run Tests') {
            agent {
                docker {
                    image 'mcr.microsoft.com/playwright/python:v1.47.0-jammy'
                    args '-u root:root --add-host=host.docker.internal:host-gateway'
                    reuseNode true
                }
            }
            steps {
                echo '🧪 Running Playwright + Pytest tests...'
                sh '''
                    set -e

                    echo "📥 Installing Python dependencies..."
                    pip install --upgrade pip
                    pip install -r requirements.txt

                    echo "🎭 Installing Playwright browsers..."
                    playwright install

                    mkdir -p ${ALLURE_RESULTS_DIR}
                    export PYTHONPATH=${WORKSPACE}

                    # Set environment variables for tests
                    export BASE_URL=${FRONTEND_URL}
                    export BACKEND_URL=${API_BASE_URL}/api/records
                    export MONGO_HOST=host.docker.internal

                    echo "🧪 Running tests..."
                    echo "Frontend URL: ${BASE_URL}"
                    echo "Backend URL: ${BACKEND_URL}"
                    echo "MongoDB Host: ${MONGO_HOST}"

                    pytest tests \
                        --alluredir=${ALLURE_RESULTS_DIR} \
                        --junitxml=junit-tests.xml \
                        -v \
                        --tb=short
                '''
            }
            post {
                always {
                    echo '✅ Test execution completed.'
                }
                failure {
                    sh '''
                        echo "📋 Service logs on failure:"
                        docker-compose logs --tail=50 || true
                    '''
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
                        echo "⚠️ No allure results found, skipping report generation."
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
        always {
            echo '🧹 Stopping services...'
            sh 'docker-compose down || true'
        }
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed! Check logs above for details.'
        }
        cleanup {
            cleanWs()
        }
    }
}
