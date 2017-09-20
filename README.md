# Proxy LBC podcasts

This is a little script that runs on AWS Lambda because my podcast client
doesn't support the password-protected XML feeds offered by [LBC][lbc-podcast].

[lbc-podcast]: http://lbc.audioagain.com/

## Environment variables

- `USERNAME` and `PASSWORD`: credentials for the LBC podcast service
- `S3_BUCKET_NAME`: an S3 bucket you can upload to
- `S3_FEED_KEY`: a random string of characters to "protect" the file

## Development

```
pip install -r requirements.txt
lambda invoke
```

## Deployment

Copy and paste it into the AWS Lambda web interface.

### Scheduling

Use CloudWatch Events to trigger it periodically.

### Access

The Lambda function will need a service role attached which has access to read
and write to the specified S3 bucket.
