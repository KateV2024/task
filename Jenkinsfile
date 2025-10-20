pipeline {
  agent {
    docker {
      image 'python:3.14-slim'
      args '-u root:root -v /var/run/docker.sock:/var/run/docker.sock'
    }
  }

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  environment {
    VENV_DIR = '.venv'
    PYTHON = "${env.WORKSPACE}/${VENV_DIR}/bin/python"
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

    stage('Setup Python') {
      steps {
        sh """
          set -e
          python3 -m venv ${VENV_DIR}
          ${PIP} install --upgrade pip
          if [ -f requirements.txt ]; then
            ${PIP} install -r requirements.txt
          elif [ -f automation_framework/requirements.txt ]; then
            ${PIP} install -r automation_framework/requirements.txt
          else
            echo "WARNING: No requirements.txt found"
            exit 1
          fi
        """
      }
    }

    stage('Install Playwright Browsers') {
      steps {
        sh """
          set -e
          apt-get update && apt-get install -y wget gnupg
          ${PYTHON} -m playwright install --with-deps chromium
        """
      }
    }

    stage('Run All Tests') {
      steps {
        sh """
          set -e
          rm -rf ${ALLURE_RESULTS_DIR} ${ALLURE_REPORT_DIR} junit-*.xml || true
          mkdir -p ${ALLURE_RESULTS_DIR}
          ${PYTHON} -m pytest tests \\
            --alluredir=${ALLURE_RESULTS_DIR} \\
            --junitxml=junit-tests.xml \\
            -v
        """
      }
    }

    stage('Generate Allure Report') {
      steps {
        sh """
          set -e
          apt-get update && apt-get install -y docker.io || true
          rm -rf ${ALLURE_REPORT_DIR} || true
          docker run --rm \\
            -v "\${WORKSPACE}/${ALLURE_RESULTS_DIR}:/app/allure-results" \\
            -v "\${WORKSPACE}/${ALLURE_REPORT_DIR}:/app/allure-report" \\
            -e CHECK_RESULTS_EVERY_SECONDS=0 \\
            ${ALLURE_DOCKER_IMAGE} generate
        """
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