pipeline {
  agent any
  environment {
    IMAGE      = "ghcr.io/yenlik-lika/java-app"
    TAG        = "v${BUILD_NUMBER}"
    GITOPS_REPO = "github.com/Yenlik-lika/java-redis-gitops.git"
  }
  stages {
    stage('Checkout') { steps { checkout scm } }

    stage('Build & Unit Test') {
      steps { dir('app') { sh 'mvn -B clean package' } }
    }

    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv('sonarqube') {
          dir('app') {
            sh 'mvn -B sonar:sonar -Dsonar.projectKey=java-app -Dsonar.projectName=java-app'
          }
        }
      }
    }

    stage('Quality Gate') {
      steps {
        timeout(time: 5, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }

    stage('Docker Build') {
      steps { dir('app') { sh 'docker build -t $IMAGE:$TAG .' } }
    }

    stage('Security Scan') {
      steps {
        sh 'trivy image --format table --output trivy-report.txt --severity CRITICAL,HIGH $IMAGE:$TAG || true'
        sh 'trivy image --exit-code 1 --severity CRITICAL,HIGH --ignore-unfixed $IMAGE:$TAG'
      }
      post { always { archiveArtifacts artifacts: 'trivy-report.txt', allowEmptyArchive: true } }
    }

    stage('Push Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub',
                         usernameVariable: 'U', passwordVariable: 'P')]) {
          sh 'echo $P | docker login -u $U --password-stdin && docker push $IMAGE:$TAG'
        }
      }
    }

    stage('Update GitOps Manifest') {
      steps {
        withCredentials([string(credentialsId: 'github-token', variable: 'GH')]) {
          sh '''
            sed -i "s|image: .*/java-app:.*|image: $IMAGE:$TAG|" k8s/java-deployment.yaml
            git config user.email "jenkins@ci" && git config user.name "jenkins"
            git commit -am "ci: bump java-app to $TAG" || exit 0
            git push https://$GH@$GITOPS_REPO HEAD:main
          '''
        }
      }
    }
  }
}
