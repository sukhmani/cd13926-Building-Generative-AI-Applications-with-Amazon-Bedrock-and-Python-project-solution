provider "aws" {
  region = "us-west-2"
}

module "bedrock_kb" {
  source = "../modules/bedrock_kb"

  # Knowledge Base metadata
  knowledge_base_name        = "my-bedrock-kb"
  knowledge_base_description = "Knowledge base connected to Aurora Serverless database"

  # Aurora configuration
  aurora_arn                 = "arn:aws:rds:us-west-2:245403145430:cluster:my-aurora-serverless"
  aurora_db_name             = "myapp"
  aurora_endpoint            = "my-aurora-serverless.cluster-cfpcpqajvwgv.us-west-2.rds.amazonaws.com"
  aurora_table_name          = "bedrock_integration.bedrock_kb"
  aurora_primary_key_field   = "id"
  aurora_metadata_field      = "metadata"
  aurora_text_field = "content"

  aurora_verctor_field       = "embedding"
  aurora_username            = "dbadmin"


  aurora_secret_arn          = "arn:aws:secretsmanager:us-west-2:245403145430:secret:my-aurora-serverless-TnyA3G"

  # S3 configuration
  s3_bucket_arn              = "arn:aws:s3:::bedrock-kb-245403145430"
}
