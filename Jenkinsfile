pipeline {
  agent any // Runs on any available Jenkins agent

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  environment {
    VENV_DIR = '.venv'
    PYTHON = "${env.WORKSPACE}/${VENV_DIR}/bin/python3"
    PIP = "${env.WORKSPACE}/${VENV_DIR}/bin/pip"
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

    stage('Setup Python Environment') {
      steps {
        sh """
          set -e
          # Create virtual environment
          python3 -m venv ${VENV_DIR}
          # Upgrade pip
          ${PIP} install --upgrade pip
          # Install project requirements
          if [ -f requirements.txt ]; then
            ${PIP} install -r requirements.txt
          elif [ -f automation_framework/requirements.txt ]; then
            ${PIP} install -r automation_framework/requirements.txt
          else
            echo "ERROR: No requirements.txt found. Please create one."
            exit 1
          fi
        """
      }
    }

    stage('Install Playwright Browsers') {
      steps {
        sh """
          set -e
          # Install Playwright browsers (e.g., Chromium)
          ${PYTHON} -m playwright install --with-deps chromium
        """
      }
    }

    stage('Run All Tests') {
      steps {
        sh """
          set -e
          # Clean up previous results and create directory for new ones
          rm -rf ${ALLURE_RESULTS_DIR} ${ALLURE_REPORT_DIR} junit-*.xml || true
          mkdir -p ${ALLURE_RESULTS_DIR}
          # Execute pytest
          ${PYTHON} -m pytest tests \\
            --alluredir=${ALLURE_RESULTS_DIR} \\
            --junitxml=junit-tests.xml \\
            -v
        """
      }
    }

    stage('Generate Allure Report') {
      steps {
        script {
          // Check if Docker is available
          def docker_available = sh(script: 'docker info > /dev/null 2>&1 || { echo "Docker not found"; exit 1; }', returnStatus: true) == 0
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