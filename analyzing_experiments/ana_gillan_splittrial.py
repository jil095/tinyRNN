import pandas as pd

from analyzing_experiments.analyzing_dynamics import *
from analyzing_experiments.analyzing_perf import *
from analyzing_experiments.analyzing_check import *
from analyzing_experiments.analyzing_decoding import *
from matplotlib import pyplot as plt
from utils import goto_root_dir
goto_root_dir.run()

analyzing_pipeline = [
    # 'analyze_model_perf_for_each_exp',
    'compile_perf_for_all_exps',
    # 'examine_readout_weight_exp',
    # 'run_scores_for_each_exp',
    # 'run_dynamical_regression_for_each_exp',
    # 'compile_cog_model_param_for_each_exp',
]

exp_folders = [
    'exp_Gillan_splittrial',
]
compile_folder = 'exp_Gillan_splittrial_sub_avg'
# perf
if 'analyze_model_perf_for_each_exp' in analyzing_pipeline:
    for exp_folder in exp_folders:
        find_best_models_for_exp(exp_folder, 'OTSCog',
                                 additional_rnn_keys={'model_identifier_keys': ['block','distill','pretrained',
                                                                                'distill_temp','teacher_prop',
                                                                                ],
                                                      },
                                 additional_cog_keys={'model_identifier_keys': ['block','distill']},
                                 rnn_sort_keys=['block', 'hidden_dim'],
                                 cog_sort_keys=['block'],
                                 has_rnn=True,
                                 has_cog=True,
                                 cog_hidden_dim={
                                     'MF': 2*3,
                                     'MB': 2*2,
                                     'MX': 2*3,
                                     'MFs': 3,
                                     'MBs': 2,
                                     'MXs': 3,
                                     'MFsr': 3,
                                 },
                                 return_dim_est=True,
                                 include_acc=True,
                                 include_acc_filter=lambda row: 'hidden_dim' not in row or row['hidden_dim'] <=20,
                                 check_missing=False,
                                 )

if 'compile_perf_for_all_exps' in analyzing_pipeline:
    # compile_perf_for_exps(exp_folders,compile_folder,
    #                       additional_rnn_keys={'model_identifier_keys': ['distill','pretrained']},
    #                       rnn_filter={'distill': 'student'},
    #                       lambda_filter=lambda dt, dt_ref: dt['block'].isin(pd.unique(dt_ref[dt_ref['rnn_type'] == 'MLR']['block'])),
    #                       lambda_filter_name='_ref_MLRblock',
    #                       )
    compile_perf_for_exps(exp_folders, compile_folder,
                          additional_rnn_keys={'model_identifier_keys': ['distill','pretrained',
                                                                         'distill_temp','teacher_prop']},
                          additional_cog_keys={'model_identifier_keys': ['distill', ]},
                          rnn_filter={'distill': 'student', 'rnn_type': 'GRU'#, 'pretrained':'none'
                                      },
                          # lambda_filter=lambda dt, dt_ref: dt['block'].isin(
                          #     pd.unique(dt_ref[dt_ref['rnn_type'] == 'GRU']['block'])),
                          # lambda_filter_name='_noMLR',
                          has_rnn=True,
                          has_cog=True,
                          )
# dynamics
if 'run_scores_for_each_exp' in analyzing_pipeline:
    for exp_folder in exp_folders:
        # # only analyze cog models
        # run_scores_exp(exp_folder, demask=False, pointwise_loss=True,
        #                overwrite_config={'behav_data_spec': {'augment': True}},
        #                include_data='test_augment',
        #                has_cog=True,
        #                has_rnn=False,
        #                )
        #
        # # only analyze student networks
        # run_scores_exp(exp_folder, demask=False, pointwise_loss=True,
        #                model_filter={'distill': 'student', 'rnn_type': 'GRU'},
        #                overwrite_config={'behav_data_spec': {'augment': True}},
        #                include_data='test_augment',
        #                has_cog=False,
        #                has_rnn=True,
        #                )
        # for tch models, 'augment': 2, include_data='all'
        run_scores_exp(exp_folder, demask=False, pointwise_loss=True,
                       model_filter={'distill': 'none', 'rnn_type': 'GRU'},
                       overwrite_config={
                           'behav_data_spec': {'augment': True
                                               },
                           'device': 'cpu',
                       },
                       include_data='all',
                       has_cog=False,
                       )