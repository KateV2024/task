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
            # Clean up any existing containers and network
            docker stop mongo backend frontend || true
            docker rm mongo backend frontend || true
            docker network rm test-network || true

            # Create network
            docker network create test-network

            # Start MongoDB
            docker run -d --name mongo --network test-network -p 27017:27017 mongo:6.0

            # Start Backend
            docker build -t backend ./backend
            docker run -d --name backend --network test-network -p 5000:5000 backend

            # Start Frontend
            docker build -t frontend ./frontend
            docker run -d --name frontend --network test-network -p 3000:3000 frontend
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
          timeout=60
          counter=0
          until docker exec mongo mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1 || [ $counter -ge $timeout ]; do
            sleep 2
            counter=$((counter + 2))
          done
          if [ $counter -ge $timeout ]; then
            echo "MongoDB failed to start within $timeout seconds"
            exit 1
          fi
          echo "MongoDB is up!"

          echo "Waiting for backend to start..."
          counter=0
          until curl -s http://localhost:5000/ > /dev/null 2>&1 || [ $counter -ge $timeout ]; do
            sleep 2
            counter=$((counter + 2))
          done
          if [ $counter -ge $timeout ]; then
            echo "Backend failed to start within $timeout seconds"
            exit 1
          fi
          echo "Backend is up!"

          echo "Waiting for frontend to start..."
          counter=0
          until curl -s http://localhost:3000/ > /dev/null 2>&1 || [ $counter -ge $timeout ]; do
            sleep 2
            counter=$((counter + 2))
          done
          if [ $counter -ge $timeout ]; then
            echo "Frontend failed to start within $timeout seconds"
            exit 1
          fi
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
        sh '''
          docker stop frontend backend mongo || true
          docker rm frontend backend mongo || true
          docker network rm test-network || true
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