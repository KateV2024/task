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

    stage('Start Services') {
      agent any
      steps {
        script {
          sh '''
            set -e
            # Clean up any existing containers
            docker stop mongo backend frontend || true
            docker rm mongo backend frontend || true

            # Start MongoDB
            docker run -d --name mongo -p 27017:27017 mongo:6.0

            # Start Backend
            docker build -t backend ./backend
            docker run -d --name backend -p 5000:5000 --link mongo:mongo backend

            # Start Frontend
            docker build -t frontend ./frontend
            docker run -d --name frontend -p 3000:3000 --link backend:backend frontend
          '''
        }
      }
    }

    stage('Wait for Services') {
      agent any
      steps {
        sh '''
          set -e
          echo "Waiting for MongoDB to start..."
          until docker exec mongo mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; do
            sleep 2
          done
          echo "MongoDB is up!"

          echo "Waiting for backend to start..."
          until curl -s http://localhost:5000/ > /dev/null 2>&1; do
            sleep 2
          done
          echo "Backend is up!"

          echo "Waiting for frontend to start..."
          until curl -s http://localhost:3000/ > /dev/null 2>&1; do
            sleep 2
          done
          echo "Frontend is up!"
        '''
      }
    }

    stage('Install Dependencies and Run Tests') {
      agent {
        docker {
          image 'mcr.microsoft.com/playwright/python:v1.49.0-noble'
          args '-u root:root --network host'
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
            -v "\${WORKSPACE}/${ALLURE_RESULTS_DIR}:/app/allure-results" \\
            -v "\${WORKSPACE}/${ALLURE_REPORT_DIR}:/app/allure-report" \\
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
    always {
      node('any') {
        // Stop and remove containers
        sh '''
          docker stop frontend backend mongo || true
          docker rm frontend backend mongo || true
        '''
      }
    }
    cleanup {
      node('any') {
        cleanWs()
      }
    }
  }
}