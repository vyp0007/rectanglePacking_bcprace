import os
import re


def filename_to_caption(filename: str) -> str:
    """
    Convert filename into a readable caption.
    Example:
        experiment_c1_1.5_c2_1.5_w_0.7.txt
        -> "Results for experiment (c1=1.5, c2=1.5, w=0.7)"
    """
    name = os.path.splitext(filename)[0]

    # Extract parameter-like patterns
    params = re.findall(r'([a-zA-Z]+)_([0-9.]+)', name)

    if params:
        param_str = ", ".join(f"{k}={v}" for k, v in params)
        base = re.sub(r'(_[a-zA-Z]+_[0-9.]+)+', '', name)
        base = base.replace("_", " ").strip()
        return f"{base.capitalize()} ({param_str})"
    else:
        return name.replace("_", " ").capitalize()


def filename_to_label(filename: str) -> str:
    """
    Convert filename into a safe LaTeX label.
    """
    name = os.path.splitext(filename)[0]
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '_', name)
    return f"tab:{name}"


def process_latex_tables(input_dir, output_file, step=10):

    with open(output_file, "w", encoding="utf-8") as out_f:

        for filename in sorted(os.listdir(input_dir)):
            file_path = os.path.join(input_dir, filename)

            if not os.path.isfile(file_path):
                continue

            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Locate table
            begin_idx = None
            end_idx = None

            for i, line in enumerate(lines):
                if "\\begin{tabular}" in line:
                    begin_idx = i
                if "\\end{tabular}" in line:
                    end_idx = i
                    break

            if begin_idx is None or end_idx is None:
                continue

            header = []
            data = []
            footer = []

            in_data = False

            for line in lines[begin_idx:end_idx + 1]:
                stripped = line.strip()

                if stripped.startswith("\\midrule"):
                    in_data = True
                    header.append(line)
                    continue

                if stripped.startswith("\\bottomrule"):
                    in_data = False
                    footer.append(line)
                    continue

                if not in_data:
                    if not footer:
                        header.append(line)
                    else:
                        footer.append(line)
                else:
                    data.append(line)

            # Keep every Nth row
            filtered_data = [row for i, row in enumerate(data) if i % step == 0]

            # Optionally keep last row
            if data and data[-1] not in filtered_data:
                filtered_data.append(data[-1])

            # Generate caption + label
            caption = filename_to_caption(filename)
            label = filename_to_label(filename)

            # Write full LaTeX table
            out_f.write("\\begin{table}[htbp]\n")
            out_f.write("    \\centering\n")
            out_f.write(f"    \\caption{{{caption}}}\n")
            out_f.write(f"    \\label{{{label}}}\n")

            out_f.writelines(["    " + line for line in header])
            out_f.writelines(["    " + line for line in filtered_data])
            out_f.writelines(["    " + line for line in footer])

            out_f.write("\\end{table}\n\n\n")


if __name__ == "__main__":
    input_dir = "./latex_export"
    output_file = "./latex_merged/mergedPSO.tex"
    step = 10

    process_latex_tables(input_dir, output_file, step)