
"""
parameters:

1. Organism: {human, mouse, rat, Chinese hamster}
2. Model: {recon, recon v1, recon v2, recon v2.2}
3. Threshold type: {global, local}
    3a. Global thresholding parameters: 
        i. percentile_or_value: {percentile, value}
            a. {percentile} -> accept {percentile}
            b. {value} -> accept {value}
    3b. Local thresholding parameters:
        i. local threshold type: {minmaxmean, mean}
        ii. percentile_or_value: {percentile, value}
            a. {percentile} -> accept {low percentile} and {high percentile}
            b. {value} -> accept {low value} and {high value}

Follow-up:
>> Low_value: range?
>> High_value: range? 


MT_iCHOv1_final = "MT_iCHOv1_final.mat" - chinese hamster
MT_iHsa = "MT_iHsa.mat"
MT_iMM1415 = "MT_iMM1415.mat" --> mouse
MT_inesMouseModel = "MT_inesMouseModel.mat" --> mouse
MT_iRno = "MT_iRno.mat" --> rat
MT_quek14 = "MT_quek14.mat"

human
MT_recon_1 = "MT_recon_1.mat"
MT_recon_2 = "MT_recon_2.mat"
MT_recon_2_2_entrez = "MT_recon_2_2_entrez.mat"

all input data is human, except d/e.csv
for human data, use MT_recon_2_2_entrez
e.csv is mouse - use (not sure what authoritative model is) MT_iMM1415, MT_inesMouseModel
d.csv is chinese hamster  - 30 MB - takes 30 min to run - use MT_iCHOv1_final
"""

input_files = ["a.csv", "b.csv", "c.csv", "d.csv", "e.csv"]
organism = ["human", "mouse", "rat", "chinese hamster"]
models = ["recon", "recon v1", "recon v2", "recon v2.2"]

# local path variables
path_test_data = "/Users/shalkishrivastava/renci/ImmCellFIE/test-data"
path_cellfie_input = "/Users/shalkishrivastava/renci/ImmCellFIE/fuse-tool-cellfie/CellFie/input"

# cellfie parameters
mem = "10g"
# map
org_model = {"a.csv":"MT_recon_2_2_entrez.mat", "b.csv":"MT_recon_2_2_entrez.mat", "c.csv":"MT_recon_2_2_entrez.mat", "d.csv":"MT_iCHOv1_final.mat", "e.csv":"MT_iMM1415.mat", "e.csv":"MT_iMM1415.mat", "e.csv":"MT_inesMouseModel.mat" }

command = f"time docker run -it -m ${mem} -v ${path_test_data}:/data -v ${path_cellfie_input}:/input -w /input hmasson/cellfie-standalone-app:v2"

threshold_type = ["global", "local"]
percentile_or_value = ["percentile", "value"]
local_threshold_type = ["minmaxmean", "mean"]

"""
measure file dimensions

head -1 {input_file} | sed 's/[^,]//g' | wc -c
"""

file_dimensions = {"a.csv":7, "b.csv":7, "c.csv":65, "d.csv":190, "e.csv":97}

for input_file, model in org_model.items():
    command += f" /data/${input_file} ${file_dimensions.get(input_file)} ${model}"
    for threshold in threshold_type:
        if threshold == "global":
            for pv in percentile_or_value:
                if pv == "percentile":
                    for p in range(0, 110, 10):
                        command =  f"${threshold_type} ${pv}"




"""
Command to run cellfie from terminal:

"time docker run -it -m 10g -v /Users/shalkishrivastava/renci/ImmCellFIE/test-data:/data -v /Users/shalkishrivastava/renci/ImmCellFIE/fuse-tool-cellfie/CellFie/input:/input -w /input hmasson/cellfie-standalone-app:v2 /data/e.csv 96 MT_iCHOv1_final.mat global percentile 50 minmaxmean 25 75 /data"
"""
