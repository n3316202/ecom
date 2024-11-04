from .cart import Cart # 현재폴더 cart.py 에서 Cart객체를 가져옴

def cart(request):
    return {'cart':Cart(request)}
