import random

cardapio = {
    "chocolate": 5.00,
    "baunilha": 4.50,
    "morango": 3.00,
    "flocos": 9.00,
    
}

brinde = ["Canudo", "Copo", "Gelo", "Badge"]

def mostar_cardapio():
    print("-- CARDAPIO --")
    for sabor, preco in cardapio.items():
        print(f"{sabor.title()}, R${preco:.2f}")

def fazer_pedido():
    total = 0
    pedido = []
    while True:
        sabor = input("\nQual sabor? (digite 0 para finalizar)")
        if sabor == "0":
            break
        elif sabor in cardapio:
            total += cardapio[sabor]
            pedido.append(sabor)
            print(f"{sabor} adicionado!")
        else:
            print("Sabor não está no cardápio!")
    return pedido, total

    



mostar_cardapio()
pedido, total = fazer_pedido()
            
print(f"\nSeu pedido foi: {pedido}")
print(f"Total: R${total:.2f}")

if total > 15:
    print(f"Você recebeu um brinde: {random.choice(brinde)}")