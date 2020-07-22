from pizza_boom.core.handlers import LambdaBase, lambda_injector
from pizza_boom.pizza_orders.business_logic.pizza_order_failed import pizza_order_failed


class FailPizzaOrderLambda(LambdaBase):
    def handler(self, event, context):
        error_info: dict = event['error_info']
        pizza_order_failed(
            pizza_order_id=event['pizza_order_id'],
            error=error_info['Error'],
            cause=error_info['Cause']
        )


handler = lambda_injector.get(FailPizzaOrderLambda).get_handler()
