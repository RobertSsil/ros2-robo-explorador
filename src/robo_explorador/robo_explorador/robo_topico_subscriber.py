
import rclpy
from rclpy.node import Node
from robo_interfaces.msg import Monitoramento


class RoboTopicoSubscriber(Node):
    def __init__(self):
        super().__init__("robo_topico_subscriber")

        self.subscription = self.create_subscription(
            Monitoramento,
            "/monitoramento",
            self.callback,
            10
        )

        self.get_logger().info("MONITORAMENTO INICIADO!")
        self.get_logger().info("Aguardando dados do robo...")


    def callback(self, msg):
        self.get_logger().info(
            f"Recebido: oxigenio={msg.oxigenio:.1f}, "
            f"temperatura={msg.temperatura:.1f}"
        )

        if 10 <= msg.temperatura <= 40 and msg.oxigenio > 80:
            estado = "Safe"
        else:
            estado = "Not Safe"

        self.get_logger().info(f"ESTADO DO ROBO: {estado}")


def main(args=None):
    rclpy.init(args=args)
    node = RoboTopicoSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
