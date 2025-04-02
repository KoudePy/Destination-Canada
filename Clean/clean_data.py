import pandas as pd

def load_and_clean_data(input_path, output_path):
    df = pd.read_csv(input_path, sep="\t")

    df = df.rename(columns={
        "EN_YEAR": "Year",
        "EN_MONTH": "Month",
        "EN_QUARTER": "Quarter",
        "EN_PROVINCE_TERRITORY": "Province",
        "EN_IMMIGRATION_CATEGORY-MAIN_CATEGORY": "MainCategory",
        "EN_IMMIGRATION_CATEGORY-GROUP": "GroupCategory",
        "EN_IMMIGRATION_CATEGORY-COMPONENT": "SubCategory",
        "TOTAL": "Total"
    })

    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
    df = df.dropna(subset=["Total"])

    df.to_csv(output_path, index=False)
    print(f"Données nettoyées sauvegardées dans : {output_path}")

if __name__ == "__main__":
    load_and_clean_data("data/data1.csv", "data/cleaned_data1.csv")
