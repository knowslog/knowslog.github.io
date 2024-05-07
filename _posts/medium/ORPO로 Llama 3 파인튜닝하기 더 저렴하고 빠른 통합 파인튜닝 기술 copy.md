---
title: ORPO로 Llama 3 파인튜닝하기: 더 저렴하고 빠른 통합 파인튜닝 기술
date: 2024-05-07
category: medium
layout: post
mermaid: true
---

출처 : [Fine-tune Llama 3 with ORPO. A cheaper and faster unified… - Maxime Labonne](https://medium.com/towards-data-science/fine-tune-llama-3-with-orpo-56cfab2f9ada)

# TL;DR

- ORPO는 기존의 지도 학습 파인튜닝(SFT)과 선호도 정렬(rlhf/dpo)을 하나로 통합한 기술임  
- SFT만으로는 원치 않는 결과에 대한 확률도 높아지므로, 선호도 정렬이 추가로 필요했음
- ORPO는 odds ratio(OR) 항을 추가해 원치않는 결과는 약하게, 원하는 결과는 강하게 페널티/보상을 줌
- TRL 라이브러리를 활용해 Llama 3 8B 모델을 ORPO로 파인튜닝 할 수 있음
- 짧은 학습에도 ORPO로 파인튜닝한 모델이 여러 벤치마크에서 기본 모델보다 우수한 성능을 보임

## 목차

- ORPO 소개 
- ORPO로 Llama 3 8B 파인튜닝하기
- 결론

# ORPO 소개

ORPO(Odds Ratio Preference Optimization)는 Hong과 Lee가 2024년에 발표한 새로운 파인튜닝 기술이다. 기존에는 LLM을 특정 태스크에 적용하기 위해 다음과 같은 2단계 프로세스를 거쳤다.

1. 지도 학습 파인튜닝(Supervised Fine-Tuning, SFT): 원하는 도메인의 명령/출력 데이터로 모델을 학습
2. 선호도 정렬(Preference Alignment): RLHF나 DPO 등으로 모델이 선호하는 출력에 높은 확률을 부여하도록 조정

그러나 SFT만으로는 모델이 원하는 도메인에 적응되는 동시에 원치 않는 출력에 대한 확률도 높아지는 문제가 있었다. 이 때문에 선호하는 출력과 그렇지 않은 출력 간의 격차를 벌리기 위한 선호도 정렬 단계가 필요했다.   

ORPO는 이런 2단계 프로세스를 하나로 통합했다. 손실 함수에 odds ratio(OR) 항을 추가해, 원치 않는 출력은 약하게 페널티를 주고 원하는 출력은 강하게 보상한다. 이를 통해 모델이 타겟 태스크를 학습함과 동시에 인간의 선호도에 부합하도록 정렬된다.

ORPO는 TRL, Axolotl, LLaMA-Factory 등 주요 파인튜닝 라이브러리에서 지원하고 있다.

# ORPO로 Llama 3 8B 파인튜닝하기

Meta에서 최근 공개한 Llama 3은 15조 토큰으로 학습된 LLM이다. 70B와 8B 버전이 공개되었는데, 70B 모델은 MMLU 82점, HumanEval 81.7점으로 우수한 성능을 보였다. 8B 모델도 컨텍스트 길이가 8,192토큰으로 늘어나고, 새로운 토크나이저로 15% 정도 토큰 수가 감소했다.

ORPO를 사용하려면 프롬프트, 선호하는 응답, 선호하지 않는 응답으로 구성된 데이터셋이 필요하다. 여기서는 DPO 데이터셋을 모은 `mlabonne/orpo-dpo-mix-40k`를 사용할 것이다.

먼저 필요한 라이브러리를 설치한다:

```bash
pip install -U transformers datasets accelerate peft trl bitsandbytes wandb  
```

그 다음 라이브러리를 임포트하고, bitsandbytes를 사용해 Llama 3 8B 모델을 4비트 정밀도로 로드한다. LoRA 설정은 PEFT의 QLoRA를 활용한다. 또한 `setup_chat_format()` 함수로 모델과 토크나이저에 ChatML 포맷을 적용한다.  

```python
...

# QLoRA config 
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch_dtype,
    bnb_4bit_use_double_quant=True,  
)

# LoRA config
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,  
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM", 
    target_modules=['up_proj', 'down_proj', 'gate_proj', 'k_proj', 'q_proj', 'v_proj', 'o_proj']
)

# 모델 로드  
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=bnb_config,
    device_map="auto",
    attn_implementation=attn_implementation  
)
model, tokenizer = setup_chat_format(model, tokenizer)
model = prepare_model_for_kbit_training(model)
```

이제 `mlabonne/orpo-dpo-mix-40k` 데이터셋을 로드하고, `apply_chat_template()` 함수로 chosen과 rejected 열을 ChatML 포맷으로 변환한다. 

```python
dataset_name = "mlabonne/orpo-dpo-mix-40k"
dataset = load_dataset(dataset_name, split="all")
dataset = dataset.shuffle(seed=42).select(range(1000))

def format_chat_template(row):
    row["chosen"] = tokenizer.apply_chat_template(row["chosen"], tokenize=False)  
    row["rejected"] = tokenizer.apply_chat_template(row["rejected"], tokenize=False)
    return row

dataset = dataset.map(
    format_chat_template, 
    num_proc= os.cpu_count(),
)
dataset = dataset.train_test_split(test_size=0.01)
```

이제 ORPOTrainer로 모델을 학습시킬 수 있다.

```python
orpo_args = ORPOConfig(
    learning_rate=8e-6,
    beta=0.1,
    lr_scheduler_type="linear",
    max_length=1024,
    max_prompt_length=512,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,  
    gradient_accumulation_steps=4,
    optim="paged_adamw_8bit",
    num_train_epochs=1,
    evaluation_strategy="steps",
    eval_steps=0.2,
    logging_steps=1,
    warmup_steps=10, 
    report_to="wandb",
    output_dir="./results/",
)

trainer = ORPOTrainer(
    model=model, 
    args=orpo_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    peft_config=peft_config,
    tokenizer=tokenizer,  
)

trainer.train()  
trainer.save_model(new_model)
```

1,000개 샘플로 약 2시간 정도 학습했다. W&B 그래프를 보면 손실은 감소하지만 chosen과 rejected 간 차이는 크지 않다. 논문에서는 16만개 샘플로 10 에포크 학습한 것에 비하면 턱없이 부족한 셈이다. 

마지막으로 QLoRA 어댑터를 베이스 모델과 병합하고, 허깅페이스 허브에 푸시한다.

```python
...

# 메모리 비우기
del trainer, model  
gc.collect()
torch.cuda.empty_cache()

# 토크나이저와 모델 다시 로드  
tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForCausalLM.from_pretrained( 
    base_model,
    low_cpu_mem_usage=True,
    return_dict=True,
    torch_dtype=torch.float16,
    device_map="auto",
)
model, tokenizer = setup_chat_format(model, tokenizer)

# 어댑터와 베이스 모델 병합
model = PeftModel.from_pretrained(model, new_model)
model = model.merge_and_unload()
model.push_to_hub(new_model, use_temp_dir=False) 
tokenizer.push_to_hub(new_model, use_temp_dir=False)
```

이로써 Llama 3 8B 모델을 ORPO로 파인튜닝 하는 과정을 마쳤다. 학습이 충분치 않았음에도 Nous의 벤치마크에서 기본 모델보다 나은 성능을 보였다. 전체 4만개 샘플로 학습한다면 더 좋은 결과를 얻을 수 있을 것이다. 

# 결론

이 글에서는 ORPO 알고리즘을 소개하고, 기존의 SFT와 선호도 정렬을 하나로 통합하는 원리를 설명했다. 그리고 TRL을 사용해 Llama 3 8B 모델을 커스텀 데이터셋으로 파인튜닝 하는 과정을 살펴봤다. 

최종 모델은 학습량이 적었음에도 고무적인 결과를 보여줬고, ORPO가 새로운 파인튜닝 패러다임으로서의 잠재력을 보여줬다. 앞으로 고품질 데이터셋을 만드는 방법 등을 다루는 후속 글도 준비할 예정이다.