import math
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from robo_interfaces.action import Deslocamento


class RoboDeslocamentoServidor(Node):
    def __init__(self):
        super().__init__("robo_deslocamento_servidor")
        self.lat = 0.0
        self.lon = 0.0
        self.group = ReentrantCallbackGroup()
        self.server = ActionServer(
            self,
            Deslocamento,
            "deslocamento",
            execute_callback=self.execute_cb,
            goal_callback=self.goal_cb,
            cancel_callback=self.cancel_cb,
            callback_group=self.group,
        )
        self.get_logger().info("Servidor deslocamento pronto em (0.0, 0.0)")

    def goal_cb(self, goal):
        self.get_logger().info(
            f"Meta recebida: lat={goal.latitude} lon={goal.longitude}"
        )
        return GoalResponse.ACCEPT

    def cancel_cb(self, goal_handle):
        self.get_logger().info("Cancelamento solicitado")
        return CancelResponse.ACCEPT

    def execute_cb(self, goal_handle):
        goal = goal_handle.request
        result = Deslocamento.Result()
        feedback = Deslocamento.Feedback()
        result.distancia_percorrida = 0.0

        vlat = abs(goal.vel_latitude)
        vlon = abs(goal.vel_longitude)
        falta_lat = goal.latitude - self.lat
        falta_lon = goal.longitude - self.lon

        # Mesma localizacao: sem sucesso
        if falta_lat == 0.0 and falta_lon == 0.0:
            self.get_logger().warn("Localizacao igual a atual")
            goal_handle.abort()
            return result

        # Velocidade zero em um eixo que precisa andar: nunca chegaria
        if (falta_lat != 0.0 and vlat == 0.0) or (falta_lon != 0.0 and vlon == 0.0):
            self.get_logger().warn("Velocidade invalida para chegar a meta")
            goal_handle.abort()
            return result

        distancia = 0.0
        while rclpy.ok():
            time.sleep(1.0)

            if goal_handle.is_cancel_requested:
                result.distancia_percorrida = distancia
                goal_handle.canceled()
                self.get_logger().info(f"Cancelado. Distancia: {distancia:.2f}")
                return result

            dlat = goal.latitude - self.lat
            dlon = goal.longitude - self.lon
            ant_lat, ant_lon = self.lat, self.lon

            if abs(dlat) <= vlat:
                self.lat = goal.latitude
            else:
                self.lat += math.copysign(vlat, dlat)
            if abs(dlon) <= vlon:
                self.lon = goal.longitude
            else:
                self.lon += math.copysign(vlon, dlon)

            distancia += math.hypot(self.lat - ant_lat, self.lon - ant_lon)

            feedback.latitude_atual = self.lat
            feedback.longitude_atual = self.lon
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(
                f"Posicao: ({self.lat:.2f}, {self.lon:.2f}) distancia={distancia:.2f}"
            )

            if self.lat == goal.latitude and self.lon == goal.longitude:
                break

        result.distancia_percorrida = distancia
        goal_handle.succeed()
        return result


def main(args=None):
    rclpy.init(args=args)
    node = RoboDeslocamentoServidor()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == "__main__":
    main()