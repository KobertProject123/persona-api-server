import os
import json

input_folder = "TL학교,학업"
output_path = os.path.join(input_folder, "conversation_list.json")

conversation_list = []

for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(input_folder, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                conv_id = data["info"]["id"]
                category = data["info"]["topic"]

                # persona 목록에서 profile_minor 추출
                persona_entries = []
                for persona in data["info"].get("personas", []):
                    persona_id = persona["persona_id"]
                    profile_minors = [
                        p["profile_minor"] for p in persona["persona"]
                        if p["profile_minor"] is not None
                    ]
                    persona_entries.append({
                        "persona_id": persona_id,
                        "profile_minors": profile_minors
                    })

                conversation_list.append({
                    "conversation_id": conv_id,
                    "category_id": category,
                    "personas": persona_entries
                })

        except Exception as e:
            print(f"❌ {filename} 처리 중 오류 발생: {e}")

# 저장
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(conversation_list, f, ensure_ascii=False, indent=2)

print(f"✅ 총 {len(conversation_list)}개의 conversation 항목 저장 완료!")
print(f"📁 저장 위치: {output_path}")
