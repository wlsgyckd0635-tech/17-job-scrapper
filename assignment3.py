class Product:
    """상품 정보를 관리하는 클래스"""
    
    def __init__(self, product_id, name, price, weight, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.weight = weight
        self.stock = stock
    
    def get_info(self):
        """상품 정보를 딕셔너리로 반환"""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "weight": self.weight,
            "stock": self.stock
        }
    
    def update_stock(self, quantity):
        """
        재고 수량 업데이트
        재고가 부족하면 False 반환, 성공하면 True 반환
        """
        if self.stock >= quantity:
            self.stock = self.stock - quantity
            return True
        else:
            return False
    
    def apply_discount(self, discount_rate):
        """할인율을 적용한 가격 반환 (원본 가격은 유지)"""
       
        discounted_price = self.price * (1 - discount_rate)
        return int(discounted_price)


class ShoppingCart:
    """장바구니를 관리하는 클래스"""
    
    def __init__(self):
        """장바구니 초기화 (상품 목록을 저장할 리스트 생성)"""
        self.cart_list = []
    
    def add_product(self, product, quantity):
        """
        장바구니에 상품 추가
        {'product': Product객체, 'quantity': 수량} 형태로 저장
        """
        self.cart_list.append({
            'product': product, 
            'quantity': quantity
        })
    
    def remove_product(self, product_id):
        """상품 ID로 장바구니에서 상품 제거"""
        new_cart = []
        for item in self.cart_list:
            if item['product'].product_id != product_id:
                new_cart.append(item)
        self.cart_list = new_cart
    
    def get_total_price(self):
        """장바구니 내 모든 상품의 총 금액 계산"""
        total = 0
        for item in self.cart_list:
            total = total + (item['product'].price * item['quantity'])
        return total
    
    def get_total_weight(self):
        """장바구니 내 모든 상품의 총 무게 계산"""
        total_weight = 0
        for item in self.cart_list:
            total_weight = total_weight + (item['product'].weight * item['quantity'])
        return total_weight
    
    def show_cart(self):
        """
        장바구니 내용을 보기 좋게 출력
        각 상품의 이름, 수량, 가격 표시
        """
        print("====== 🛒 장바구니 목록 ======")
        for item in self.cart_list:
            p = item['product']
            q = item['quantity']
            print(f"상품명: {p.name} | 수량: {q}개 | 가격: {p.price * q}원")
        print("==============================")


class Order:
    """주문 정보를 관리하는 클래스"""
    
    def __init__(self, order_id, cart, customer_name):
        self.order_id = order_id
        self.cart = cart
        self.customer_name = customer_name
    
    def calculate_final_price(self):
        """
        최종 결제 금액 계산 (상품 금액 + 배송비)
        기본 배송비 3000원 설정
        """
        shipping_fee = 3000
        return self.cart.get_total_price() + shipping_fee
    
    def print_receipt(self):
        """주문서 출력"""
        print("\n====== 📄 주 문 서 ======")
        print(f"주문 ID   : {self.order_id}")
        print(f"고객명    : {self.customer_name}")
        print("------------------------")
        print("주문 상품 목록:")
        for item in self.cart.cart_list:
            print(f"  - {item['product'].name} ({item['quantity']}개)")
        print("------------------------")
        print(f"상품 금액 : {self.cart.get_total_price()}원")
        print(f"배송비    : 3000원")
        print(f"최종 금액 : {self.calculate_final_price()}원")
        print("========================")


# ==================== 실행 예시 코드 ====================
if __name__ == "__main__":
    
    laptop = Product("P001", "노트북", 1200000, 2.5, 10)
    mouse = Product("P002", "무선마우스", 35000, 0.2, 50)
    keyboard = Product("P003", "기계식키보드", 89000, 1.0, 30)
     
   
    cart = ShoppingCart()
    cart.add_product(laptop, 1)
    cart.add_product(mouse, 2)
    cart.add_product(keyboard, 1)
     
   
    cart.show_cart()
     
    
    order = Order("ORD20260211001", cart, "홍길동")
     
   
    order.print_receipt()