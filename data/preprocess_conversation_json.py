import json

input_path = "02.라벨링데이터/1-014-044_sample(페르소나대화).json"
output_path = "02.라벨링데이터/BP22000905_processed.json"

# JSON 파일 로드 
with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# conversation_id 추출
conversation_id = data["info"]["id"]
utterances = data["utterances"]

# 전처리된 데이터 구조
processed = {
    "conversation_id": conversation_id,
    "utterances": [
        {
            "utterance_id": u["utterance_id"],
            "persona_id": u["persona_id"],
            "text": u["text"],
            "terminate": u["terminate"]
        } for u in utterances
    ]
}

# JSON 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(processed, f, ensure_ascii=False, indent=2)

print(f"전처리 완료! 저장 위치: {output_path}")
