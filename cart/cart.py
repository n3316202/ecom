#https://ramyo564.github.io/django/session/
# 아래코드 설명

from store.models import Product, Profile

class Cart():

    def __init__(self,request):
        self.session = request.session

        #Get request
        self.request = request

        #Get the current session key if it exists
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #make suer cart is available
        self.cart = cart

    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        quantities = self.cart

        total = 0

        for key, value in quantities.items():
            #Convert key string into so we 
            key = int(key)

            for product in products:
                if product.id  == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        return total

    def add(self,product, quantity):

        product_id  = str(product.id)
        product_qty = str(quantity)
        
        #>>> a[3] = [1, 2, 3]
        #>>> a
        #{1: 'a', 2: 'b', 'name': 'pey', 3: [1, 2, 3]}

        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # {'3':1,'2':1}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart=str(carty))

            
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        
        # Get ids from cart
        product_ids = self.cart.keys()

        # use ids to lookup products in database model
        products =  Product.objects.filter(id__in=product_ids)
        print("프로덕트", products)
        #Return those looked up products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id =  str(product)
        product_qty = int(quantity)

        ourcart = self.cart

        ourcart[product_id] = product_qty

        self.session.modified = True
        thing = self.cart

        return thing

    def delete(self,product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True    
