import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import random
import flet as ft
from flet.matplotlib_chart import MatplotlibChart


def get_weekly_data(two_hour_blocks=True):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    full_hours = list(range(6, 21))  # 6 to 20 inclusive

    if two_hour_blocks:
        hour_blocks = [(f"{h}–{h+2}", h, h+2) for h in range(6, 20, 2)]
    else:
        hour_blocks = [(f"{h}:00", h, h+1) for h in full_hours]

    data_by_day = {}
    for day in days:
        random.seed(hash(day) % 1000)
        if day in ['Saturday', 'Sunday']:
            raw_values = [random.randint(0, 10) for _ in full_hours]
        elif day == 'Friday':
            raw_values = [random.randint(4, 14) for _ in full_hours]
        else:
            raw_values = [random.randint(6, 18) for _ in full_hours]

        grouped = []
        for _, start, end in hour_blocks:
            values = raw_values[start - 6:end - 6]
            avg = sum(values) / len(values)
            grouped.append(round(avg, 1))

        data_by_day[day] = grouped

    return data_by_day, [label for label, _, _ in hour_blocks], days


def create_chart_figure(day, values, hour_labels):
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='white')
    bars = ax.bar(hour_labels, values, color="#5C6BC0", edgecolor='black', linewidth=0.5)
    ax.set_ylim(0, 18)
    ax.set_title(f"Occupancy on {day}", fontsize=14, fontweight='bold')
    ax.set_xlabel("Time Interval", fontsize=12)
    ax.set_ylabel("Number of People", fontsize=12)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.3, str(val), ha='center', va='bottom', fontsize=8)

    fig.tight_layout()
    return fig


def create_occupancy_card():
    data_by_day, hour_blocks, days = get_weekly_data()
    default_day = "Monday"

    chart_container = ft.Column()

    def update_chart(day):
        fig = create_chart_figure(day, data_by_day[day], hour_blocks)
        new_chart = MatplotlibChart(figure=fig)
        chart_container.controls.clear()
        chart_container.controls.append(new_chart)
        chart_container.update()

    dropdown = ft.Dropdown(
        label="Select day",
        options=[ft.dropdown.Option(day) for day in days],
        value=default_day,
        width=220,
        border_radius=8,
        filled=True,
        bgcolor=ft.Colors.WHITE,
        border_color=ft.Colors.INDIGO_200,
        label_style=ft.TextStyle(font_family="Trasandina", size=14),
        on_change=lambda e: update_chart(e.control.value)
    )

    card = ft.Card(
        width=350,
        shape=ft.RoundedRectangleBorder(radius=12),
        shadow_color=ft.Colors.GREY_100,
        content=ft.Container(
            padding=10,
            border_radius=12,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            bgcolor=ft.Colors.WHITE,
            content=ft.Column([
                ft.Text("Occupancy", size=22, weight=ft.FontWeight.BOLD, font_family="Trasandina"),
                dropdown,
                chart_container
            ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )

    return card, lambda: update_chart(default_day)


