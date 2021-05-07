from dash_website.utils.aws_loader import load_csv

COLUMNS_TO_TAKE = {
    "SNP": "SNP",
    "CHR": "chromosome",
    "Gene": "Gene",
    "Gene_type": "Gene_type",
    "P_BOLT_LMM_INF": "p_value",
    "BETA": "size_effect",
    "organ": "dimension",
}

if __name__ == "__main__":
    size_effects = load_csv("page10_GWASResults/Volcano/GWAS_hits_Age_All_withGenes.csv")[COLUMNS_TO_TAKE].rename(
        columns=COLUMNS_TO_TAKE
    )
    size_effects.replace({"*instances1": "*instances1.5x", "ImmuneSystem": "BloodCells"}, inplace=True)
    size_effects.drop(index=size_effects[size_effects["dimension"] == "withGenes"].index, inplace=True)
    size_effects.reset_index(drop=True).to_feather("all_data/genetics/gwas/size_effects.feather")
