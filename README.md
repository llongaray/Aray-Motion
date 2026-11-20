# Aray Motion

Controle por gestos e visão computacional para Windows e Android.

> Estado: base inicial de desenvolvimento. A aplicação Windows possui captura de webcam, landmarks e detecção básica de pinça. A base Android ainda não executa comandos globais nem fornece APK compilado.

## Arquitetura

- `desktop/`: aplicativo Windows (Python, PySide6, OpenCV e MediaPipe).
- `core/`: reconhecimento de gestos a partir de landmarks normalizados.
- `android/`: projeto Android nativo (Kotlin, CameraX/MediaPipe previstos).
- `tests/`: testes independentes de hardware.
- `.github/workflows/`: integração contínua e pacote Windows.

## Windows

Requer Python 3.11 e Windows 10/11 x64:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-windows.txt
python -m desktop.app
```

O primeiro uso necessita que os modelos sejam fornecidos em `desktop/models/` conforme [instruções dos modelos](desktop/models/README.md). Não há download automático de modelos. O aplicativo não ativa controle de mouse por padrão.

## Testes

```powershell
pip install pytest
python -m pytest -q
```

## Releases

O workflow Windows empacota os fontes e dependências em `dist/ArayMotion/`, gera um ZIP executável e publica um artefato do Actions. O APK ainda depende da implementação nativa Android e da configuração da assinatura para distribuição. Não são publicadas releases automaticamente nesta etapa.

## Segurança

- Vídeo processado localmente.
- Sem upload ou gravação de imagens.
- Ativação explícita antes de qualquer comando de entrada no sistema.
- Ações Android devem respeitar as permissões e restrições do AccessibilityService e da câmera em segundo plano.

## Licença

Consulte `LICENSE`.
