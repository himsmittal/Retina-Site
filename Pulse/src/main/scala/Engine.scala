package org.template.orange

import org.apache.predictionio.controller.EngineFactory
import org.apache.predictionio.controller.Engine

case class Query(q: Array[Double]) extends Serializable

case class PredictedResult(p: Array[Double]) extends Serializable

object OrangeEngine extends EngineFactory {
  def apply() = {
    new Engine(
      classOf[DataSource],
      classOf[Preparator],
      Map("algo" -> classOf[Algorithm]),
      classOf[Serving])
  }
}
