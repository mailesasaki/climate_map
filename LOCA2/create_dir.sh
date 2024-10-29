declare -a models=("ACCESS-CM2" "ACCESS-ESM1-5" "AWI-CM-1-1-MR" "BCC-CSM2-MR" "CESM2-LENS" "CNRM-CM6-1" "CNRM-CM6-1-HR" "CNRM-ESM2-1" "CanESM5" "EC-Earth3" "EC-Earth3-Veg" \
"FGOALS-g3" "GFDL-CM4" "GFDL-ESM4" "HadGEM3-GC31-LL" "HadGEM3-GC31-MM" "INM-CM4-8" "INM-CM5-0" "IPSL-CM6A-LR" "KACE-1-0-G" "MIROC6" "MPI-ESM1-2-HR" "MPI-ESM1-2-LR" \
"MRI-ESM2-0" "NorESM2-LM" "NorESM2-MM" "TaiESM1")

for i in "${models[@]}"
do
   mkdir -p "$i/historical"
   mkdir -p "$i/ssp245"
   mkdir -p "$i/ssp370"
   mkdir -p "$i/ssp585"
   # or do whatever with individual element of the array
done
