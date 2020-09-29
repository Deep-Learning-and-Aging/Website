cp /n/groups/patel/samuel/LinearOutput/*.csv /n/groups/patel/samuel/data_final/page1_biomarkers/LinearOutput/
cp /n/groups/patel/samuel/final_inputs/*.csv /n/groups/patel/samuel/data_final/page1_biomarkers/BiomarkerDatasets/
cp /n/groups/patel/Alan/Aging/Medical_Images/data/PERFORMANCES*.csv /n/groups/patel/samuel/data_final/page2_predictions/Performances/
cp /n/groups/patel/samuel/feature_importances_final/*csv /n/groups/patel/samuel/data_final/page3_featureImp/FeatureImp/
cp /n/groups/patel/Alan/Aging/Medical_Images/data/ResidualsCorrelations*.csv /n/groups/patel/samuel/data_final/page4_correlations/ResidualsCorrelations/
cp /n/groups/patel/samuel/EWAS/linear_output_final/*csv /n/groups/patel/samuel/data_final/page5_LinearXWASResults/LinearOutput/
cp /n/groups/patel/samuel/EWAS/Correlations/Correlations_*.csv /n/groups/patel/samuel/data_final/page6_LinearXWASCorrelations/CorrelationsLinear/
cp /n/groups/patel/samuel/EWAS/Scores/*.csv /n/groups/patel/samuel/data_final/page7_MultivariateXWASResults/Scores/
cp /n/groups/patel/samuel/EWAS/Correlations/CorrelationsMultivariate*.csv /n/groups/patel/samuel/data_final/page8_MultivariateXWASCorrelations/CorrelationsMultivariate/
cp -r /n/groups/patel/Alan/Aging/Medical_Images/figures/Attention_Maps/Age/ /n/groups/patel/samuel/data_final/page9_AttentionMaps/Images
cp /n/groups/patel/Alan/Aging/Medical_Images/data/AttentionMaps*.csv /n/groups/patel/samuel/data_final/page9_AttentionMaps/Attention_maps_infos
cp /n/groups/patel/Alan/Aging/Medical_Images/figures/GWAS/*.png /n/groups/patel/samuel/data_final/page10_GWASResults/Manhattan
cp  /n/groups/patel/Alan/Aging/Medical_Images/data/GWAS_hits_Age_* /n/groups/patel/samuel/data_final/page10_GWASResults/Volcano
cp /n/groups/patel/Alan/Aging/Medical_Images/data/GWAS_heritabilities_Age.csv /n/groups/patel/samuel/data_final/page11_GWASHeritability/Heritability/GWAS_heritabilities_Age.csv

cp /n/groups/patel/JbProst/Heart/ActivationMap/Age/AttentionMaps-samples_Age_Heart_MRI_* /n/groups/patel/samuel/data_final/page12_AttentionMapsVideos/AttentionMapsVideos
cp /n/groups/patel/JbProst/Heart/ActivationMap/Age/Gradient/Gif/*.gif /n/groups/patel/samuel/data_final/page12_AttentionMapsVideos/gif
cp /n/groups/patel/JbProst/Heart/ActivationMap/Age/Gradient/2D/*.jpg /n/groups/patel/samuel/data_final/page12_AttentionMapsVideos/img

cp -r /n/groups/patel/Alan/Aging/Medical_Images/figures/Images_TimeSeries/Age/ /n/groups/patel/samuel/data_final/page13_AttentionMapsTimeSeries/img
#cp -r /n/groups/patel/Alan/Aging/Medical_Images/figures/Attention_Maps/Age/Heart /n/groups/patel/samuel/data_final/page13_AttentionMapsTimeSeries/attentionmaps/
#cp -r /n/groups/patel/Alan/Aging/Medical_Images/figures/Attention_Maps/Age/PhysicalActivity /n/groups/patel/samuel/data_final/page13_AttentionMapsTimeSeries/attentionmaps/
#cp -r /n/groups/patel/Alan/Aging/Medical_Images/figures/Attention_Maps/Age/Arterial*PulseWaveAnalysis* /n/groups/patel/samuel/data_final/page13_AttentionMapsTimeSeries/attentionmaps/



scp -r "sd375@transfer.rc.hms.harvard.edu:/n/groups/patel/samuel/data_final/page13_AttentionMapsTimeSeries/" Desktop/dash_app/data/page13_AttentionMapsTimeSeries/
