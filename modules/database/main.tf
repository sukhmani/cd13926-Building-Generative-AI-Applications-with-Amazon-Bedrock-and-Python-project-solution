module "bedrock_kb" {
  source = "../modules/bedrock_kb"

  knowledge_base_name        = "my-bedrock-kb"
  knowledge_base_description = "Knowledge base for Bedrock RAG with Aurora and S3"

  aurora_arn                 = "arn:aws:rds:us-west-2:621074666262:cluster:my-aurora-serverless"
  aurora_db_name             = "myapp"
  aurora_endpoint            = "my-aurora-serverless.cluster-xxxxxxxxxx.us-west-2.rds.amazonaws.com"
  aurora_table_name          = "bedrock_integration.bedrock_kb"
  aurora_username            = "mydbuser"
  aurora_secret_arn          = "arn:aws:secretsmanager:us-west-2:621074666262:secret:my-aurora-serverless-rovkox"

  aurora_primary_key_field   = "id"
  aurora_vector_field        = "embedding"         
  aurora_text_field          = "chunks"
  aurora_metadata_field      = "metadata"

  s3_bucket_arn              = "arn:aws:s3:::bedrock-kb-621074666262"
}
