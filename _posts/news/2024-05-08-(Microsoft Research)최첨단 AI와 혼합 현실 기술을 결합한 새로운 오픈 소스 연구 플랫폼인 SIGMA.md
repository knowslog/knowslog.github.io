---
title: (Microsoft Research)최첨단 AI와 혼합 현실 기술을 결합한 새로운 오픈 소스 연구 플랫폼인 SIGMA
date: 2024-05-08
category: news
layout: post
mermaid: true
---

출처 : [Microsoft AI Research Introduces SIGMA: An Open-Source Research Platform to Enable Research and Innovation at the Intersection of Mixed Reality and AI-Dhanshree Shripad Shenwai](https://www.marktechpost.com/2024/05/07/microsoft-ai-research-introduces-sigma-an-open-source-research-platform-to-enable-research-and-innovation-at-the-intersection-of-mixed-reality-and-ai/)

# TL;DR

Microsoft Research는 최첨단 AI와 혼합 현실 기술을 결합한 새로운 오픈 소스 연구 플랫폼인 SIGMA를 소개했습니다. SIGMA는 실제 세계에서 사람과 상호작용하는 AI 시스템을 구축하는 데 필요한 다중 모달 지각, 추론 및 생성 기능을 제공합니다. 또한 HoloLens 2를 사용하여 사용자에게 절차상 작업을 안내할 수 있으며, 대화형 질문에 대답할 수 있습니다. SIGMA는 혼합 현실과 AI의 교차점에서 새로운 연구와 혁신을 가능하게 하는 오픈 소스 연구 플랫폼입니다.

# 섹션

## SIGMA 개요

Microsoft Research는 최첨단 AI와 혼합 현실 기술을 결합한 새로운 오픈 소스 연구 플랫폼인 SIGMA를 공개했습니다. SIGMA는 실제 세계에서 사람과 원활하게 작업할 수 있는 AI 시스템을 구축하기 위해 필요한 물체 감지 및 추적을 넘어서는 다중 모달 지각, 추론 및 생성 기능을 제공합니다. 

## SIGMA의 주요 기능

SIGMA는 HoloLens 2를 활용하여 사용자에게 절차상 작업을 안내할 수 있습니다. GPT-4와 같은 대규모 언어 모델이나 작업 라이브러리의 수동으로 정의된 단계를 사용하여 동적으로 작업을 만들 수 있습니다. 또한 상호작용 중에 사용자가 개방형 질문을 할 때 SIGMA의 광범위한 언어 모델을 사용하여 답변할 수 있습니다. Detic 및 SEEM과 같은 비전 모델을 사용하여 사용자의 시야에서 작업 관련 개체를 찾아 강조 표시할 수도 있습니다.

## SIGMA의 구현 및 아키텍처

SIGMA는 HoloLens 2 디바이스에서 실행되는 경량 클라이언트 애플리케이션을 사용하는 클라이언트-서버 아키텍처로 구현됩니다. 클라이언트 앱은 RGB, 깊이, 오디오, 헤드, 손, 시선 추적 정보를 포함한 여러 다중 모달 데이터 스트림을 더 강력한 데스크탑 서버로 전송합니다. 데스크탑 서버는 애플리케이션의 핵심 기능을 실행하고 장치에서 콘텐츠를 표시하는 방법에 대한 데이터와 명령을 클라이언트 앱에 전달합니다. 

SIGMA는 Platform for Situated Intelligence(psi)라는 다중 모달 통합 AI 시스템을 개발하고 연구하기 위한 오픈 소스 아키텍처를 기반으로 합니다. psi 프레임워크에는 고성능 스트리밍 및 로깅 인프라, 신속한 프로토타이핑, 그리고 데이터 기반 애플리케이션 수준 개발 및 튜닝을 가능하게 하는 데이터 재생 인프라가 제공됩니다.

## 결론

SIGMA는 실제 세계에서 인간과 상호 작용하는 AI 시스템을 구축하는 데 필요한 기술과 기능을 제공하는 새로운 오픈 소스 연구 플랫폼입니다. Microsoft Research는 이 시스템을 공개적으로 사용할 수 있도록 함으로써 다른 연구원들이 혼합 현실과 AI 교차점에서 흥미로운 새로운 프런티어로 바로 나아갈 수 있기를 희망하고 있습니다.