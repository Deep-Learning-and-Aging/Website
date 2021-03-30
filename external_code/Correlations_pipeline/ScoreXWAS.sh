job_name="create_score_XWAS.job"
out_file="/n/groups/patel/samuel/Aging/logs/create_score_XWAS.out"
err_file="/n/groups/patel/samuel/Aging/logs/create_score_XWAS.err"

sbatch --error=$err_file --output=$out_file --job-name=$job_name --mem-per-cpu=16G -c 1 -p short -t 0-11:59 XWAS_scores_single.sh
