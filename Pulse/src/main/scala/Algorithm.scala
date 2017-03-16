package org.template.orange

import java.io._
import grizzled.slf4j.Logger
import org.apache.predictionio.controller.{P2LAlgorithm, Params}
import org.apache.spark.SparkContext
import org.apache.spark.mllib.clustering.{KMeans, KMeansModel}
import org.apache.spark.mllib.linalg.{Vector, Vectors}
import scala.io.Source
import scala.collection.mutable.{ArrayBuffer, HashMap}

case class AlgorithmParams(numberOfCenters: Int, numberOfIterations: Int) extends Params

class Algorithm(val ap: AlgorithmParams) extends P2LAlgorithm[PreparedData, KMeansModel, Query, PredictedResult] {

  @transient lazy val logger = Logger[this.type]
  var clusterCentroids: ArrayBuffer[Double] = new ArrayBuffer[Double]()
  var clusterMeanDistances: HashMap[Int, Double] = new HashMap[Int, Double]()

  def train(sc: SparkContext, data : PreparedData): KMeansModel = {
    val kmeans = new KMeans()
    kmeans.setK(ap.numberOfCenters)
    kmeans.setMaxIterations(ap.numberOfIterations)

    val model = kmeans.run(data.events)
    model.clusterCenters.foreach( centroid =>
      clusterCentroids += centroid.toArray(0)
    )
    computeMeanDistances(model, data.events.collect())
    val file = new File("/tmp/meanDistances.csv")
    val bw = new BufferedWriter(new FileWriter(file))
    clusterMeanDistances.foreach { case (k, v) =>
      bw.write(s"$k,$v\n")
    }
    bw.close()
    model
  }

  def predict(model: KMeansModel, query: Query): PredictedResult = {
    // Prefix the query with the model data
    var results: ArrayBuffer[Double] = new ArrayBuffer[Double]()


    // Setting up the required meta data
    model.clusterCenters.foreach( centroid =>
      clusterCentroids += centroid.toArray(0)
    )

    val file = new File("/tmp/meanDistances.csv")
    for (line <- Source.fromFile(file).getLines()) {
      val values = line.trim.split(",")
      clusterMeanDistances(values(0).toInt) = values(1).toDouble
    }

    query.q.foreach( q => {
      val clusterNumber = model.predict(Vectors.dense(q))
      results += computeAnomalyScore(q, clusterNumber)
    })

    PredictedResult(p=results.toArray)
  }

  def computeAnomalyScore(dataPoint: Double, clusterNumber: Int): Double = {
    math.abs(dataPoint-clusterCentroids(clusterNumber)-clusterMeanDistances(clusterNumber))
  }

  def computeMeanDistances(model: KMeansModel, datapoints: Array[Vector]) {
    var clusterPoints: HashMap[Int, ArrayBuffer[Double]] = new HashMap[Int, ArrayBuffer[Double]]()

    // Initializing map with empty arrays
    clusterCentroids.indices.foreach(i =>
      clusterPoints(i) = ArrayBuffer[Double]()
    )

    // Bucketing the data points
    datapoints.foreach(point=>
      clusterPoints(model.predict(point)) += point.toArray(0)
    )

    // Computing the mean distances
    for ((k,v) <- clusterPoints) {
      val distances = v.map(x => {
        if ((clusterCentroids(k) - x) < 0)
          x - clusterCentroids(k)
        else
          clusterCentroids(k) - x
      })
      val mean = distances.foldLeft(0.0)(_ + _)/v.length
      clusterMeanDistances(k) = mean
    }
  }
}

class Model(val mc: Int) extends Serializable {
  override def toString = s"mc=$mc"
}
