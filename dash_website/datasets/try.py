from dash_website.utils.aws_loader import load_npy

dimension = "PhysicalActivity"
subdimension = "Walking"
sub_subdimension = "3D"
channel = 0
sex = "female"
age_group = "young"
sample = "0"

path_to_time_series = (
    f"datasets/time_series/{dimension}/{subdimension}/{sub_subdimension}/{sex}/{age_group}/sample_{sample}.npy"
)

time_series = load_npy(path_to_time_series)

print("time_series", time_series.ndim)
print("time_series", type(time_series))
print("time_series[channel]", time_series[int(channel)])
print("time_series[channel]", type(time_series[int(channel)]))