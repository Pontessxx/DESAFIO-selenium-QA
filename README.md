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
ou 
```cmd
    pytest --disable-warnings --capture=no
```

## Cenário de teste
### standart_user
</br>Login - `standard_user`/`secret_sauce`, validação de redirecionamento para o inventory.html
</br>Adicionar ao Carrinho - Inclui dois produtos diferentes, valida o redirecionamento para cart.html
</br>Remover do Carrinho o item[0]
</br>Checkout preenchendo o first-name, last-name e postal-code valida redirecionamento para checkout-step-two.html
</br>Finaliza a Compra clicando em Finish e verifica checkout-complete.html
</br>Confirmação com a msg na tela de "Thank you for your order"

### locked_out_user
</br>O usuario não entra e aparece a msg "Epic sadface: Sorry, this user has been locked out."

### problem_user
O SauceDemo não “quebra” de fato as imagens para o problem_user (naturalWidth==0), mas troca as imagens de produto – ou seja, elas carregam, só não correspondem ao nome. Por isso o seu broken_imgs ficou vazio.
eu irei manter o `@pytest.mark.xfail`pois é um bug conhecido e não me gera no cmd o FAILURE, assim quando for de fato corrigido eu irei receber um XPASS.
Caso for um corpotamento esperado, pois isso sempre está acontecendo com esse usuario entao transformaria para um teste normal

### performance_glitch_user
