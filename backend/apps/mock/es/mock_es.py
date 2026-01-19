import json
from pathlib import Path

# ======================
# 基础路径配置
# ======================
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
MOCK_DIR = PROJECT_ROOT / "mock/es"
MOCK_INDICES = MOCK_DIR / "mock_es_indices.json"
MOCK_MAPPING = MOCK_DIR / "mock_es_mapping.jsonl"


# ======================
# 加载 mock 索引列表
# ======================
def get_mock_indices():
    """
    模拟 es_client.cat.indices 返回值
    生产环境无 monitor / indices 权限
    """
    with open(MOCK_INDICES, "r", encoding="utf-8") as f:
        return json.load(f)


# ======================
# 预加载 mapping（jsonl）
# ======================
def _load_mock_mappings() -> dict:
    """
    将 jsonl 格式的 mapping 文件加载为 dict:
    {
        index_name: {
            index_name: {
                "mappings": {...}
            }
        }
    }
    """
    mappings = {}

    with open(MOCK_MAPPING, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            data = json.loads(line)
            for index_name, mapping in data.items():
                mappings[index_name] = {
                    index_name: mapping
                }

    return mappings


# ======================
# 获取指定 index 的 mapping
# ======================
def get_mock_mapping(table_name: str):
    mappings = _load_mock_mappings()
    try:
        return mappings[table_name]
    except KeyError:
        raise ValueError(f"Unknown table: {table_name}")

# ======================
# main 测试入口
# ======================
def main():
    print("=" * 60)
    print("1. 测试 get_mock_indices()")
    print("=" * 60)

    indices = get_mock_indices()
    print(f"索引数量: {len(indices)}")

    for idx in indices:
        print(f"- {idx['index']}")

    print("\n" + "=" * 60)
    print("2. 测试 get_mock_mapping()")
    print("=" * 60)

    # 选取第一个索引做 mapping 测试
    test_index = indices[0]["index"]
    print(f"测试索引: {test_index}")

    mapping = get_mock_mapping(test_index)

    # 只打印关键信息，避免输出过长
    meta = mapping[test_index]["mappings"].get("_meta", {})
    properties = mapping[test_index]["mappings"].get("properties", {})

    print("描述信息:", meta.get("description"))
    print("字段数量:", len(properties))
    print("字段列表:")
    for field, spec in properties.items():
        print(f"  - {field}: {spec['type']}")

    print("\n" + "=" * 60)
    print("3. 测试非法 index")
    print("=" * 60)

    try:
        get_mock_mapping("not_exists_index")
    except ValueError as e:
        print("捕获预期异常:", e)


if __name__ == "__main__":
    main()
