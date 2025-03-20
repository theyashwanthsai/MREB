import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def generate_plots():
    categories = ["coding", "logical", "ethics", "multimodal"]
    model_scores = {}
    
    if not os.path.exists("graphics"):
        os.makedirs("graphics")
    
    for category in categories:
        file_path = f"Results/{category}_results.json"
        with open(file_path, 'r') as f:
            data = json.load(f)
            for model_name, model_data in data['models'].items():
                if model_name not in model_scores:
                    model_scores[model_name] = {
                        "Coding Score": 0,
                        "Logical Score": 0,
                        "Ethics Score": 0,
                        "Multimodal Score": 0
                    }
                category_key = f"{category.title()} Score"
                model_scores[model_name][category_key] = model_data["accuracy"]


    for model in model_scores.values():
        total = sum(model.values())
        model["Overall Score"] = round(total / 4, 2)


    df = pd.DataFrame(model_scores).T.reset_index().rename(columns={'index': 'Model Name'})
    df = df.sort_values(by='Overall Score', ascending=False)

    # 1. Horizontal Bar Chart
    fig1 = px.bar(
        df,
        x='Overall Score',
        y='Model Name',
        orientation='h',
        title='Model Overall Performance Comparison',
        text='Overall Score',
        color_discrete_sequence=['#FF6969']
    )

    # Todo: Think of better colors
    fig1.update_layout(
        plot_bgcolor='#272829',
        paper_bgcolor='#272829',
        font_color='#F1F1F1',
        xaxis=dict(
            titlefont_color='#F1F1F1',
            tickfont_color='#F1F1F1',
            showgrid=False  
        ),
        yaxis=dict(
            titlefont_color='#F1F1F1',
            tickfont_color='#F1F1F1'
        ),
        margin=dict(l=150, r=20, t=50, b=20) 
    )

    fig1.update_traces(
        marker_line_color='#61677A',
        marker_line_width=1.5,
        texttemplate='%{text:.1f}%',
        textposition='outside',
        textfont=dict(color='#F1F1F1')
    )

    # fig1.show()
    fig1.write_image("graphics/1.png", scale=2)


    # 2 Grouped Bar Chart
    category_columns = [col for col in df.columns if 'Score' in col and col != 'Overall Score']
    df_melted = df.melt(
        id_vars=['Model Name'],
        value_vars=category_columns,
        var_name='Category',
        value_name='Score'
    )

    fig2 = px.bar(
        df_melted,
        x='Model Name',
        y='Score',
        color='Category',
        barmode='group',
        title='Model Performance by Category',
        text='Score',
        color_discrete_sequence=['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FF8000', '#00FFCC', '#FF1493', '#7FFFD4']
    )

    fig2.update_layout(
        plot_bgcolor='#272829',
        paper_bgcolor='#272829',
        font_color='#F1F1F1',
        xaxis=dict(
            titlefont_color='#F1F1F1',
            tickfont_color='#F1F1F1',
            showgrid=False
        ),
        yaxis=dict(
            titlefont_color='#F1F1F1',
            tickfont_color='#F1F1F1',
            title='Score (%)'
        ),
        legend=dict(
            title=None,
            font_color='#F1F1F1'
        ),
        margin=dict(l=50, r=20, t=50, b=50)
    )

    fig2.update_traces(
        marker_line_color='#F1F1F1',
        marker_line_width=1,
        texttemplate='%{text:.1f}%',
        textposition='inside',
        textfont=dict(color='#F1F1F1')
    )

    fig2.write_image("graphics/2.png", scale=2)

    # 3. Spider Plot models
    category_columns = ['Coding Score', 'Logical Score', 'Ethics Score', 'Multimodal Score']
    categories_clean = [cat.replace(' Score', '') for cat in category_columns]
    
    fig3 = go.Figure()
    
    colors = ['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FF8000', '#00FFCC', '#FF1493', '#7FFFD4']
    
    for i, model in enumerate(df['Model Name']):
        model_data = df[df['Model Name'] == model][category_columns].values[0]
        
        fig3.add_trace(go.Scatterpolar(
            r=model_data,
            theta=categories_clean,
            fill='toself',
            name=model,
            line_color=colors[i % len(colors)],
            fillcolor=colors[i % len(colors)],
            opacity=0.6
        ))

    fig3.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont_color='#F1F1F1',
                gridcolor='#444444'
            ),
            angularaxis=dict(
                tickfont_color='#F1F1F1',
                gridcolor='#444444'
            ),
            bgcolor='#272829'
        ),
        title='Model Performance Radar Chart',
        font_color='#F1F1F1',
        paper_bgcolor='#272829',
        plot_bgcolor='#272829',
        legend=dict(
            font_color='#F1F1F1',
            bgcolor='#333333',
            bordercolor='#F1F1F1'
        )
    )
    
    fig3.write_image("graphics/3.png", scale=2)

generate_plots()