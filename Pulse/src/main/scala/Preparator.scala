package org.template.orange

import grizzled.slf4j.Logger
import org.apache.predictionio.controller.PPreparator
import org.apache.spark.SparkContext
import org.apache.spark.mllib.linalg.{Vector, Vectors}
import org.apache.spark.rdd.RDD

class Preparator extends PPreparator[TrainingData, PreparedData] {
  @transient lazy val logger = Logger[this.type]

  def prepare(sc: SparkContext, trainingData: TrainingData): PreparedData = {
    val dataVector = trainingData.events.collect()
    val dplist = dataVector.map{ (event) => Vectors.dense(event.properties.get[Double]("attr0"))}
    new PreparedData(events = sc.parallelize(dplist))
  }
}

class PreparedData(
  val events: RDD[Vector]
) extends Serializable
