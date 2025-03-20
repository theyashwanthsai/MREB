import json

def create_leaderboard():
    categories = ["coding", "logical", "ethics", "multimodal"]
    model_scores = {}

    for category in categories:
        file_path = f"Results/{category}_results.json"

        with open(file_path, 'r') as f:
            data = json.load(f)

            for model_name, model_data in data['models'].items():
                if model_name not in model_scores:
                    model_scores[model_name] = {"Coding Score": 0,
                                               "Logical Score": 0,
                                               "Ethics Score": 0,
                                               "Multimodal Score": 0}

                category_key = category.title() + " Score"
                model_scores[model_name][category_key] = model_data["accuracy"]

    for model in model_scores.values():
        total = sum(model.values())
        model["Overall Score"] = round(total / 4, 2)

    sorted_models = sorted(
        model_scores.items(),
        key=lambda x: x[1]["Overall Score"],
        reverse=True
    )

    header = ["Model Name", "Coding Score", "Logical Score", "Ethics Score", "Multimodal Score", "Overall Score"]
    separator = ["---" for _ in header]


    table_rows = []
    for model_name, scores in sorted_models:
        row = [
            model_name,
            scores["Coding Score"],
            scores["Logical Score"],
            scores["Ethics Score"],
            scores["Multimodal Score"],
            scores["Overall Score"]
        ]
        table_rows.append(row)

    table = []
    table.append(" | ".join(header))
    table.append(" | ".join(separator))
    for row in table_rows:
        formatted_row = [str(item) for item in row]
        table.append(" | ".join(formatted_row))

    return "\n".join(table)

leaderboard_table = create_leaderboard()
with open("leaderboard.md", "w") as f:
    f.write(leaderboard_table)
print("Leaderboard saved to leaderboard.md")