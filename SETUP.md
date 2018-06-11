## AWS環境構築フロー

1. IAMロール(実行ロール)の作成
1. S3バケット作成
1. SAMデプロイパッケージの作成
1. SAMデプロイ
1. SAMアンデプロイ


## IAMロール(実行ロール)の作成

```bash
aws iam create-role \
--role-name todoAppRole \
--assume-role-policy-document file://./trustpolicy.json
```

```json
{
    "Role": {
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17", 
            "Statement": [
                {
                    "Action": "sts:AssumeRole", 
                    "Principal": {
                        "Service": [
                            "lambda.amazonaws.com", 
                            "apigateway.amazonaws.com"
                        ]
                    }, 
                    "Effect": "Allow", 
                    "Sid": ""
                }
            ]
        }, 
        "RoleId": "AROAIHWOPC3A6PKBMPXF2", 
        "CreateDate": "2018-06-11T04:50:40.032Z", 
        "RoleName": "todoAppRole", 
        "Path": "/", 
        "Arn": "arn:aws:iam::182919047280:role/todoAppRole"
    }
}

```

```bash
aws iam put-role-policy \
--role-name todoAppRole \
--policy-name todoAppPolicy \
--policy-document file://./permission.json
```


## S3バケット作成

```bash
aws s3 mb s3://todoCm20180612 --region ap-northeast-1
```


## SAMデプロイ

```bash
aws cloudformation package \
    --template-file template.yml \
    --s3-bucket todoCm20180612 \
    --region ap-northeast-1 \
    --output-template-file packaged-template.yml
```

```bash
aws cloudformation deploy \
    --template-file packaged-template.yml \
    --stack-name todo-app \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides Stage=stg
```

## SAMアンデプロイ

```bash
aws cloudformation delete-stack \
    --stack-name todo-app
```