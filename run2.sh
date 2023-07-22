#!/bin/bash

# . conda/bin/activate 



datapath=data/features

# exp_name=tuning

## procedure
procedure='train_test'
# procedure='train'
# procedure='test'

## model config
seg_method='sample'
num_seg=32
cnn_kernel_size=5
num_cnn_layer=2
# num_encoder_layers=2
# num_decoder_layers=4
num_gru_layers=2
d_model=192
dout_p=0.2
no_sen_fusion='--no_sen_fusion'
# no_sen_fusion=''
jst='--jst'
# jst=''
min_iou=0.5
max_iou=1.0

## training 
device_ids='5'
batch_size=16 # per device
num_workers=4
weight_decay=0.001
lr=0.0003
sim_weight=1
tan_weight=1
teacher_weight=0.5
student_weight=0.5
min_freq_caps=2
smoothing=0
shrank=''
epoch_num=50
one_by_one_starts_at=10

## decoding_method
# decoding_method='greedy'
decoding_method='beam_search'

## log and debug
# debug="--debug"
# dont_log="--dont_log"
# wandb=""
debug=""
dont_log=""
wandb="--wandb"

last_only="--last_only"

train_set=./data/train_set4DSTC8-AVSD+reason.json
val_set=./data/valid_set4DSTC10-AVSD+reason.json
test_set=./data/test_set4DSTC10-AVSD_multiref+reason.json
test_set7=data/mock_test_set4DSTC10-AVSD_from_DSTC7_multiref.json
test_set8=data/mock_test_set4DSTC10-AVSD_from_DSTC8_multiref.json

log_dir=./log

# convert data
# echo "Coverting json files to csv for the tool"
# generate_csv='utils/generate_previous_csv.py'
# num_prev=0
# python $generate_csv duration_info/duration_Charades_v1_480.csv $train_set train ./data/dstc10_train.csv $num_prev
# python $generate_csv duration_info/duration_Charades_v1_480.csv $val_set val ./data/dstc10_val.csv $num_prev
# python $generate_csv duration_info/duration_Charades_v1_480.csv $val_set test ./data/dstc10_val_one.csv $num_prev
# python $generate_csv duration_info/duration_Charades_vu17_test_480.csv $test_set test ./data/dstc10_test.csv $num_prev
# python $generate_csv duration_info/duration_Charades_vu17_test_480.csv $test_set7 test ./data/dstc7_test.csv $num_prev
# python $generate_csv duration_info/duration_Charades_vu17_test_480.csv $test_set8 test ./data/dstc8_test.csv $num_prev
# return


lr=0.0003
num_encoder_layers=2
num_decoder_layers=4


function run_exp(){
    # Train
    echo $exp_name
    # echo Start training
    python main.py \
    --train_meta_path ./data/dstc10_train.csv \
    --val_meta_path ./data/dstc10_val.csv \
    --test_meta_path ./data/dstc10_test2.csv \
    --reference_paths $val_set \
    --procedure $procedure \
    --batch_size $batch_size \
    --num_encoder_layers $num_encoder_layers \
    --num_decoder_layers $num_decoder_layers \
    --num_gru_layers $num_gru_layers \
    --d_vid 2048 --d_aud 128 \
    --d_model $d_model \
    --dout_p $dout_p \
    --num_seg $num_seg \
    --cnn_kernel_size $cnn_kernel_size \
    --num_cnn_layer $num_cnn_layer \
    --use_linear_embedder \
    --device_ids $device_ids \
    --epoch_num $epoch_num \
    --one_by_one_starts_at $one_by_one_starts_at \
    --stopwords ./data/stopwords.txt \
    --exp_name $exp_name \
    --log_dir $log_dir \
    --num_workers $num_workers \
    --num_seg $num_seg \
    --seg_method $seg_method \
    --no_sen_fusion $no_sen_fusion \
    --weight_decay $weight_decay \
    --min_iou $min_iou \
    --max_iou $max_iou \
    --lr $lr \
    --decoding_method $decoding_method \
    --sim_weight $sim_weight \
    --tan_weight $tan_weight \
    --teacher_weight $teacher_weight \
    --student_weight $student_weight \
    --min_freq_caps $min_freq_caps \
    --smoothing $smoothing \
    --pretrained_cap_model_path $pretrained_cap_model_path \
    $jst \
    $teacher \
    --teacher_path $teacher_path \
    $av_mapping \
    $bimodal_encoder \
    $update_gate \
    $debug \
    $dont_log \
    $last_only \
    $wandb
}

# procedure='train'
# pretrained_cap_model_path='log/train_teacher/best_cap_model.pt'
# batch_size=16
# jst=''
# teacher='--teacher'
# teacher_path=''
# av_mapping=''
# bimodal_encoder=''
# update_gate='--update_gate'
# exp_name="train_teacher"
# run_exp


# procedure='train_test'
procedure='test'
pretrained_cap_model_path=''
batch_size=16
jst='--jst'
teacher=''
teacher_path='./log/train_teacher/best_cap_model.pt'
av_mapping=''
bimodal_encoder=''
update_gate='--update_gate'
exp_name="train_jst"
run_exp


echo 'end'