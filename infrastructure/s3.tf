# criar bucket
resource "aws_s3_bucket" "datalake" {
  # parametros do objeto criado
  bucket = "${var.base_bucket_name}-${var.environment}-${var.aws_account}"

  tags = {
    IES       = "IGTI"
    CURSO     = "EDC"
    USE_CASE  = "1"
  }

}

# cria configuração de criptografia do bucket
resource "aws_s3_bucket_server_side_encryption_configuration" "datalake-config" {
  
  bucket = aws_s3_bucket.datalake.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }

}

# cria config acl do bucket
resource "aws_s3_bucket_acl" "datalake-acl" {
  
  bucket  = aws_s3_bucket.datalake.id
  acl     = "private"

}



