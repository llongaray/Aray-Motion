<div align="center">

# Aray Motion

**Controle por gestos com visão computacional para Windows e Android**

Transforme movimentos das mãos em interações digitais — com foco em acessibilidade, privacidade e processamento local.

[![CI](https://github.com/llongaray/Aray-Motion/actions/workflows/ci.yml/badge.svg)](https://github.com/llongaray/Aray-Motion/actions/workflows/ci.yml)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D4?logo=windows)](#executando-no-windows)
[![Android](https://img.shields.io/badge/Android-planejado-3DDC84?logo=android)](#android)
[![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)](#status-do-projeto)

[Visão geral](#visão-geral) · [Funcionalidades](#funcionalidades) · [Instalação](#executando-no-windows) · [Roadmap](#roadmap) · [Contribuição](#contribuindo)

</div>

> [!IMPORTANT]
> **Projeto em desenvolvimento.** O protótipo Windows contém a interface de câmera e a integração inicial com os detectores MediaPipe, mas ainda precisa de validação em hardware. O controle efetivo do mouse não foi implementado. O Android ainda não possui aplicativo Gradle ou APK. Não existe release pronta para usuários finais.

## Visão geral

O **Aray Motion** é um projeto de interação sem toque (*touchless*) que utiliza a câmera do dispositivo para localizar mãos e rostos e, progressivamente, converter gestos intencionais em comandos de interface.

**Objetivo do produto:** movimentar o mouse, clicar, arrastar, rolar, abrir e fechar janelas e alternar abas no Windows; no Android, permitir toques, deslizamentos e navegação por meio de recursos de acessibilidade autorizados.

## Funcionalidades

| Recurso | Windows | Android |
| --- | --- | --- |
| Interface gráfica | Implementação inicial | Planejado |
| Seleção de câmera | Implementação inicial | Planejado |
| Visualização da câmera | Implementação inicial | Planejado |
| Landmarks de mãos (21 pontos) | Implementação inicial | Planejado |
| Landmarks faciais | Implementação inicial | Planejado |
| Interpretação de pinça | Núcleo implementado; sem comando de sistema | Planejado |
| Movimento do cursor e cliques | Planejado | Não aplicável |
| Toques e navegação do sistema | Não aplicável | Planejado |
| ZIP compilado | Workflow de prévia, não validado como release | Não aplicável |
| APK instalável | Não aplicável | Planejado |

A identificação anatômica completa das orelhas pode exigir um modelo adicional aos landmarks faciais convencionais.

## Demonstração

Capturas de tela e vídeos reais serão adicionados após a validação do protótipo. Nenhuma demonstração é apresentada como funcional antes dos testes.

## Tecnologias

| Camada | Tecnologias |
| --- | --- |
| Interface Windows | Python 3.11, PySide6 |
| Captura de vídeo | OpenCV |
| Visão computacional | MediaPipe Tasks |
| Motor de gestos | Python, landmarks normalizados |
| Android (planejado) | Kotlin, Jetpack Compose, CameraX |
| Controle Android (planejado) | AccessibilityService, com consentimento |
| Testes | pytest |
| CI e empacotamento | GitHub Actions, PyInstaller |

## Estrutura do repositório

```text
Aray-Motion/
├── .github/workflows/      # CI e build de prévia Windows
├── android/                # Planejamento do aplicativo Android
├── core/                   # Reconhecimento e confirmação de gestos
├── desktop/                # Interface, webcam e detecção visual
│   └── models/             # Instruções dos modelos MediaPipe
├── tests/                  # Testes unitários do core
├── requirements-windows.txt
├── requirements-dev.txt
├── LICENSE
└── README.md
```

## Executando no Windows

### Pré-requisitos

- Windows 10 ou 11, 64 bits;
- Python 3.11;
- Webcam integrada ou USB;
- Modelos oficiais compatíveis com MediaPipe Tasks.

### 1. Clonar o projeto

```powershell
git clone https://github.com/llongaray/Aray-Motion.git
cd Aray-Motion
```

> [!NOTE]
> Enquanto o pull request inicial não for integrado à `main`, selecione a branch `feat/initial-cross-platform-foundation` com `git switch feat/initial-cross-platform-foundation` após `git fetch origin`.

### 2. Criar o ambiente virtual

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-windows.txt
```

### 3. Adicionar os modelos

Obtenha os modelos `hand_landmarker.task` e `face_landmarker.task` de fontes oficiais e coloque-os em `desktop/models/`.

Consulte [instruções e fontes dos modelos](desktop/models/README.md). Os modelos não são baixados automaticamente.

### 4. Iniciar a aplicação

```powershell
python -m desktop.app
```

Selecione uma câmera, habilite os detectores desejados e clique em **Iniciar**. A aplicação exibirá a imagem com os pontos detectados, conforme compatibilidade do ambiente.

> [!WARNING]
> Esta versão **não controla o mouse nem a tela do dispositivo**. O processamento visual é experimental e requer testes com câmera real.

## Android

A implementação Android será nativa em Kotlin, utilizando CameraX, MediaPipe e, para ações globais autorizadas, `AccessibilityService`.

**Status atual:** apenas documentação de arquitetura em [android/README.md](android/README.md). Ainda não há APK nem projeto Gradle funcional.

O uso da câmera sobre outros aplicativos dependerá das permissões e restrições da versão do Android e do fabricante.

## Testes

Instale o pytest e execute os testes do núcleo de gestos:

```powershell
python -m pip install pytest
python -m pytest -q tests/
```

A execução automática está configurada no [GitHub Actions](https://github.com/llongaray/Aray-Motion/actions). A aprovação dos testes unitários não substitui a validação com webcam ou dispositivo físico.

## Roadmap

- [x] Estrutura inicial do repositório
- [x] Motor básico de interpretação de pinça
- [x] Testes unitários do motor de gestos
- [x] CI inicial no GitHub Actions
- [ ] Validar detecção de mãos e rosto em webcam Windows
- [ ] Implementar controle seguro de mouse, cliques e arraste
- [ ] Adicionar calibração, suavização e perfis de gestos
- [ ] Empacotar modelos e gerar ZIP Windows pronto para uso
- [ ] Criar aplicativo Android com CameraX e MediaPipe
- [ ] Implementar toques e navegação via acessibilidade
- [ ] Validar funcionamento em dispositivos Android reais
- [ ] Automatizar APK assinado e releases versionadas

Acompanhe o progresso em [Pull Requests](https://github.com/llongaray/Aray-Motion/pulls) e [Actions](https://github.com/llongaray/Aray-Motion/actions).

## Releases

A versão Windows possui um workflow de **prévia técnica**. O artefato atual não inclui automaticamente os modelos MediaPipe e não deve ser considerado um instalador final.

As futuras releases deverão disponibilizar:

- `ArayMotion-Windows-x64-vX.Y.Z.zip`;
- `ArayMotion-Android-vX.Y.Z.apk`;
- `SHA256SUMS.txt`;
- Notas de versão e instruções de instalação.

Consulte a página de [Releases](https://github.com/llongaray/Aray-Motion/releases) para verificar os arquivos efetivamente publicados.

## Segurança e privacidade

- Processamento local de vídeo, sem upload de imagens na implementação inicial.
- Sem gravação automática das imagens da câmera.
- Comandos do sistema somente após ativação explícita.
- Confirmação temporal para reduzir acionamentos involuntários.
- Botão de interrupção e permissões mínimas previstos para as próximas fases.
- No Android, o serviço de acessibilidade deve ser habilitado pelo usuário e respeitar as restrições do sistema.

## Contribuindo

Contribuições, relatos de erros e sugestões são bem-vindos:

1. Abra uma [issue](https://github.com/llongaray/Aray-Motion/issues) descrevendo o problema ou proposta.
2. Crie uma branch específica para a alteração.
3. Inclua testes quando aplicável.
4. Abra um pull request explicando as mudanças e como validá-las.

Evite incluir gravações de câmera com dados pessoais, credenciais, chaves de assinatura ou arquivos locais de configuração.

## Licença

Este projeto está disponibilizado conforme os termos do arquivo [LICENSE](LICENSE).

---

<div align="center">

Desenvolvido como projeto **Aray Motion**.

[Voltar ao topo](#aray-motion)

</div>
