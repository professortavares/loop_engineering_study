---
name: resumo-vendas
description: Como montar um resumo de vendas de um período, com total por produto e o produto mais vendido. Use quando a tarefa pedir relatório, resumo ou ranking de vendas.
---

# Resumo de vendas

Siga estes passos, nesta ordem:

1. Consulte as vendas de cada mês do período com `consultar_vendas`. Não pule nenhum mês.
2. Para cada produto, some as quantidades dos meses com `calcular`. Use uma expressão com os valores, por exemplo `120 + 135 + 150`.
3. Identifique o produto com a maior soma total.
4. Monte a resposta com:
   - uma tabela com produto e total do período;
   - uma linha dizendo qual produto mais vendeu e quantas unidades;
   - os valores mensais usados, para o leitor conferir.

Não invente números. Se algum mês não for encontrado, diga qual e não calcule o total com ele.
