from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
import sys

APP_NAME = "Wikipedia Page Extraction"

def main(sqlc, filename_in, filename_out, limit=None):

        all_pages = sqlc.read.format('com.databricks.spark.xml') \
                .options(rowTag='page') \
                .load(filename_in)
        all_pages.cache()
        print("============================================ Finished loading the data")

        all_battle_pages = all_pages.filter(all_pages.title.rlike("((B|b)attle (of|on))"))
        all_battle_pages.cache()
        print("============================================ Finished filtering %s" % all_battle_pages.count())

        all_battle_pages \
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
                limit=sys.argv[3]

        conf = SparkConf().setAppName(APP_NAME)
        sc = SparkContext(conf=conf)
        sqlc = SQLContext(sc)

        main(sqlc, filename_in, filename_out, limit)

