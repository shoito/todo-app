## AWS環境構築フロー

1. S3バケット作成
1. SAMデプロイパッケージの作成
1. SAMデプロイ
1. SAMアンデプロイ


## S3バケット作成

```bash
aws s3 mb s3://shoito20180612 --region ap-northeast-1
```


## SAMデプロイ

```bash
aws cloudformation package \
    --template-file template.yml \
    --s3-bucket shoito20180612 \
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