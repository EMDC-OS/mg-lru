import java.time.temporal.ChronoUnit
import org.apache.spark.sql.SparkSession

object SparkSort {
    def main(args: Array[String]): Unit = {
        val spark = SparkSession.builder().getOrCreate()
        val file = sc.textFile("dataset.txt", 32)
        val start = java.time.Instant.now()
        val results = file.flatMap(_.split(",")).map(x => (x, 1)).sortByKey().takeOrdered(10)
        val finish = java.time.Instant.now()
        println(s"wall time: ${ChronoUnit.SECONDS.between(start, finish)}")
        results.foreach(println)
        spark.stop()
    }
}
SparkSort.main(Array())
