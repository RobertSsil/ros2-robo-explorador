import random

import rclpy
from rclpy.node import Node
from robo_interfaces.srv import ColetaAmostra


class RoboColetaCliente(Node):
    def __init__(self):
        super().__init__("robo_coleta_cliente")
        self.client = self.create_client(ColetaAmostra, "coleta_material")

    def coletar(self):
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Aguardando servico coleta_material...")
        req = ColetaAmostra.Request()
        req.profundidade = random.uniform(0.1, 0.5)
        self.get_logger().info(f"Solicitando coleta a {req.profundidade:.2f}")
        future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        if future.result().sucesso:
            self.get_logger().info("Coleta bem sucedida")
        else:
            self.get_logger().info("Coleta mal sucedida")


def main(args=None):
    rclpy.init(args=args)
    node = RoboColetaCliente()
    node.coletar()
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == "__main__":
    main()