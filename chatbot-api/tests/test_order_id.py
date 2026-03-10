from chatbot_api.app.utils import extract_order_id

def test_extract_order_id():
    assert extract_order_id("meu pedido é PED-1001") == "PED-1001"
    assert extract_order_id("pedido ped-9999") == "PED-9999"
    assert extract_order_id("sem id aqui") is None
