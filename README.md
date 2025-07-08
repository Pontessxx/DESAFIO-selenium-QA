# 🚀 SauceDemo Test Automation
![banner](https://raw.githubusercontent.com/Pontessxx/DESAFIO-selenium-QA/main/assets/image.png)

Automação de ponta a ponta dos principais fluxos do site [SauceDemo](https://www.saucedemo.com/) usando Python + Selenium. Este repositório contém um único teste que cobre login, carrinho, checkout e confirmação de pedido.

## 🛠️ Tecnologias e Dependências (Versões)

- **Python** = 3.12.6 
- **Selenium** = 4.34.1
- **pytest** = 8.4.1
- **webdriver-manager** = 4.0.2

# Como executar os testes

Você pode rodar com :
```cmd
    pytest --disable-warnings -q
```

## Cenário de teste

Login - `standard_user`/`secret_sauce`, validação de redirecionamento para o inventory.html
Adicionar ao Carrinho - Inclui dois produtos diferentes, valida o redirecionamento para cart.html
Remover do Carrinho o item[0]
Checkout preenchendo o first-name, last-name e postal-code valida redirecionamento para checkout-step-two.html
Finaliza a Compra clicando em Finish e verifica checkout-complete.html
Confirmação com a msg na tela de "Thank you for your order"