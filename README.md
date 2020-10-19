# Aplicação de Cloud Gaming

## Estrutura de Diretórios
- `CentralServer/`
  - Servidor que gerencia as sessões de jogo
- `GamingInstance/`
  - Cliente que é responsável por transmitir as imagens do jogo para o Servidor Central
- `App/`
  - Frontend e Backend da aplicação web

## Guidelines

### Gitflow

Para adicionar uma nova funcionalidade a aplicação, crie uma branch a partir da branch `dev`. Quando a funcionalidade estiver pronta, submeta um pull request para a branch `dev`.

> Não altere a branch `dev` diretamente em hipótese alguma
