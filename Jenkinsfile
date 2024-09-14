pipeline {
  agent any
  stages {
    stage('Install dependencies') {
      steps {
        sh 'pip3 install -r requirements.txt'
      }
    }

    stage('Run tests') {
      steps {
        sh 'chmod +x ./run_tests.sh'
        sh './run_tests.sh'
      }
    }

    stage('Run ML pipeline') {
      steps {
        sh 'python3 run_python_script.py pipeline ${problem_name} ${ml_pipeline_params_name} ${feature_set_name} ${algorithm_name} ${algorithm_params_name}'
      }
    }

    stage('Production - Register Model and Acceptance Test') {
      when {
        allOf {
          equals expected: 'default', actual: "${params.ml_pipeline_params_name}"
          equals expected: 'default', actual: "${params.feature_set_name}"
          equals expected: 'default', actual: "${params.algorithm_name}"
          equals expected: 'default', actual: "${params.algorithm_params_name}"
        }

      }
      post {
        success {
          sh 'python3 run_python_script.py register_model ${MLFLOW_TRACKING_URL} yes'
        }

        failure {
          sh 'python3 run_python_script.py register_model ${MLFLOW_TRACKING_URL} no'
        }

      }
      steps {
        sh 'python3 run_python_script.py acceptance'
      }
    }

  }
  environment {
    AWS_ACCESS_KEY_ID = 'minio'
    AWS_SECRET_ACCESS_KEY = 'minio123'
    MLFLOW_TRACKING_URL = 'http://mlflow:5000' 
    MLFLOW_S3_ENDPOINT_URL ='http://minio:9000'
  }
  options {
    timestamps()
  }
  parameters {
    choice(name: 'problem_name', choices: ['houses', 'groceries', 'iris'], description: 'Choose the problem name')
    string(name: 'ml_pipeline_params_name', defaultValue: 'default', description: 'Specify the ml_pipeline_params file')
    string(name: 'feature_set_name', defaultValue: 'default', description: 'Specify the feature_set name/file')
    string(name: 'algorithm_name', defaultValue: 'default', description: 'Specify the algorithm (overrides problem_params)')
    string(name: 'algorithm_params_name', defaultValue: 'default', description: 'Specify the algorithm params')
  }
  triggers {
    pollSCM('* * * * *')
  }
}