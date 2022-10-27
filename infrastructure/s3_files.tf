resource "aws_s3_object" "delta_insert" {

  bucket = aws_s3_bucket.datalake.id

  # remote location for the file
  key = "emr-code/pyspark/01_delta_spark_insert.py"
  acl = "private"

  # local location of the file
  source = "../etl/01_delta_spark_insert.py"
  # only update the file if MD5 check is different
  etag = filemd5("../etl/01_delta_spark_insert.py")

}


resource "aws_s3_object" "delta_upsert" {

  bucket = aws_s3_bucket.datalake.id

  # remote location for the file
  key = "emr-code/pyspark/02_delta_spark_upsert.py"
  acl = "private"

  # local location of the file
  source = "../etl/02_delta_spark_upsert.py"
  # only update the file if MD5 check is different
  etag = filemd5("./etl/02_delta_spark_upsert.py")

}