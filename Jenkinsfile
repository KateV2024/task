pipeline {
  agent {
    dockerContainer {
      image 'python:3.11'
      args '-u root:root'
    }
  }

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  environment {
    REPO_URL = 'https://github.com/KateV2024/task.git'
    BRANCH = 'main' // change if your default branch differs
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
        wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'xterm']) {
          checkout([$class: 'GitSCM',
            userRemoteConfigs: [[url: "${REPO_URL}"]],
            branches: [[name: "*/${BRANCH}"]],
            extensions: [[$class: 'CleanBeforeCheckout']]
          ])
        }
      }
    }

    stage('Setup Python') {
      steps {
        wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'xterm']) {
          sh """
            set -e
            python -m venv ${VENV_DIR}
            ${PIP} install --upgrade pip
            if [ -f requirements.txt ]; then
              ${PIP} install -r requirements.txt
            elif [ -f automation_framework/requirements.txt ]; then
              ${PIP} install -r automation_framework/requirements.txt
            fi
          """
        }
      }
    }

    stage('Install Playwright Browsers') {
      when {
        expression { return fileExists('requirements.txt') || fileExists('automation_framework/requirements.txt') }
      }
      steps {
        wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'xterm']) {
          sh """
            set -e
            ${PYTHON} -m playwright install --with-deps chromium
          """
        }
      }
    }

    stage('Run All Tests') {
      steps {
        wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'xterm']) {
          sh """
            set -e
            rm -rf ${ALLURE_RESULTS_DIR} ${ALLURE_REPORT_DIR} junit-*.xml || true
            mkdir -p ${ALLURE_RESULTS_DIR}
            ${PYTHON} -m pytest automation_framework/tests \\
              --alluredir=${ALLURE_RESULTS_DIR} \\
              --junitxml=junit-tests.xml \\
              -q
          """
        }
      }
    }

    stage('Generate Allure HTML (Docker)') {
      steps {
        wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'xterm']) {
          sh """
            set -e
            rm -rf ${ALLURE_REPORT_DIR} || true
            docker run --rm \\
              -v "\$PWD/${ALLURE_RESULTS_DIR}:/app/allure-results" \\
              -v "\$PWD/${ALLURE_REPORT_DIR}:/app/allure-report" \\
              -e CHECK_RESULTS_EVERY_SECONDS=0 \\
              "${ALLURE_DOCKER_IMAGE}" generate
          """
        }
      }
    }

    stage('Archive Reports') {
      steps {
        archiveArtifacts artifacts: "${ALLURE_RESULTS_DIR}/**, ${ALLURE_REPORT_DIR}/**, junit-*.xml", fingerprint: true, allowEmptyArchive: true
      }
    }
  }

  post {
    always {
      junit allowEmptyResults: true, testResults: 'junit-*.xml'
      echo "Allure HTML report: ${env.BUILD_URL}artifact/${ALLURE_REPORT_DIR}/index.html"
    }
  }
}