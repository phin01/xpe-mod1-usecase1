resource "aws_lambda_function" "executa_emr" {

    filename            = "lambda_function_payload.zip"
    function_name       = var.lambda_function_name
    role                = aws_iam_role.lambda.arn
    
    # nome da função 'handler', no arquivo 'lambda_function.py'
    handler             = "lambda_function.handler"
    runtime             = "python3.8"
    
    memory_size         = 128
    timeout             = 30

    source_code_hash    = filebase64sha256("lambda_function_payload.zip")
    
    tags = {
        IES = "IGTI"
        CURSO = "EDC"
        USE_CASE = "1"
    }
}