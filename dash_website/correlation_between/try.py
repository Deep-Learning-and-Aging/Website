def LoadData(value_eid_vs_instances, value_aggregate, value_organ, value_step):
    dict_value_step_value = dict(zip(["Validation", "Train", "Test"], ["val", "train", "test"]))
    if value_aggregate == "bestmodels":
        df = load_csv(
            path_residualscorr
            + "ResidualsCorrelations_bestmodels_%s_Age_%s.csv"
            % (value_eid_vs_instances, dict_value_step_value[value_step])
        )
        std = load_csv(
            path_residualscorr
            + "ResidualsCorrelations_bestmodels_sd_%s_Age_%s.csv"
            % (value_eid_vs_instances, dict_value_step_value[value_step])
        )
        if value_eid_vs_instances == "*":
            df_instances = load_csv(
                path_residualscorr
                + "ResidualsCorrelations_bestmodels_%s_Age_%s.csv" % ("*", dict_value_step_value[value_step])
            )

    index_std = std.columns[0]
    index = df.columns[0]
    std = std.set_index(index_std)
    df = df.set_index(index)
    std.index.name = "Models"
    df.index.name = "Models"

    df.index = ["-".join(elem.split("_")[:4]) for elem in df.index.values]
    df.columns = ["-".join(elem.split("_")[:4]) for elem in df.index.values]

    std.index = ["-".join(elem.split("_")[:4]) for elem in std.index.values]
    std.columns = ["-".join(elem.split("_")[:4]) for elem in std.index.values]

    if value_aggregate == "bestmodels":
        scores = load_csv(
            path_performance
            + "PERFORMANCES_bestmodels_alphabetical_%s_Age_%s.csv"
            % (value_eid_vs_instances, dict_value_step_value[value_step])
        )[["version", "R-Squared_all"]].set_index("version")
        scores_organs = [elem.split("_")[1] for elem in scores.index.values]
        scores_view = [
            (elem.split("_")[2]).replace("*", "").replace("HearingTest", "").replace("BloodCount", "")
            for elem in scores.index.values
        ]
        scores.index = [organ + view for organ, view in zip(scores_organs, scores_view)]

        intersect = scores.index.intersection(df.index)
        customdata_score = scores.loc[intersect]
        df = df.loc[intersect, intersect]

    customdata_score_eids = customdata_score_eids["R-Squared_all"].values
    customdata_score_eids_x = np.tile(customdata_score_eids, (len(customdata_score_eids), 1))
    customdata_score_eids_y = customdata_score_eids_x.T

    customdata_score_instances = customdata_score_instances["R-Squared_all"].values
    customdata_score_instances_x = np.tile(customdata_score_instances, (len(customdata_score_instances), 1))
    customdata_score_instances_y = customdata_score_instances_x.T

    na_instances = df_instances.isna().values

    customdata_score_x = copy.deepcopy(df)
    customdata_score_y = copy.deepcopy(df)
    customdata_score_x.values[na_instances] = customdata_score_instances_x[na_instances]
    customdata_score_y.values[na_instances] = customdata_score_instances_y[na_instances]
    customdata_score_x.values[np.invert(na_instances)] = customdata_score_eids_x[np.invert(na_instances)]
    customdata_score_y.values[np.invert(na_instances)] = customdata_score_eids_y[np.invert(na_instances)]

    custom_order = []
    for organ_ in order:
        custom_order = custom_order + list(df.index[df.index.str.contains(organ_)])
    difference = df.index.difference(Index(custom_order))
    custom_order = list(difference) + custom_order

    return customdata_score_x, customdata_score_y, df, std, custom_order
