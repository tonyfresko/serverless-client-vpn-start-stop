# serverless-client-vpn-start-stop
A Serverless service to start and stop AWS Client VPN Endpoint Associations in order to save costs

## Usage
This service is deployed with the Serverless Framework https://www.serverless.com/framework/docs/getting-started/

This package assumes that you have already set up the Client VPN Endpoint, and wish to automate it starting and stopping

The only configuation required is setting the `CLIENT_VPN_ENDPOINT_ID` and `SUBNET_N` environment variables in `serverless.yml`, and also configuring the cron expressions to times which suit you.
