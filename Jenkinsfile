pipeline {
  agent none

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  environment {
    ALLURE_RESULTS_DIR = 'allure-results'
    ALLURE_REPORT_DIR = 'allure-report'
    ALLURE_DOCKER_IMAGE = 'frankescobar/allure-docker-service-cli:latest'
    HEADLESS = 'true'
  }

  stages {
    stage('Checkout') {
      agent any
      steps {
        checkout scm
      }
    }

    stage('Install Dependencies and Run Tests') {
      agent {
        docker {
          image 'mcr.microsoft.com/playwright/python:v1.49.0-noble'
          args '-u root:root'
          reuseNode true
        }
      }
      stages {
        stage('Install Dependencies') {
          steps {
            sh """
              set -e
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
              export PYTHONPATH=\${PYTHONPATH}:\$(pwd)
              pytest tests \\
                --alluredir=${ALLURE_RESULTS_DIR} \\
                --junitxml=junit-tests.xml \\
                -v
            """
          }
        }
      }
    }

    stage('Generate Allure Report') {
      agent any
      steps {
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

    stage('Archive Reports') {
      agent any
      steps {
        archiveArtifacts artifacts: "${ALLURE_RESULTS_DIR}/**, ${ALLURE_REPORT_DIR}/**, junit-*.xml",
                         fingerprint: true,
                         allowEmptyArchive: true
      }
    }

    stage('Publish Results') {
      agent any
      steps {
        junit allowEmptyResults: true, testResults: 'junit-*.xml'
        echo "Allure HTML report: ${env.BUILD_URL}artifact/${ALLURE_REPORT_DIR}/index.html"
      }
    }
  }

  post {
    cleanup {
      node('') {
        cleanWs()
      }
    }
  }
}