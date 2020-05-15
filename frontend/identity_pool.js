
console.log('Initialize Cognito')

// Initialize the Amazon Cognito credentials provider
AWS.config.region = 'us-east-1'; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: identityPoolId,
});

get_credential();

function get_credential() {
    AWS.config.credentials.get(function(err, cred) {
        if (!err) {
            console.log(AWS.config.credentials);
            console.log('retrieved identity: ' + AWS.config.credentials.identityId);
            console.log('retrieved identity: ' + AWS.config.credentials.accessKeyId);
            console.log('retrieved identity: ' + AWS.config.credentials.secretAccessKey);
            console.log('retrieved identity: ' + AWS.config.credentials.sessionToken);
            setStatus('AWS Credential Ready.')

        } else {
            self.logger.error('error retrieving identity:' + err);
            alert('error retrieving identity: ' + err);

        }
    });
}

