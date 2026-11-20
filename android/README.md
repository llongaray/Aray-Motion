# Android — Aray Motion

O aplicativo Android será desenvolvido nativamente com Kotlin, Jetpack Compose, CameraX e MediaPipe Tasks.

## Escopo do adaptador

1. Captura de câmera frontal/traseira e permissão `CAMERA`.
2. Visualização de landmarks e detecção de gestos.
3. `AccessibilityService` explicitamente habilitado pelo usuário, com `dispatchGesture()` para toques e deslizamentos.
4. Ações globais (voltar, tela inicial e aplicativos recentes) apenas após ativação.
5. Serviço em primeiro plano e indicador visível, obedecendo às restrições Android vigentes.
6. Botão de emergência para desativar ações.

Esta pasta é uma reserva de arquitetura: **ainda não há projeto Gradle ou APK funcional**. O suporte a captura em segundo plano deve ser validado em hardware real. Não usar serviços de acessibilidade para ocultar ações, burlar proteções ou coletar dados de outros aplicativos.
