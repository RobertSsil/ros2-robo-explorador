import random

import rclpy
from rclpy.node import Node
from robo_interfaces.srv import ColetaAmostra


class RoboColetaServidor(Node):
    def __init__(self):
        super().__init__("robo_coleta_servidor")
        self.create_service(ColetaAmostra, "coleta_material", self.callback)
        self.get_logger().info("Servico coleta_material pronto")

    def callback(self, request, response):
        response.sucesso = random.random() <= 0.7
        self.get_logger().info(
            f"Profundidade={request.profundidade:.2f} -> sucesso={response.sucesso}"
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = RoboColetaServidor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == "__main__":
    main()