import argparse
import logging

from core import *
from managers import *
from utils import *

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='TransE model')

parser.add_argument("--experiment_name", type=str, default="default",
                    help="Experiment folder to load model from")


parser.add_argument("--p_norm", type=int, default=1,
                    help="The norm to use for the distance metric")
parser.add_argument("--embedding_dim", type=int, default=50,
                    help="Entity and relations embedding size")
parser.add_argument("--neg_sample_size", type=int, default=30,
                    help="No. of negative samples to compare to for MRR/MR/Hit@10")

params = parser.parse_args()

exps_dir = os.path.join(MAIN_DIR, 'experiments')
params.exp_dir = os.path.join(exps_dir, params.experiment_name)

test_data_sampler = DataSampler(TEST_DATA_PATH)
transE = initialize_model(params)
evaluator = Evaluator(transE, test_data_sampler, params.neg_sample_size)

logging.info('Testing model %s' % os.path.join(params.exp_dir, 'best_model.pth'))

log_data = evaluator.get_log_data()
logging.info('Test performance:' + str(log_data))