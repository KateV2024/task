pipeline {
  agent {
    docker {
      image 'mcr.microsoft.com/playwright/python:v1.49.0-noble'
      args '-u root:root -v /var/run/docker.sock:/var/run/docker.sock'
    }
  }

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  environment {
    ALLURE_RESULTS_DIR = 'allure-results'
    ALLURE_REPORT_DIR = 'allure-report'
    ALLURE_DOCKER_IMAGE = 'frankescobar/allure-docker-service-cli:latest'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install Dependencies') {
      steps {
        sh """
          set -e
          # Playwright browsers and Docker CLI are pre-installed in this image
          if [ -f requirements.txt ]; then
            pip install --upgrade pip
            pip install -r requirements.txt
          else
            echo "INFO: No requirements.txt found, skipping pip install."
          fi
        """
      }
    }

    stage('Run All Tests') {
      steps {
        sh """
          set -e
          rm -rf ${ALLURE_RESULTS_DIR} ${ALLURE_REPORT_DIR} junit-*.xml || true
          mkdir -p ${ALLURE_RESULTS_DIR}
          pytest tests \\
            --alluredir=${ALLURE_RESULTS_DIR} \\
            --junitxml=junit-tests.xml \\
            -v
        """
      }
    }

    stage('Generate Allure Report') {
      steps {
        script {
          def docker_available = sh(script: 'docker info > /dev/null 2>&1', returnStatus: true) == 0
          if (!docker_available) {
            error 'Docker is required for Allure report generation but is not available on this agent.'
          }

          sh """
            set -e
            rm -rf ${ALLURE_REPORT_DIR} || true
            docker run --rm \\
              -v "\$(pwd)/${ALLURE_RESULTS_DIR}:/app/allure-results" \\
              -v "\$(pwd)/${ALLURE_REPORT_DIR}:/app/allure-report" \\
              -e CHECK_RESULTS_EVERY_SECONDS=0 \\
              ${ALLURE_DOCKER_IMAGE} generate
          """
        }
      }
    }

    stage('Archive Reports') {
      steps {
        archiveArtifacts artifacts: "${ALLURE_RESULTS_DIR}/**, ${ALLURE_REPORT_DIR}/**, junit-*.xml",
                         fingerprint: true,
                         allowEmptyArchive: true
      }
    }
  }

  post {
    always {
      junit allowEmptyResults: true, testResults: 'junit-*.xml'
      echo "Allure HTML report: ${env.BUILD_URL}artifact/${ALLURE_REPORT_DIR}/index.html"
    }
    cleanup {
      cleanWs()
    }
  }
}