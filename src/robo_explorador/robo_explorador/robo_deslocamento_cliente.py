import sys

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from robo_interfaces.action import Deslocamento


class RoboDeslocamentoCliente(Node):
    def __init__(self):
        super().__init__("robo_deslocamento_cliente")
        self.client = ActionClient(self, Deslocamento, "deslocamento")

    def enviar(self, lat, lon, vlat, vlon):
        self.client.wait_for_server()
        goal = Deslocamento.Goal()
        goal.latitude = lat
        goal.longitude = lon
        goal.vel_latitude = vlat
        goal.vel_longitude = vlon
        self.get_logger().info(f"Enviando meta: ({lat}, {lon}) vel=({vlat}, {vlon})")
        future = self.client.send_goal_async(goal, feedback_callback=self.feedback_cb)
        future.add_done_callback(self.resposta_cb)

    def resposta_cb(self, future):
        handle = future.result()
        if not handle.accepted:
            self.get_logger().error("Meta rejeitada")
            rclpy.shutdown()
            return
        handle.get_result_async().add_done_callback(self.resultado_cb)

    def feedback_cb(self, msg):
        fb = msg.feedback
        self.get_logger().info(
            f"Feedback: ({fb.latitude_atual:.2f}, {fb.longitude_atual:.2f})"
        )

    def resultado_cb(self, future):
        res = future.result().result
        self.get_logger().info(f"Distancia percorrida: {res.distancia_percorrida:.2f}")
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    valores = [float(v) for v in sys.argv[1:5]]
    padrao = [6.0, 8.0, 1.0, 1.0]
    lat, lon, vlat, vlon = valores + padrao[len(valores):]
    node = RoboDeslocamentoCliente()
    node.enviar(lat, lon, vlat, vlon)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()