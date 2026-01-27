# report.py
import csv
import matplotlib.pyplot as plt
from jinja2 import Template


def generate_csv(path, rows):
    if not rows:
        print("[WARN] CSV rows 為空，無法寫入")
        return

    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"[INFO] CSV 產生完成: {path}")


def plot_curve(x, y, xlabel, ylabel, img_path):
    if not x or not y or len(x) != len(y):
        print("[WARN] X/Y 資料長度不匹配或為空，無法畫圖")
        return

    plt.figure(figsize=(6, 4))
    plt.plot(x, y, marker='o', linestyle='-', color='b', label='UDP Loss %')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title('UDP Loss vs Target BW')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(img_path)
    plt.close()
    print(f"[INFO] 圖表已儲存: {img_path}")


def plot_bar(data_dict, title, ylabel, img_path):
    """
    畫簡單的條形圖
    :param data_dict: dict {label: value}
    """
    labels = list(data_dict.keys())
    values = list(data_dict.values())

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color='skyblue')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(img_path)
    plt.close()
    print(f"[INFO] 條形圖已儲存: {img_path}")


def generate_html(path, context):
    html_template = '''
<html>
<head><title>RF / Network Test Report</title></head>
<body>
<h1>RF / Network Test Report</h1>
<p>Date: {{ date }}</p>
<p>Interface: {{ interface }}</p>
<p><b>Status: {{ status }}</b></p>
<h3>UDP Loss Plot</h3>
<img src="{{ loss_plot }}" alt="Loss Plot">
{% if bar_plot %}
<h3>各指標統計</h3>
<img src="{{ bar_plot }}" alt="Bar Plot">
{% endif %}
</body>
</html>
'''
    template = Template(html_template)
    with open(path, 'w') as f:
        f.write(template.render(**context))
    print(f"[INFO] HTML 報表已生成: {path}")
