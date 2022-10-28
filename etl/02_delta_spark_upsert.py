import logging
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min, max, lit

# Configuracao de logs de aplicacao
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger('datalake_enem_small_upsert')
logger.setLevel(logging.DEBUG)

# Definicao da Spark Session
spark = (SparkSession.builder.appName("DeltaExercise")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)


logger.info("Importing delta.tables...")
from delta.tables import *


logger.info("Produzindo novos dados...")
enemnovo = (
    spark.read.format("delta")
    .load("s3://datalake-edc-usecase1-tf-dev-1234567/staging-zone/modulo-1/enem/")
)

# Define algumas inscricoes (chaves) que serao alteradas
inscricoes = [200006177608,
            200005859107,
            200006601650,
            200004252009,
            200004745615,
            200004578512,
            200004770327,
            200004108272,
            200002591497,
            200001214485,
            200004216415,
            200006312232,
            200006487611,
            200004299700,
            200006159215,
            200005206477,
            200001886915,
            200001748808,
            200001336591,
            200002421709,
            200003127063,
            200006455299,
            200003789904,
            200003223827,
            200001116313,
            200003921286,
            200002773418,
            200004943082,
            200002604167,
            200002366435,
            200006354213,
            200003273171,
            200005975528,
            200004129232,
            200006131601,
            200001019619,
            200005282550,
            200006198885,
            200003642153,
            200005954626,
            200004345816,
            200006369608,
            200003733552,
            200005903951,
            200003339032,
            200003835030,
            200002075869,
            200001299415,
            200001092723,
            200005574268]


logger.info("Reduz a 50 casos e faz updates internos no municipio de residencia")
enemnovo = enemnovo.where(enemnovo.nu_inscricao.isin(inscricoes))
enemnovo = enemnovo.withColumn("no_municipio_esc", lit("NOVA CIDADE")).withColumn("co_municipio_esc", lit(10000000))


logger.info("Pega os dados do Enem velhos na tabela Delta...")
enemvelho = DeltaTable.forPath(spark, "s3://datalake-edc-usecase1-tf-dev-1234567/staging-zone/modulo-1/enem/")


logger.info("Realiza o UPSERT...")
(
    enemvelho.alias("old")
    .merge(enemnovo.alias("new"), "old.nu_inscricao = new.nu_inscricao")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

logger.info("Atualizacao completa! \n\n")

logger.info("Gera manifesto symlink...")
enemvelho.generate("symlink_format_manifest")

logger.info("Manifesto gerado.")