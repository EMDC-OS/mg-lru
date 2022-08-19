import java.io._
import scala.collection.mutable.ArrayBuffer

object GenData {
    def main(args: Array[String]): Unit = {
        val file = new File("dataset.txt")
        val writer = new BufferedWriter(new FileWriter(file))
        val buf = ArrayBuffer(0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L)
        for(_ <- 0 until 300000000) {
            for (i <- 0 until 10) {
                buf.update(i, scala.util.Random.nextLong())
            }
            writer.write(s"${buf.mkString(",")}\n")
        }
        writer.close()
    }
}
GenData.main(Array())
