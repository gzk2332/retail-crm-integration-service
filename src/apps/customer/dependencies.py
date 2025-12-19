from apps.customer.services.customer_service import CustomerService


def get_customer_service() -> CustomerService:
    return CustomerService()
