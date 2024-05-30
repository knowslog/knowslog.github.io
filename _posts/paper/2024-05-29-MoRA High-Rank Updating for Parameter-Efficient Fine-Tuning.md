---
title: MoRA High-Rank Updating for Parameter-Efficient Fine-Tuning
date: 2024-05-29
category: paper
layout: post
mermaid: true
---
출처 : [MoRA: High-Rank Updating for Parameter-Efficient Fine-Tuning-Ting Jiang, Shaohan Huang, Shengyue Luo, Zihan Zhang, Haizhen Huang, Furu Wei, Weiwei Deng, Feng Sun, Qi Zhang, Deqing Wang, Fuzhen Zhuang](https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css)

# TL;DR
- **MoRA**는 대형 언어 모델(LLM)의 파라미터 효율적 미세 조정을 위한 새로운 방법으로, 기존의 저랭크 업데이트 방식인 **LoRA**의 한계를 극복하고자 제안되었습니다. MoRA는 동일한 수의 학습 가능한 파라미터를 유지하면서 고랭크 업데이트를 달성하기 위해 정방 행렬을 사용합니다. 이를 통해 메모리 집약적인 작업에서 LoRA보다 우수한 성능을 보이며, 다른 작업에서도 유사한 성능을 유지합니다.

# 목차
- 1 Introduction
- 2 Related Work
  - 2.1 LoRA
  - 2.2 Fine-Tuning with LLMs
- 3 Analysis the Influence of Low-rank Updating
- 4 Method
- 5 Experiment
  - 5.1 Memorizing UUID Pairs
  - 5.2 Fine-tuning Tasks
    - 5.2.1 Setup
    - 5.2.2 Baselines and Implements
    - 5.2.3 Results and Analysis
  - 5.3 Pretraining
- 6 Analysis
  - 6.1 High-rank Updating
  - 6.2 Influence of Decompression and Compression
- 7 Conclusion
- References
- Appendix A Hyperparameters
- Appendix B Implementation of ReMoRA
- Appendix C Downstream Tasks of Continual Pretraining

# 1 Introduction
- **파라미터 효율적 미세 조정(PEFT)**은 대형 언어 모델(LLM)을 특정 다운스트림 작업에 적응시키기 위한 인기 있는 기술입니다.
- **LoRA**는 저랭크 행렬을 사용하여 파라미터를 업데이트함으로써 성능을 향상시킵니다.
- 그러나 저랭크 업데이트는 새로운 지식을 효과적으로 학습하고 기억하는 데 한계가 있습니다.
- 이를 해결하기 위해 **MoRA**는 정방 행렬을 사용하여 고랭크 업데이트를 달성합니다.

# 2 Related Work
## 2.1 LoRA
- **LoRA**는 저랭크 행렬을 사용하여 파라미터를 업데이트하는 PEFT 방법입니다.
- 저랭크 행렬을 사용함으로써 추가적인 추론 비용 없이 원래 모델 파라미터에 병합할 수 있습니다.
- 다양한 방법들이 LoRA를 개선하려고 시도했지만, 대부분은 GLUE 벤치마크를 기반으로 효율성을 검증합니다.

## 2.2 Fine-Tuning with LLMs
- **미세 조정**은 LLM의 성능을 향상시키기 위해 필요한 경우가 많습니다.
- 미세 조정은 크게 세 가지 유형으로 나눌 수 있습니다: 지시 조정, 복잡한 추론 작업, 지속적 사전 학습.
- LoRA와 그 변형들은 주로 지시 조정이나 텍스트 분류 작업을 통해 효율성을 검증합니다.

# 3 Analysis the Influence of Low-rank Updating
- **LoRA**는 저랭크 업데이트를 사용하여 FFT의 풀랭크 업데이트를 추정합니다.
- 저랭크 업데이트는 메모리 집약적인 작업에서 새로운 지식을 기억하는 데 어려움을 겪습니다.
- 이를 검증하기 위해 UUID 쌍을 기억하는 작업을 수행했습니다.
- **LoRA**는 FFT에 비해 성능이 떨어지며, 랭크를 증가시켜도 여전히 성능 차이가 존재합니다.

# 4 Method
- **MoRA**는 동일한 수의 학습 가능한 파라미터를 유지하면서 고랭크 업데이트를 달성하기 위해 정방 행렬을 사용합니다.
- 입력 차원을 줄이고 출력 차원을 늘리기 위해 비파라미터 연산자를 도입합니다.
- 이러한 연산자와 정방 행렬은 ΔW로 변환될 수 있어, LoRA처럼 LLM에 병합할 수 있습니다.

# 5 Experiment
## 5.1 Memorizing UUID Pairs
- **MoRA**는 동일한 수의 학습 가능한 파라미터를 사용하여 LoRA보다 우수한 성능을 보입니다.
- MoRA는 FFT와 유사한 성능을 달성하며, 500 스텝 내에 모든 UUID 쌍을 기억할 수 있습니다.

## 5.2 Fine-tuning Tasks
### 5.2.1 Setup
- 세 가지 미세 조정 작업(지시 조정, 수학적 추론, 지속적 사전 학습)에서 MoRA와 LoRA를 평가합니다.
- 각 작업에 대해 고품질의 데이터셋을 선택하여 테스트합니다.

### 5.2.2 Baselines and Implements
- 다양한 LoRA 변형 방법과 MoRA를 랭크 8과 256에서 실험합니다.
- MoRA는 회전 연산자를 사용하여 압축 및 압축 해제를 구현합니다.

### 5.2.3 Results and Analysis
- MoRA는 지시 조정 및 수학적 추론에서 LoRA와 유사한 성능을 보입니다.
- 지속적 사전 학습에서는 MoRA가 LoRA보다 우수한 성능을 보입니다.

## 5.3 Pretraining
- **MoRA**는 사전 학습에서 LoRA와 ReLoRA보다 우수한 성능을 보입니다.
- 고랭크 업데이트의 이점을 통해 MoRA는 더 낮은 퍼플렉시티를 달성합니다.

# 6 Analysis
## 6.1 High-rank Updating
- **MoRA**와 **ReMoRA**는 LoRA와 ReLoRA보다 더 많은 유의미한 특이값을 보입니다.
- 이는 ΔW의 랭크를 증가시키는 데 효과적임을 나타냅니다.

## 6.2 Influence of Decompression and Compression
- 압축 및 압축 해제 함수의 영향을 탐구한 결과, 회전 방법이 가장 효율적임을 확인했습니다.

# 7 Conclusion
- **MoRA**는 저랭크 업데이트의 한계를 극복하고, 메모리 집약적인 작업에서 우수한 성능을 보입니다.
- 다양한 방법을 통해 압축 및 압축 해제 함수를 구현하여 MoRA의 성능을 최적화했습니다.
- MoRA는 지시 조정 및 수학적 추론에서 LoRA와 유사한 성능을 보이며, 지속적 사전 학습 및 메모리 작업에서 우수한 성능을 보입니다.