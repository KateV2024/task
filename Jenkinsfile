pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "myapp"
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

        stage('Cleanup') {
            steps {
                echo '🧹 Cleaning up previous runs...'
                sh '''
                    docker-compose down -v || true
                    rm -rf ${ALLURE_RESULTS_DIR} ${ALLURE_REPORT_DIR} junit-*.xml || true
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                echo '🔨 Building Docker images...'
                sh 'docker-compose build'
            }
        }

        stage('Start Services') {
            steps {
                echo '🚀 Starting MongoDB and Backend...'
                sh '''
                    docker-compose up -d mongo backend
                    echo "Waiting for services to be ready..."
                    sleep 15
                '''
            }
        }

        stage('Run Python Tests') {
            steps {
                echo '🧪 Running Playwright + Pytest tests...'
                sh '''
                    set -e

                    # Create allure results directory
                    mkdir -p ${ALLURE_RESULTS_DIR}

                    # Run pytest with allure reporting
                    docker-compose exec -T backend \
                        pytest tests \
                            --alluredir=${ALLURE_RESULTS_DIR} \
                            --junitxml=junit-tests.xml \
                            -v \
                            --tb=short \
                            || EXIT_CODE=$?

                    # Copy reports from container to host
                    docker-compose cp backend:/app/${ALLURE_RESULTS_DIR} . || true
                    docker-compose cp backend:/app/junit-tests.xml . || true

                    if [ ! -z "$EXIT_CODE" ]; then
                        exit $EXIT_CODE
                    fi
                '''
            }
            post {
                always {
                    echo '🧾 Collecting logs...'
                    sh '''
                        docker-compose logs backend > backend-test.log || true
                        docker-compose logs mongo > mongo-test.log || true
                    '''
                    archiveArtifacts artifacts: '*-test.log', followSymlinks: false, allowEmptyArchive: true
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
        always {
            echo '🧹 Cleaning up containers...'
            sh '''
                docker-compose down -v || true
            '''
        }
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