
import sys

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from robo_interfaces.action import Deslocamento


class RoboDeslocamentoCancela(Node):

    def __init__(self):
        super().__init__("robo_deslocamento_cancela")

        self.client = ActionClient(
            self,
            Deslocamento,
            "deslocamento"
        )

        self.goal_handle = None
        self.timer = None

    def enviar(self, lat, lon, vlat, vlon):
        self.get_logger().info("Aguardando servidor da ação...")

        self.client.wait_for_server()

        goal = Deslocamento.Goal()
        goal.latitude = lat
        goal.longitude = lon
        goal.vel_latitude = vlat
        goal.vel_longitude = vlon

        self.get_logger().info(
            f"Enviando meta: ({lat}, {lon}); cancelamento em 5 segundos"
        )

        future = self.client.send_goal_async(
            goal,
            feedback_callback=self.feedback_cb
        )

        future.add_done_callback(self.resposta_cb)

    def resposta_cb(self, future):
        self.goal_handle = future.result()

        if not self.goal_handle.accepted:
            self.get_logger().error("Meta rejeitada pelo servidor.")
            rclpy.shutdown()
            return

        self.get_logger().info("Meta aceita pelo servidor.")

        result_future = self.goal_handle.get_result_async()
        result_future.add_done_callback(self.resultado_cb)

        self.timer = self.create_timer(
            5.0,
            self.cancelar
        )

    def feedback_cb(self, feedback_msg):
        fb = feedback_msg.feedback

        self.get_logger().info(
            f"Feedback: latitude={fb.latitude_atual:.2f}, "
            f"longitude={fb.longitude_atual:.2f}"
        )

    def cancelar(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

        if self.goal_handle is None:
            return

        self.get_logger().info("Solicitando cancelamento da ação...")

        future = self.goal_handle.cancel_goal_async()
        future.add_done_callback(self.cancelamento_cb)

    def cancelamento_cb(self, future):
        resposta = future.result()

        if len(resposta.goals_canceling) > 0:
            self.get_logger().info("Cancelamento aceito pelo servidor.")
        else:
            self.get_logger().warning(
                "O servidor não aceitou o cancelamento."
            )

    def resultado_cb(self, future):
        resultado = future.result().result

        self.get_logger().info(
            f"Distância percorrida: "
            f"{resultado.distancia_percorrida:.2f}"
        )

        if rclpy.ok():
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)

    padrao = [30.0, 30.0, 1.0, 1.0]
    argumentos = sys.argv[1:5]

    try:
        valores = [float(v) for v in argumentos]
    except ValueError:
        print(
            "Erro: informe valores numéricos para latitude, longitude "
            "e velocidades."
        )
        rclpy.shutdown()
        return

    valores += padrao[len(valores):]

    lat, lon, vlat, vlon = valores

    node = RoboDeslocamentoCancela()

    try:
        node.enviar(lat, lon, vlat, vlon)
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        if rclpy.ok():
            rclpy.shutdown()

        node.destroy_node()


if __name__ == "__main__":
    main()
