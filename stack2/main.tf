resource "aws_iam_role_policy" "bedrock_kb_rds_access" {
  name = "bedrock-kb-rds-access"
  role = aws_iam_role.bedrock_kb_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "rds:DescribeDBClusters",
          "rds:DescribeDBInstances",
          "rds:DescribeDBSubnetGroups",
          "secretsmanager:GetSecretValue"
        ],
        Resource = "*"
      }
    ]
  })
}



provider "aws" {
  region = "us-west-2"
}


resource "aws_iam_role" "bedrock_kb_role" {
  name = "my-bedrock-kb-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "bedrock.amazonaws.com"
        }
      }
    ]
  })
}

module "bedrock_kb" {
  source = "../modules/bedrock_kb" 

  knowledge_base_name        = "my-bedrock-kb"
  knowledge_base_description = "Knowledge base connected to Aurora Serverless database"

 
  role_arn = aws_iam_role.bedrock_kb_role.arn

  aurora_arn                 = "arn:aws:rds:us-west-2:621074666262:cluster:my-aurora-serverless"
  aurora_db_name             = "myapp"
  aurora_endpoint            = "my-aurora-serverless.cluster-cs20rasuw1hx.us-west-2.rds.amazonaws.com"
  aurora_table_name          = "bedrock_integration.bedrock_kb"
  aurora_primary_key_field   = "id"
  aurora_metadata_field      = "metadata"
  aurora_text_field          = "chunks"
  aurora_vector_field        = "embedding"
  aurora_username            = "dbadmin"
  aurora_secret_arn          = "arn:aws:secretsmanager:us-west-2:621074666262:secret:my-aurora-serverless-rovkox"
  s3_bucket_arn              = "arn:aws:s3:::bedrock-kb-621074666262"
}
