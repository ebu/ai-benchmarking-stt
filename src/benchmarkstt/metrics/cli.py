"""
Calculate metrics based on the comparison of a hypothesis with a reference.
"""

from benchmarkstt.input import core
from benchmarkstt.metrics import factory
from benchmarkstt.cli import args_from_factory
import argparse


def args_reference_hypothesis(parser):
    parser.add_argument('-r', '--reference', required=True,
                        help='The file to use as reference')
    parser.add_argument('-h', '--hypothesis', required=True,
                        help='The file to use as hypothesis')

    parser.add_argument('-rt', '--reference-type', default='infer',
                        help='Type of reference file')
    parser.add_argument('-ht', '--hypothesis-type', default='infer',
                        help='Type of hypothesis file')


def argparser(parser: argparse.ArgumentParser):
    # steps: input normalize[pre?] segmentation normalize[post?] compare

    args_reference_hypothesis(parser)

    metrics_desc = " A list of metrics to calculate. At least one metric needs to be provided."

    subparser = parser.add_argument_group('available metrics', description=metrics_desc)
    args_from_factory('metrics', factory, subparser)
    return parser


def file_to_iterable(file, type_, normalizer=None):
    if type_ == 'argument':
        return core.PlainText(file, normalizer=normalizer)
    return core.File(file, type_, normalizer=normalizer)


def main(parser, args, normalizer=None):
    ref = file_to_iterable(args.reference, args.reference_type, normalizer=normalizer)
    hyp = file_to_iterable(args.hypothesis, args.hypothesis_type, normalizer=normalizer)

    ref = list(ref)
    hyp = list(hyp)

    if 'metrics' not in args or not len(args.metrics):
        parser.error("need at least one metric")

    for item in args.metrics:
        metric_name = item.pop(0).replace('-', '.')
        print(metric_name)
        print('=' * len(metric_name))
        print()
        metric = factory.create(metric_name, *item)
        # todo: different output options
        result = metric.compare(ref, hyp)
        if type(result) is float:
            print("%.6f" % (result,))
        else:
            print(result)
        print()
