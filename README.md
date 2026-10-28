# Autodiagnóstico de Gestão para MEI (Python)

Programa de terminal para microempreendedores individuais avaliarem a gestão do negócio. As áreas avaliadas são adaptadas dos domínios de desempenho do PMBOK Guide (PMI). Cada diagnóstico gera uma pontuação geral, notas por área e dicas de ação para as áreas mais fracas.

## Como executar
1. Instale o Python 3.
2. Na pasta do projeto, rode: `python main.py`
3. Os dados ficam salvos em `diagnosticos.json`, criado automaticamente.

Para rodar online sem instalar nada: no GitHub, abra o repositório, clique em **Code > Codespaces > Create codespace** e, no terminal que abrir, digite `python main.py`.

## Etapas do guia e onde estão no código
| Etapa do guia | Como foi feita |
| --- | --- |
| 1. Estrutura e menu | `mostrar_menu()` e `main()`, com todas as opções e a saída |
| 2. Cadastro | `cadastrar_diagnostico()`, com dicionários em lista global `diagnosticos` (negócio, responsável, ano, notas, plano concluído) |
| 3. Consulta e busca | `listar_diagnosticos()` e `buscar_diagnostico()`, com mensagem quando nada é encontrado |
| 4. Empréstimos e devoluções | `alterar_plano()`: o campo `plano_concluido` muda entre "Não" e "Sim" |
| 5. Persistência em JSON | `carregar_dados()` ao iniciar e `salvar_dados()` a cada alteração |
| 6. Melhorias | Contadores, ordenação, remoção e relatório com dicas |
| 7. Organização | Nomes descritivos, funções reutilizáveis, comentários e validação de entradas |

## Aviso
Ferramenta educativa. Não substitui a orientação de um contador ou consultor.
