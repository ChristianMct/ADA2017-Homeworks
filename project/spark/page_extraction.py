from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import StructField, StructType, StringType, IntegerType
import sys

APP_NAME = "Wikipedia Page Extraction"


def main(sqlc, filename_in, filename_out, limit=None):

    schem = StructType([
        StructField("title", StringType(), False),
        StructField("id", IntegerType(), False),
        StructField("revision", StructType([
            StructField("id", IntegerType(), False),
            StructField("model", StringType(), True),
            StructField("format", StringType(), True),
            StructField("text", StringType(), True)
        ]), False)
    ])

    all_pages = sqlc.read.format('com.databricks.spark.xml') \
        .options(rowTag='page') \
        .load(filename_in, schema=schem)

    print("============================================ Finished loading the data")

    all_battle_pages = all_pages.filter(all_pages.title.rlike("((B|b)attle (of|on))"))

    if limit:
        all_battle_pages = all_battle_pages.limit(limit)

    all_battle_pages.cache()

    print("============================================ Finished filtering %s" % all_battle_pages.count())

    t = all_battle_pages
    all_battle_pages \
        .select(t.id,
                t.title,
                t.revision.id.alias('rev_id'),
                t.revision.model.alias('model'),
                t.revision.format.alias('format'),
                t.revision.text.alias('text')) \
        .coalesce(1) \
        .write.format('com.databricks.spark.xml') \
        .options(rowTag='page', rootTag='pages') \
        .save(filename_out)


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Incorrect number of argument passed to the job")
        sys.exit(1)

    filename_in = sys.argv[1]
    filename_out = sys.argv[2]
    limit = None

    if len(sys.argv) >= 4:
        limit = int(sys.argv[3])

    conf = SparkConf().setAppName(APP_NAME)
    sc = SparkContext(conf=conf)
    sqlc = SQLContext(sc)

    main(sqlc, filename_in, filename_out, limit)
