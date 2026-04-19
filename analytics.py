import os

try:
    import matplotlib
    matplotlib.use("Agg")         
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_charts")


def _ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def _pause():
    input("\n  Press Enter to continue...")


#  1. GRADE TRENDS BAR CHART

def plot_grade_trends(students_map):
    students = list(students_map.values())
    if not students:
        print("  No student data.")
        return

    # Collect all subjects
    all_subjects = set()
    for s in students:
        all_subjects.update(s.grades.keys())
    subjects = sorted(all_subjects)

    names = [s.full_name for s in students]
    x = np.arange(len(names))
    width = 0.15
    n_subjects = len(subjects)
    colors = plt.cm.Set2(np.linspace(0, 1, n_subjects))

    fig, ax = plt.subplots(figsize=(12, 6))
    for i, subj in enumerate(subjects):
        marks = [s.grades.get(subj, 0) for s in students]
        offset = (i - n_subjects / 2) * width + width / 2
        bars = ax.bar(x + offset, marks, width, label=subj, color=colors[i], edgecolor="white")
        for bar, mark in zip(bars, marks):
            if mark > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                        str(mark), ha='center', va='bottom', fontsize=7)

    ax.set_xlabel("Students", fontsize=12)
    ax.set_ylabel("Marks", fontsize=12)
    ax.set_title("Grade Trends by Subject", fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=15, ha='right')
    ax.set_ylim(0, 115)
    ax.axhline(60, color='red', linestyle='--', alpha=0.4, label='Pass Threshold (60)')
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "grade_trends.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  [+] Chart saved: {path}")


#  2. ECA IMPACT SCATTER PLOT

def plot_eca_impact(students_map):
    students = [s for s in students_map.values() if s.grades]
    if not students:
        print("  No grade data available.")
        return

    eca_counts = [len(s.eca) for s in students]
    avg_grades  = [s.average_grade() for s in students]
    names       = [s.full_name for s in students]

    fig, ax = plt.subplots(figsize=(8, 5))
    scatter = ax.scatter(eca_counts, avg_grades, c=avg_grades,
                         cmap='RdYlGn', s=120, edgecolors='grey', zorder=3)

    for name, x, y in zip(names, eca_counts, avg_grades):
        ax.annotate(name, (x, y), textcoords="offset points",
                    xytext=(8, 4), fontsize=8)

    # Trend line
    if len(students) >= 2:
        z = np.polyfit(eca_counts, avg_grades, 1)
        p = np.poly1d(z)
        x_line = np.linspace(min(eca_counts), max(eca_counts), 100)
        ax.plot(x_line, p(x_line), "b--", alpha=0.5, label="Trend")

    ax.axhline(60, color='red', linestyle='--', alpha=0.4, label='Pass Threshold')
    ax.set_xlabel("Number of ECA Activities", fontsize=12)
    ax.set_ylabel("Average Grade", fontsize=12)
    ax.set_title("ECA Involvement vs Academic Performance", fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    plt.colorbar(scatter, label="Avg Grade")

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "eca_impact.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  [+] Chart saved: {path}")


#  3. PERFORMANCE ALERTS

def performance_alerts(students_map, threshold=60):
    print(f"\n  PERFORMANCE ALERTS  (threshold: {threshold})")
    print(f"  {'─'*50}")
    at_risk = [s for s in students_map.values() if s.average_grade() < threshold]
    if not at_risk:
        print("  ✓  No students below threshold. All performing well!")
    else:
        for s in sorted(at_risk, key=lambda x: x.average_grade()):
            print(f"\n  ⚠  {s.full_name} ({s.user_id})")
            print(f"     Average: {s.average_grade():.1f}  |  Status: {s.grade_status()}")
            weak = [(subj, mark) for subj, mark in s.grades.items() if mark < threshold]
            if weak:
                print(f"     Weak subjects: {', '.join(f'{subj}({mark})' for subj, mark in weak)}")
            print(f"     Suggestion: Schedule tutoring sessions and review core concepts.")


#  4. SUBJECT AVERAGE PIE CHART

def plot_subject_averages(students_map):
    subject_totals = {}
    subject_counts = {}
    for s in students_map.values():
        for subj, mark in s.grades.items():
            subject_totals[subj] = subject_totals.get(subj, 0) + mark
            subject_counts[subj] = subject_counts.get(subj, 0) + 1

    if not subject_totals:
        print("  No grade data.")
        return

    labels = sorted(subject_totals)
    averages = [subject_totals[l] / subject_counts[l] for l in labels]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Pie
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(labels)))
    wedges, texts, autotexts = ax1.pie(
        averages, labels=labels, autopct='%1.1f%%',
        colors=colors, startangle=140, pctdistance=0.8
    )
    for t in autotexts:
        t.set_fontsize(9)
    ax1.set_title("Subject Contribution to Overall Average", fontsize=11, fontweight='bold')

    # Bar
    bars = ax2.barh(labels, averages, color=colors, edgecolor='grey')
    for bar, avg in zip(bars, averages):
        ax2.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                 f"{avg:.1f}", va='center', fontsize=9)
    ax2.set_xlim(0, 110)
    ax2.axvline(60, color='red', linestyle='--', alpha=0.4, label='Pass (60)')
    ax2.set_title("Average Score by Subject", fontsize=11, fontweight='bold')
    ax2.set_xlabel("Average Marks")
    ax2.legend()
    ax2.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "subject_averages.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  [+] Chart saved: {path}")


#  DASHBOARD MENU

def analytics_dashboard(students_map):
    if not MATPLOTLIB_AVAILABLE:
        print("\n  [!] matplotlib/numpy not installed.")
        print("  Run: pip install matplotlib numpy")
        _pause()
        return

    _ensure_output_dir()

    while True:
        print(f"\n{'='*45}")
        print("  ANALYTICS DASHBOARD")
        print(f"{'='*45}")
        print("  [1] Grade Trends Chart")
        print("  [2] ECA Impact on Performance")
        print("  [3] Performance Alerts")
        print("  [4] Subject Average Charts")
        print("  [5] Generate All Charts")
        print("  [0] Back")
        print("=" * 45)

        choice = input("  Select option: ").strip()

        if choice == "1":
            plot_grade_trends(students_map)
            _pause()
        elif choice == "2":
            plot_eca_impact(students_map)
            _pause()
        elif choice == "3":
            performance_alerts(students_map)
            _pause()
        elif choice == "4":
            plot_subject_averages(students_map)
            _pause()
        elif choice == "5":
            print("\n  Generating all charts...")
            plot_grade_trends(students_map)
            plot_eca_impact(students_map)
            plot_subject_averages(students_map)
            performance_alerts(students_map)
            print(f"\n  All charts saved to: {OUTPUT_DIR}")
            _pause()
        elif choice == "0":
            break
        else:
            print("  [!] Invalid option.")