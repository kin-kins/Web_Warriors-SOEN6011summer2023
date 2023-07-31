node {
    // This block specifies that the pipeline should run on any available Jenkins agent.

    stage('Docker Build') {

        sh 'docker build -t shanem/spring-petclinic:latest .'
    }

    stage('Test') {
        // This is the "Test" stage. You can run your tests or any other validation steps here.
        // For example, running unit tests for your application.

        // Replace the below 'sh' command with the appropriate test command for your application.
        sh 'echo "Running tests..."'
    }

    stage('Deploy') {
        // This is the "Deploy" stage. You can deploy your application to the desired environment here.
        // For example, pushing the Docker image to a container registry or deploying to a server.

        // Replace the below 'sh' command with the appropriate deployment command for your application.
        sh 'echo "Deploying the application..."'
    }

    // You can add more stages for additional steps like integration tests, security scans, etc.

    // Post section for cleanup or notifications after the pipeline is executed.
    post {
        always {
            // Clean up Docker images or resources if required.
            // For example:
            // sh 'docker rmi shanem/spring-petclinic:latest'

            // Send notifications about the build status. This can be Slack, email, etc.
            // Replace the 'slackSend' step with the appropriate notification plugin.
            // Example:
            // slackSend channel: '#build-notifications', message: "Pipeline for Spring Petclinic completed."
        }
    }
}
