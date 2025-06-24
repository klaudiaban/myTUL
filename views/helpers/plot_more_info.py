import matplotlib
matplotlib.use("Agg")

import random
from constants import *
from flet import Colors, Column, Dropdown, dropdown, Text, Card, RoundedRectangleBorder, Container, ClipBehavior, TextStyle, FontWeight, CrossAxisAlignment
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle, Ellipse
from datetime import datetime

def get_weekly_data(two_hour_blocks=True):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    full_hours = list(range(8, 21)) 

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

def create_chart_figure(day, values, hour_labels, current_hour=None):
    font_path = "assets/fonts/Trasandina.otf"

    fig, ax = plt.subplots(figsize=(6, 4), facecolor='white')

    colors = [TUL_RED if val > 12 else "#9EA5D4" for val in values]

    for i, (label, val, color) in enumerate(zip(hour_labels, values, colors)):
        # Shorten the rectangle height slightly to make room for the ellipse
        ax.add_patch(Rectangle((i - 0.4, 0), 0.8, val - 0.2, color=color, edgecolor='black', linewidth=0.5))
        
        # Add a larger ellipse to make the top more rounded
        ax.add_patch(Ellipse((i, val - 0.1), 0.8, 4, color=color, edgecolor='black', linewidth=0.5))


        # Draw arrow if current hour is within this block
        if current_hour is not None:
            start_hour = int(label.split("–")[0])
            end_hour = int(label.split("–")[1])
            if start_hour <= current_hour < end_hour:
                ax.annotate("↓", (i, val + 2), ha='center', va='bottom', fontsize=30)

    ax.set_xlim(-0.5, len(hour_labels) - 0.5)
    ax.set_ylim(0, 21)
    ax.set_xticks(range(len(hour_labels)))
    ax.set_xticklabels(hour_labels, fontproperties=fm.FontProperties(fname=font_path, size=17))

    ax.set_yticks([])
    ax.set_ylabel(None)
    ax.set_xlabel(None)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(False)

    ax.set_title(f"Occupancy on {day}", fontproperties=fm.FontProperties(fname=font_path, size=25))

    fig.tight_layout()
    return fig

def create_occupancy_card():
    data_by_day, hour_blocks, days = get_weekly_data()
    now = datetime.now()
    default_day = now.strftime("%A")
    current_hour = now.hour

    chart_container = Column()

    def update_chart(day):
        fig = create_chart_figure(day, data_by_day[day], hour_blocks, current_hour if day == default_day else None)
        new_chart = MatplotlibChart(figure=fig)
        chart_container.controls.clear()
        chart_container.controls.append(new_chart)
        chart_container.update()

    dropdown_options = [dropdown.Option(day) for day in days]

    days_dropdown = Dropdown(
        label="Select day",
        text_size=16,
        options=dropdown_options,
        value=default_day,
        width=220,
        label_style=TextStyle(font_family="Trasandina"),
        on_change=lambda e: update_chart(e.control.value)
    )

    card = Card(
        width=350,
        shape=RoundedRectangleBorder(radius=12),
        shadow_color=Colors.GREY_100,
        content=Container(
            padding=10,
            border_radius=12,
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            bgcolor=Colors.WHITE,
            content=Column([
                days_dropdown,
                chart_container
            ],
                spacing=12,
                horizontal_alignment=CrossAxisAlignment.CENTER
            )
        )
    )

    return card, lambda: update_chart(default_day)