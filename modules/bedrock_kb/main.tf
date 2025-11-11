resource "aws_bedrockagent_knowledge_base" "main" {
  name     = var.knowledge_base_name
  role_arn = var.role_arn


  

  knowledge_base_configuration {
  type = "VECTOR"

  vector_knowledge_base_configuration {
    embedding_model_arn = "arn:aws:bedrock:us-west-2::foundation-model/amazon.titan-embed-text-v1"
  }
}


  storage_configuration {
    type = "RDS"

    rds_configuration {
      credentials_secret_arn = var.aurora_secret_arn
      database_name          = var.aurora_db_name
      resource_arn           = var.aurora_arn
      table_name             = var.aurora_table_name

      field_mapping {
        primary_key_field = var.aurora_primary_key_field
        vector_field      = var.aurora_vector_field
        text_field        = var.aurora_text_field
        metadata_field    = var.aurora_metadata_field
      }
    }
  }

 
}
