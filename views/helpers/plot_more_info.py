from flet import (
    Dropdown, DropdownOption, BarChart, BarChartGroup, BarChartRod,
    ChartAxis, ChartAxisLabel, Text, Colors, Column, Container, padding, border_radius
)
import random


def get_weekly_data(two_hour_blocks=True):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    full_hours = list(range(6, 21))  # 6 to 20 inclusive

    # Use compact labels like "6–8" instead of "6:00 - 8:00"
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
            values = raw_values[start - 6:end - 6]  # align index to 0
            avg = sum(values) / len(values)
            grouped.append(round(avg, 1))

        data_by_day[day] = grouped

    return data_by_day, [label for label, _, _ in hour_blocks], days


def plot_slay():
    data_by_day, hour_blocks, days = get_weekly_data(two_hour_blocks=True)

    chart = BarChart(
        left_axis=ChartAxis(
            title=Text("Number of People", size=12),
            labels_size=30,
        ),
        bottom_axis=ChartAxis(
            title=Text("Time Interval", size=12),
            labels=[
                ChartAxisLabel(value=i, label=Text(hour_blocks[i], size=10))
                for i in range(len(hour_blocks))
            ],
            labels_size=50,
        ),
        tooltip_bgcolor=Colors.with_opacity(0.9, Colors.INDIGO_200),
        max_y=18,
        interactive=True,
        expand=True,
    )

    def update_chart(day):
        chart.bar_groups = [
            BarChartGroup(
                x=i,
                bar_rods=[
                    BarChartRod(
                        to_y=data_by_day[day][i],
                        tooltip=f"{day} {hour_blocks[i]}: {data_by_day[day][i]} people",
                        color=Colors.INDIGO_400,
                        width=16  
                    )
                ]
            )
            for i in range(len(hour_blocks))
        ]
        chart.update()

    dropdown = Dropdown(
        label="Select day",
        options=[DropdownOption(day) for day in days],
        value="Monday",
        width=220,
        border_radius=8,
        text_size=14
    )

    dropdown.on_change = lambda e: update_chart(dropdown.value)

    content = Column([
        Text("Occupancy in 2-hour intervals", size=20, weight="bold", color=Colors.BLACK87),
        dropdown,
        chart
    ],
        spacing=15,
        horizontal_alignment="center"
    )

    ui = Container(
        content=content,
        bgcolor=Colors.GREY_100,
        padding=padding.all(20),
        border_radius=border_radius.all(12)
    )

    return ui, update_chart, dropdown.value
