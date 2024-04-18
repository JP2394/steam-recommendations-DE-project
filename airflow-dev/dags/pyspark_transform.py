
import pyspark
from pyspark.sql import types, SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql.functions import col, regexp_replace, to_timestamp, split,concat_ws, collect_list,length, trim,ltrim
from pyspark.sql.types import StructType, StructField, StringType, IntegerType



spark = SparkSession.builder.appName('pyspark_steams').getOrCreate()




def define_schema(df,table_name):

    if table_name=='games':
        df=df.withColumn('app_id',col('app_id').cast(types.IntegerType())) \
                        .withColumn('title',col('title').cast(types.StringType())) \
                        .withColumn('date_release',col('date_release').cast(types.TimestampType())) \
                        .withColumn('win',col('win').cast(types.StringType())) \
                        .withColumn('mac',col('mac').cast(types.StringType())) \
                        .withColumn('linux',col('linux').cast(types.StringType())) \
                        .withColumn('rating',col('rating').cast(types.StringType())) \
                        .withColumn('price_final',col('price_final').cast(types.FloatType())) \
                        .withColumn('price_original',col('price_original').cast(types.FloatType())) \
                        .withColumn('discount',col('discount').cast(types.IntegerType())) \
                        .withColumn('steam_deck',col('steam_deck').cast(types.StringType()))

    if table_name=='recommendations':
        df=df.withColumn('app_id',col('app_id').cast(types.IntegerType())) \
                        .withColumn('helpful',col('helpful').cast(types.IntegerType())) \
                        .withColumn('funny',col('funny').cast(types.IntegerType())) \
                        .withColumn('date',col('date').cast(types.TimestampType())) \
                        .withColumn('is_recommended',col('is_recommended').cast(types.BooleanType())) \
                        .withColumn('hours',col('hours').cast(types.FloatType())) \
                        .withColumn('user_id',col('user_id').cast(types.IntegerType())) \
                        .withColumn('review_id',col('review_id').cast(types.IntegerType()))
        
    if table_name=='users':
       df=df.withColumn('user_id',col('user_id').cast(types.IntegerType())) \
                        .withColumn('products',col('products').cast(types.IntegerType())) \
                        .withColumn('reviews',col('reviews').cast(types.IntegerType()))  
        
        
    return df 


def transform(df, table_name):
    if table_name=='games':
        columns_to_drop = ["price_final", "positive_ratio",'discount']
        df= df.drop(*columns_to_drop)
    return df 


def spark_to_gcs(df, table_name):
    df.write \
    .format("parquet") \
    .option("header", "true") \
    .save(f"gs://dtc_data_lake_steam/processed/{table_name}")
    


def run_pyspark(df,table_name):
    df = define_schema(df,table_name)
    df = transform(df, table_name)
    spark_to_gcs(df, table_name)


if __name__ == "__main__":
    for table_name in ['games','recommendations','users']:
        gcs_path = f"gs://dtc_data_lake_steam/raw/{table_name}.csv"
        df =spark.read.csv(gcs_path,header=True )
        run_pyspark(df,table_name)


