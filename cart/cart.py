#https://ramyo564.github.io/django/session/
# 아래코드 설명

class Cart():

    def __init__(self,request):
        self.session = request.session

        #Get the current session key if it exists
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #make suer cart is available
        self.cart = cart

    def add(self,product):

        product_id  = str(product.id)

        #>>> a[3] = [1, 2, 3]
        #>>> a
        #{1: 'a', 2: 'b', 'name': 'pey', 3: [1, 2, 3]}

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)}
        
        self.session.modified = True
            
