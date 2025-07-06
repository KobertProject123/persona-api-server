from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
import json

app = FastAPI()

# CORS 설정 (프론트엔드 연결 시 필요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기본 경로 설정
DATA_ROOT = "data"
# CONV_LIST_PATH = os.path.join(BASE_DIR, "conversation_list.json")
# CATEGORY_PATH = "data/category_list"

@app.get("/api/category")
def get_categories():
    try:
        # 카테고리 목록은 data 폴더 내의 하위 디렉터리 이름으로 판단
        categories = sorted([
            name for name in os.listdir(DATA_ROOT)
            if os.path.isdir(os.path.join(DATA_ROOT, name))
        ])
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"카테고리 로딩 실패: {e}")
    
@app.get("/api/conversation")
def get_conversation_list_by_category(
    category_id: str = Query(...),
    #category_id는 conversation_list의 category_id
    index: int = Query(1, ge=1)
):
    try:
        category_dir = os.path.join(DATA_ROOT, category_id)
        conv_list_path = os.path.join(category_dir, "conversation_list.json")

        if not os.path.exists(conv_list_path):
            raise HTTPException(status_code=404, detail="conversation_list.json이 존재하지 않습니다.")

        with open(conv_list_path, "r", encoding="utf-8") as f:
            all_data = json.load(f)

        size = 10  
        #size 10 고정
        total = len(all_data)
        start = (index - 1) * size
        end = start + size
        paginated = all_data[start:end]

        return {
            "category_id": category_id,
            "index": index,
            "size": size,
            "total": total,
            "total_pages": (total + size - 1) // size,
            "items": paginated
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"대화 목록 조회 실패: {e}")

@app.get("/api/conversation/{conversation_id}")
def get_conversation(conversation_id: str):
    # conversation_id는 대화 json 파일 내 "info.id"와 동일해야 함
    try:
        # 모든 파일을 스캔하면서 해당 conversation_id를 가진 파일을 찾음
        for category in os.listdir(DATA_ROOT):
            category_dir = os.path.join(DATA_ROOT, category)
            if not os.path.isdir(category_dir):
                continue

            for fname in os.listdir(category_dir):
                if fname.endswith(".json") and fname != "conversation_list.json":
                    file_path = os.path.join(category_dir, fname)
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if data.get("info", {}).get("id") == conversation_id:
                            return {"utterances": data["utterances"]}
                        
        raise HTTPException(status_code=404, detail="해당 conversation_id를 가진 파일이 없음")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"대화 로딩 실패: {e}")
