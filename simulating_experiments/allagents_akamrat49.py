"""
Run simulations of the agents, with parameters fit to the akam rat (mouse) data 49.
"""
import sys
sys.path.append('..')
from tasks import akam_tasks as ts
from utils import *
from path_settings import *
from simulate_experiment import *
import joblib
goto_root_dir.run()

sim_config = {
    'task': 'Akam_RTS',
    'com_prob': 0.8, # common transition probability
    'rew_gen': 'trans_rev',
    'block_length': 50,
    'rew_probs':[0.2, 0.8],
    'trans_rev_length': 50,
    'n_blocks': 100,
    'n_trials': 150,
    'sim_seed': 0,
    'additional_name': '',
    'use_one_hot': 'cso', # no effect for cog models and GRU models, but work for SGRU
}
for sub in [49
            ]:
    ana_exp_path = ANA_SAVE_PATH / f'exp_seg_akamrat{sub}'

    sim_exp_name = get_current_file_name(__file__).replace('_all', str(sub))

    for n_blocks, n_trials in [
        (100, 150),
        ]:
        sim_config['n_blocks'] = n_blocks
        sim_config['n_trials'] = n_trials
        sim_config['sim_exp_name'] = sim_exp_name + '_nblocks' + str(n_blocks) + '_ntrials' + str(n_trials)

        task = ts.Two_step(com_prob=sim_config['com_prob'], rew_gen=sim_config['rew_gen'],
                         block_length=sim_config['block_length'],
                         probs=sim_config['rew_probs'],
                           trans_rev_length=sim_config['trans_rev_length'],
                           )

        path = ana_exp_path / 'cog_final_best_summary.pkl'
        cog_summary = joblib.load(path)

        path = ana_exp_path / 'rnn_final_best_summary.pkl'
        rnn_summary = joblib.load(path)

        summary_cond = lambda summary: len(summary) == 10
        iter_model_infos = [] # (model_type, additional_name, this_model_summary, summary_cond)
        for model_type in [
                              'Q(1)',
                              'MFs',
                            'MF_bs_rb_ck',
                            'MB_bs_rb_ck',
                            'MF_dec_bs_rb_ck',
                            'MB_dec_bs_rb_ck',
                ]:
            iter_model_infos.append((model_type, '', cog_summary[cog_summary['cog_type'] == model_type], summary_cond))
        filter = lambda df: (df['readout_FC'])
        if 'finetune' in rnn_summary.columns:
            filter = lambda df: (df['readout_FC']) & (df['finetune'] == 'none')
        iter_model_infos.append(
            ('SGRU', '1', rnn_summary[
                (rnn_summary['rnn_type'] == 'SGRU') & (rnn_summary['hidden_dim'] == 1) & filter(rnn_summary)],
             summary_cond))
        iter_model_infos.append(
            ('GRU', '2', rnn_summary[
                (rnn_summary['rnn_type'] == 'GRU') & (rnn_summary['hidden_dim'] == 2) & filter(rnn_summary)],
             summary_cond))
        iter_model_infos.append(
            ('GRU', '4', rnn_summary[
                (rnn_summary['rnn_type'] == 'GRU') & (rnn_summary['hidden_dim'] == 4) & filter(rnn_summary)],
             summary_cond))

        iterate_each_model(iter_model_infos, task, sim_config)