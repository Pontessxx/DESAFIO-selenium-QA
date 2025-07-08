# 🚀 SauceDemo Test Automation
!(banner)[https://github.com/Pontessxx/DESAFIO-selenium-QA/blob/main/assets/image.png]

Automação de ponta a ponta dos principais fluxos do site [SauceDemo](https://www.saucedemo.com/) usando Python + Selenium. Este repositório contém um único teste que cobre login, carrinho, checkout e confirmação de pedido.

## 🛠️ Tecnologias e Dependências (Versões)

- **Python** = 3.12.6 
- **Selenium** = 4.34.1
- **pytest** = 8.4.1
- **webdriver-manager** = 4.0.2

# Como executar os testes

Você pode rodar com :
```cmd
    python tests/test_saucedemo.py
```
ou
```cmd
    pytest --disable-warnings -q
```

## Cenário de teste

Login - `standard_user`/`secret_sauce`, validação de redirecionamento para o inventory.html