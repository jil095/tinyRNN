from analyzing_experiments.analyzing_perf import *
from analyzing_experiments.analyzing_check import *
from analyzing_experiments.analyzing_dynamics import *
from analyzing_experiments.analyzing_decoding import *
from utils import goto_root_dir
goto_root_dir.run()

analyzing_pipeline = [
    # 'analyze_model_perf_for_each_exp',
    # 'compile_perf_for_all_exps',
    # 'extract_model_par',
    # 'run_scores_for_each_exp_best_for_test',
    # 'run_scores_for_each_exp',
    # 'run_2d_inits_for_each_exp',
    # 'extract_1d_for_each_exp',
    # 'extract_ev_for_each_exp',

]
exp_folders = [
    'exp_seg_akamratrts279', # missing some GRU d=3
    'exp_seg_akamratrts278',
    'exp_seg_akamratrts277',
    'exp_seg_akamratrts275',
    'exp_seg_akamratrts274',
    'exp_seg_akamratrts273',
    'exp_seg_akamratrts272',
    'exp_seg_akamratrts271',
    'exp_seg_akamratrts270',
    'exp_seg_akamratrts269',
]

## perf
if 'analyze_model_perf_for_each_exp' in analyzing_pipeline:
    for exp_folder in exp_folders:
        find_best_models_for_exp(exp_folder, 'RTSCog',
                                 additional_rnn_keys={'model_identifier_keys': ['complex_readout','finetune','symm']},
                                 include_acc=True,)

if 'compile_perf_for_all_exps' in analyzing_pipeline:
    compile_perf_for_exps(exp_folders, 'exp_seg_akamratrts',
                          rnn_filter={'readout_FC': True,
                                      })


if 'extract_model_par' in analyzing_pipeline:
        extract_model_par(exp_folders[0])

if 'extract_sv_for_each_exp' in analyzing_pipeline:
    for exp_folder in exp_folders:
        extract_sv_for_exp(exp_folder)
# dynamics
for exp_folder in exp_folders:
    if 'run_scores_for_each_exp' in analyzing_pipeline:
        run_scores_exp(exp_folder)
    if 'run_scores_for_each_exp_best_for_test' in analyzing_pipeline:
        run_scores_exp(exp_folder, best_for_test=True)
    if 'run_2d_inits_for_each_exp' in analyzing_pipeline:
        run_2d_inits_exp(exp_folder, grid_num=50)


# 1d logit features
if 'extract_1d_for_each_exp' in analyzing_pipeline:
    for exp_folder in exp_folders:
        extract_1d_logit_for_exp(exp_folder)

